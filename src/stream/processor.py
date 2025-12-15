"""
Stream Processor - przetwarzanie strumienia sygnałów

Ten moduł obsługuje czytanie i przetwarzanie sygnałów z różnych źródeł:
- Pliki CSV
- Stdin
- Generatory (dla symulacji)
"""

import sys
from pathlib import Path
from typing import Generator, List, Optional, Callable
from dataclasses import dataclass
from datetime import datetime

sys.path.insert(0, str(Path(__file__).parent.parent))
from evaluator.signal import Signal, parse_signal
from evaluator.threat_matcher import ThreatMatcher, ThreatAssessment
from parser.models import RulesDatabase


@dataclass
class ProcessingResult:
    """
    Wynik przetwarzania strumienia sygnałów

    Attributes:
        total_signals: Łączna liczba przetworzonych sygnałów
        assessments: Lista wszystkich ocen zagrożenia
        errors: Lista błędów podczas przetwarzania
        processing_time: Czas przetwarzania (opcjonalnie)
    """
    total_signals: int
    assessments: List[ThreatAssessment]
    errors: List[str]
    processing_time: Optional[float] = None

    @property
    def success_rate(self) -> float:
        """Procent pomyślnie przetworzonych sygnałów"""
        if self.total_signals == 0:
            return 0.0
        return (len(self.assessments) / self.total_signals) * 100

    @property
    def error_rate(self) -> float:
        """Procent błędów"""
        if self.total_signals == 0:
            return 0.0
        return (len(self.errors) / self.total_signals) * 100


class SignalReader:
    """
    Reader sygnałów z różnych źródeł

    Obsługuje czytanie z:
    - Plików CSV
    - Stdin
    - List
    """

    @staticmethod
    def read_file(
        file_path: str | Path,
        skip_comments: bool = True,
        skip_empty: bool = True
    ) -> Generator[Signal, None, None]:
        """
        Czyta sygnały z pliku CSV

        Format pliku:
            # Komentarz (jeśli skip_comments=True, ignorowany)
            w2,f3,t1,r2,a1,d3
            w1,f1,t1,r1,a1,d2

        Args:
            file_path: Ścieżka do pliku
            skip_comments: Czy pomijać linie zaczynające się od #
            skip_empty: Czy pomijać puste linie

        Yields:
            Signal: Kolejne sygnały z pliku

        Raises:
            FileNotFoundError: Jeśli plik nie istnieje
            ValueError: Jeśli format sygnału jest niepoprawny
        """
        path = Path(file_path)
        if not path.exists():
            raise FileNotFoundError(f"File not found: {path}")

        with open(path, 'r', encoding='utf-8') as f:
            line_num = 0
            for line in f:
                line_num += 1
                line = line.strip()

                # Pomiń komentarze
                if skip_comments and line.startswith('#'):
                    continue

                # Pomiń puste linie
                if skip_empty and not line:
                    continue

                try:
                    signal = parse_signal(line)
                    yield signal
                except ValueError as e:
                    raise ValueError(
                        f"Invalid signal format at line {line_num}: {line}\n"
                        f"Error: {str(e)}"
                    ) from e

    @staticmethod
    def read_stdin(
        prompt: str = "Enter signal (w,f,t,r,a,d): "
    ) -> Generator[Signal, None, None]:
        """
        Czyta sygnały ze stdin (interaktywny tryb)

        Args:
            prompt: Prompt wyświetlany użytkownikowi

        Yields:
            Signal: Sygnały wprowadzone przez użytkownika

        Przykład:
            for signal in SignalReader.read_stdin():
                print(f"Received: {signal}")
        """
        print("Interactive mode. Enter signals or 'q' to quit.")
        while True:
            try:
                line = input(prompt).strip()

                if line.lower() in ['q', 'quit', 'exit']:
                    break

                if not line or line.startswith('#'):
                    continue

                signal = parse_signal(line)
                yield signal

            except EOFError:
                break
            except ValueError as e:
                print(f"Error: {str(e)}")
                print("Format: w1,f1,t1,r1,a1,d1")

    @staticmethod
    def read_list(signals: List[str]) -> Generator[Signal, None, None]:
        """
        Czyta sygnały z listy stringów

        Args:
            signals: Lista stringów w formacie CSV

        Yields:
            Signal: Kolejne sygnały
        """
        for i, sig_str in enumerate(signals):
            try:
                signal = parse_signal(sig_str)
                yield signal
            except ValueError as e:
                raise ValueError(
                    f"Invalid signal at index {i}: {sig_str}\n"
                    f"Error: {str(e)}"
                ) from e


class StreamProcessor:
    """
    Procesor strumienia sygnałów

    Główny komponent do przetwarzania sygnałów w czasie rzeczywistym.

    Użycie:
        processor = StreamProcessor(rules_db)
        result = processor.process_file("signals.txt")
        print(f"Processed {result.total_signals} signals")
    """

    def __init__(
        self,
        rules_db: RulesDatabase,
        on_signal: Optional[Callable[[Signal, ThreatAssessment], None]] = None,
        debug: bool = False
    ):
        """
        Inicjalizacja processora

        Args:
            rules_db: Baza reguł zagrożeń
            on_signal: Callback wywoływany dla każdego sygnału
            debug: Tryb debug
        """
        self.rules_db = rules_db
        self.matcher = ThreatMatcher(rules_db, debug=debug)
        self.on_signal = on_signal
        self.debug = debug

    def process_file(
        self,
        file_path: str | Path,
        skip_comments: bool = True
    ) -> ProcessingResult:
        """
        Przetwarza plik z sygnałami

        Args:
            file_path: Ścieżka do pliku
            skip_comments: Czy pomijać komentarze

        Returns:
            ProcessingResult: Wynik przetwarzania
        """
        import time
        start_time = time.time()

        assessments = []
        errors = []
        total = 0

        try:
            for signal in SignalReader.read_file(file_path, skip_comments):
                total += 1
                try:
                    assessment = self.matcher.assess_threat(signal)
                    assessments.append(assessment)

                    # Wywołaj callback jeśli jest
                    if self.on_signal:
                        self.on_signal(signal, assessment)

                except Exception as e:
                    error_msg = f"Error processing signal {total}: {str(e)}"
                    errors.append(error_msg)
                    if self.debug:
                        print(f"[ERROR] {error_msg}")

        except Exception as e:
            errors.append(f"Fatal error: {str(e)}")

        processing_time = time.time() - start_time

        return ProcessingResult(
            total_signals=total,
            assessments=assessments,
            errors=errors,
            processing_time=processing_time
        )

    def process_stream(
        self,
        signals: Generator[Signal, None, None]
    ) -> ProcessingResult:
        """
        Przetwarza dowolny strumień sygnałów

        Args:
            signals: Generator sygnałów

        Returns:
            ProcessingResult: Wynik przetwarzania
        """
        import time
        start_time = time.time()

        assessments = []
        errors = []
        total = 0

        try:
            for signal in signals:
                total += 1
                try:
                    assessment = self.matcher.assess_threat(signal)
                    assessments.append(assessment)

                    if self.on_signal:
                        self.on_signal(signal, assessment)

                except Exception as e:
                    error_msg = f"Error processing signal {total}: {str(e)}"
                    errors.append(error_msg)

        except Exception as e:
            errors.append(f"Fatal error: {str(e)}")

        processing_time = time.time() - start_time

        return ProcessingResult(
            total_signals=total,
            assessments=assessments,
            errors=errors,
            processing_time=processing_time
        )

    def process_interactive(self) -> ProcessingResult:
        """
        Tryb interaktywny - czytanie ze stdin

        Returns:
            ProcessingResult: Wynik przetwarzania
        """
        return self.process_stream(SignalReader.read_stdin())


# ============================================================================
# Funkcje pomocnicze
# ============================================================================

def process_signals_file(
    file_path: str | Path,
    rules_db: RulesDatabase,
    on_signal: Optional[Callable[[Signal, ThreatAssessment], None]] = None
) -> ProcessingResult:
    """
    Szybkie przetwarzanie pliku z sygnałami

    Args:
        file_path: Ścieżka do pliku
        rules_db: Baza reguł
        on_signal: Opcjonalny callback

    Returns:
        ProcessingResult: Wynik przetwarzania

    Przykład:
        rules = parse_rules_file("data/rules.txt")
        result = process_signals_file("signals.txt", rules)
        print(f"Processed: {result.total_signals}")
    """
    processor = StreamProcessor(rules_db, on_signal=on_signal)
    return processor.process_file(file_path)

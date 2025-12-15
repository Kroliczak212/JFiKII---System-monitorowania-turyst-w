"""
Threat Matcher - dopasowanie sygnałów do reguł zagrożeń

Ten moduł łączy sygnały wejściowe z regułami i określa poziom zagrożenia.

Algorytm (zgodny z artykułem):
1. Pobierz sygnał (warunki + poziom trudności szlaku)
2. Dla każdego poziomu zagrożenia (E5, E4, E3, E2, E1) - od najwyższego:
   a. Pobierz regułę dla poziomu trudności z sygnału
   b. Ewaluuj wyrażenie logiczne
   c. Jeśli TRUE -> zwróć ten poziom zagrożenia
3. Jeśli żaden nie pasuje -> E1 (bezpiecznie)
"""

from dataclasses import dataclass
from typing import List, Optional, Tuple

from src.parser.models import (
    RulesDatabase,
    ThreatLevel,
    DifficultyLevel,
    DifficultyRule,
    LogicalExpression,
)
from .signal import Signal, DifficultySignal
from .logic_evaluator import LogicEvaluator


@dataclass
class ThreatAssessment:
    """
    Wynik oceny zagrożenia

    Attributes:
        threat_level: Określony poziom zagrożenia (E1-E5)
        matched_rule: Reguła która została dopasowana
        signal: Sygnał wejściowy
        evaluation_result: Wynik ewaluacji (True/False)
        matching_atoms: Atomy które spowodowały dopasowanie
        evaluation_trace: Trace ewaluacji (opcjonalnie)
    """
    threat_level: ThreatLevel
    matched_rule: DifficultyRule
    signal: Signal
    evaluation_result: bool
    matching_atoms: List[str]
    evaluation_trace: Optional[List[str]] = None

    @property
    def is_safe(self) -> bool:
        """Czy sytuacja jest bezpieczna (E1 lub E2)"""
        return self.threat_level in [ThreatLevel.E1, ThreatLevel.E2]

    @property
    def requires_monitoring(self) -> bool:
        """Czy wymaga monitorowania (E2+)"""
        return self.threat_level != ThreatLevel.E1

    @property
    def is_dangerous(self) -> bool:
        """Czy jest niebezpiecznie (E4+)"""
        return self.threat_level in [ThreatLevel.E4, ThreatLevel.E5]

    @property
    def is_critical(self) -> bool:
        """Czy jest krytycznie (E5)"""
        return self.threat_level == ThreatLevel.E5

    def __str__(self) -> str:
        """Czytelna reprezentacja"""
        return (
            f"ThreatAssessment(\n"
            f"  Level: {self.threat_level.value} - {self.threat_level.description}\n"
            f"  Rule: {self.matched_rule}\n"
            f"  Signal: {self.signal}\n"
            f"  Result: {self.evaluation_result}\n"
            f"  Matching atoms: {', '.join(self.matching_atoms) if self.matching_atoms else 'none'}\n"
            f")"
        )


class ThreatMatcher:
    """
    Matcher łączący sygnały z regułami

    Użycie:
        matcher = ThreatMatcher(rules_db)
        signal = Signal(...)
        assessment = matcher.assess_threat(signal)
        print(f"Threat level: {assessment.threat_level.value}")
    """

    def __init__(self, rules_db: RulesDatabase, debug: bool = False):
        """
        Inicjalizacja matchera

        Args:
            rules_db: Baza reguł z parsera
            debug: Czy wypisywać debug info
        """
        self.rules_db = rules_db
        self.evaluator = LogicEvaluator(debug=debug)
        self.debug = debug

    def assess_threat(
        self,
        signal: Signal,
        include_trace: bool = False
    ) -> ThreatAssessment:
        """
        Ocenia poziom zagrożenia dla danego sygnału

        Algorytm:
        1. Mapuj signal.difficulty na DifficultyLevel
        2. Sprawdzaj poziomy od E5 do E1 (od najwyższego)
        3. Dla każdego poziomu:
           - Pobierz regułę dla danej trudności
           - Ewaluuj wyrażenie
           - Jeśli TRUE -> zwróć ten poziom
        4. Jeśli nic nie pasuje -> E1 (default safe)

        Args:
            signal: Sygnał wejściowy
            include_trace: Czy dołączyć trace ewaluacji

        Returns:
            ThreatAssessment: Wynik oceny zagrożenia
        """
        # Mapuj DifficultySignal na DifficultyLevel
        difficulty_map = {
            DifficultySignal.D1: DifficultyLevel.D1,
            DifficultySignal.D2: DifficultyLevel.D2,
            DifficultySignal.D3: DifficultyLevel.D3,
            DifficultySignal.D4: DifficultyLevel.D4,
        }
        difficulty = difficulty_map[signal.difficulty]

        # Sprawdzaj poziomy od najwyższego do najniższego
        # Zgodnie z logiką SAT: S ⊨ A (sytuacja pociąga alert)
        threat_levels_ordered = [
            ThreatLevel.E5,
            ThreatLevel.E4,
            ThreatLevel.E3,
            ThreatLevel.E2,
            ThreatLevel.E1,
        ]

        for threat_level in threat_levels_ordered:
            block = self.rules_db.get_block(threat_level)
            if not block:
                continue

            rule = block.get_rule(difficulty)
            if not rule:
                continue

            if self.debug:
                print(f"\nChecking {threat_level.value}.{difficulty.value}:")
                print(f"  Rule: {rule.expression.to_simple_string()}")

            # Ewaluuj wyrażenie
            if include_trace:
                result, trace = self.evaluator.evaluate_with_trace(
                    rule.expression, signal
                )
            else:
                result = self.evaluator.evaluate(rule.expression, signal)
                trace = None

            if self.debug:
                print(f"  Result: {result}")

            # Jeśli wyrażenie jest TRUE, zwróć ten poziom zagrożenia
            if result:
                matching_atoms = self.evaluator.get_matching_atoms(
                    rule.expression, signal
                )

                assessment = ThreatAssessment(
                    threat_level=threat_level,
                    matched_rule=rule,
                    signal=signal,
                    evaluation_result=result,
                    matching_atoms=matching_atoms,
                    evaluation_trace=trace,
                )

                if self.debug:
                    print(f"  MATCHED! Threat level: {threat_level.value}")

                return assessment

        # Nie powinno się tu nigdy dostać, bo E1 ma "others" (zawsze FALSE)
        # Ale dla bezpieczeństwa zwracamy E1
        e1_block = self.rules_db.get_block(ThreatLevel.E1)
        e1_rule = e1_block.get_rule(difficulty) if e1_block else None

        return ThreatAssessment(
            threat_level=ThreatLevel.E1,
            matched_rule=e1_rule,
            signal=signal,
            evaluation_result=False,
            matching_atoms=[],
            evaluation_trace=None,
        )

    def assess_multiple(
        self,
        signals: List[Signal],
        include_trace: bool = False
    ) -> List[ThreatAssessment]:
        """
        Ocenia zagrożenie dla wielu sygnałów

        Args:
            signals: Lista sygnałów
            include_trace: Czy dołączyć trace

        Returns:
            List[ThreatAssessment]: Lista ocen
        """
        return [self.assess_threat(sig, include_trace) for sig in signals]

    def get_statistics(self, assessments: List[ThreatAssessment]) -> dict:
        """
        Generuje statystyki dla listy ocen

        Args:
            assessments: Lista ocen zagrożenia

        Returns:
            dict: Statystyki (liczba na każdym poziomie, etc.)
        """
        stats = {
            "total": len(assessments),
            "by_level": {
                "E5": 0,
                "E4": 0,
                "E3": 0,
                "E2": 0,
                "E1": 0,
            },
            "safe": 0,        # E1, E2
            "monitoring": 0,  # E2+
            "dangerous": 0,   # E4, E5
            "critical": 0,    # E5
        }

        for assessment in assessments:
            level = assessment.threat_level.value
            stats["by_level"][level] += 1

            if assessment.is_safe:
                stats["safe"] += 1
            if assessment.requires_monitoring:
                stats["monitoring"] += 1
            if assessment.is_dangerous:
                stats["dangerous"] += 1
            if assessment.is_critical:
                stats["critical"] += 1

        return stats


# ============================================================================
# Funkcje pomocnicze
# ============================================================================

def assess_threat(
    signal: Signal,
    rules_db: RulesDatabase,
    debug: bool = False
) -> ThreatAssessment:
    """
    Szybka ocena zagrożenia

    Args:
        signal: Sygnał wejściowy
        rules_db: Baza reguł
        debug: Debug mode

    Returns:
        ThreatAssessment: Wynik oceny

    Przykład:
        signal = parse_signal("w2,f3,t1,r2,a1,d3")
        rules = parse_rules_file("data/rules.txt")
        assessment = assess_threat(signal, rules)
        print(assessment.threat_level.value)  # E4
    """
    matcher = ThreatMatcher(rules_db, debug=debug)
    return matcher.assess_threat(signal)

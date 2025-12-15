"""
Model sygnału wejściowego - warunki w czasie rzeczywistym

Signal reprezentuje aktualny stan warunków dla konkretnego turysty:
- Warunki pogodowe (wiatr, mgła, temperatura, deszcz)
- Zagrożenie lawinowe
- Poziom trudności szlaku
"""

from dataclasses import dataclass
from typing import Optional
from enum import Enum


class SignalValue(str, Enum):
    """Bazowa klasa dla wszystkich wartości sygnałów"""
    pass


class WindSignal(SignalValue):
    """Sygnał wiatru - rosnące trudności"""
    W1 = "w1"  # Normalny wiatr
    W2 = "w2"  # Silny wiatr
    W3 = "w3"  # Bardzo silny wiatr


class FogSignal(SignalValue):
    """Sygnał mgły - rosnące trudności widoczności"""
    F1 = "f1"  # Lekka mgła
    F2 = "f2"  # Średnia mgła
    F3 = "f3"  # Gęsta mgła (bardzo słaba widoczność)


class TemperatureSignal(SignalValue):
    """Sygnał temperatury - rosnące trudności"""
    T1 = "t1"  # Normalna temperatura
    T2 = "t2"  # Niska temperatura
    T3 = "t3"  # Bardzo niska temperatura (ekstremalne warunki)


class RainSignal(SignalValue):
    """Sygnał deszczu/burzy - rosnące trudności"""
    R1 = "r1"  # Lekki deszcz
    R2 = "r2"  # Średni deszcz
    R3 = "r3"  # Silny deszcz/burza


class AvalancheSignal(SignalValue):
    """Sygnał zagrożenia lawinowego - rosnące niebezpieczeństwo"""
    A1 = "a1"  # Minimalne zagrożenie
    A2 = "a2"  # Niskie zagrożenie
    A3 = "a3"  # Średnie zagrożenie
    A4 = "a4"  # Wysokie zagrożenie
    A5 = "a5"  # Bardzo wysokie zagrożenie


class DifficultySignal(SignalValue):
    """Poziom trudności szlaku"""
    D1 = "d1"  # Łatwy szlak
    D2 = "d2"  # Średnio trudny szlak
    D3 = "d3"  # Trudny szlak
    D4 = "d4"  # Bardzo trudny szlak


@dataclass
class Signal:
    """
    Sygnał wejściowy reprezentujący aktualne warunki

    Attributes:
        wind: Poziom wiatru (w1-w3)
        fog: Poziom mgły (f1-f3)
        temperature: Poziom temperatury (t1-t3)
        rain: Poziom deszczu (r1-r3)
        avalanche: Zagrożenie lawinowe (a1-a5)
        difficulty: Poziom trudności szlaku (d1-d4)
        timestamp: Opcjonalny timestamp (dla streamingu)
        tourist_id: Opcjonalny ID turysty (dla trackingu)

    Przykład:
        signal = Signal(
            wind=WindSignal.W2,
            fog=FogSignal.F3,
            temperature=TemperatureSignal.T1,
            rain=RainSignal.R2,
            avalanche=AvalancheSignal.A1,
            difficulty=DifficultySignal.D3
        )
    """
    wind: WindSignal
    fog: FogSignal
    temperature: TemperatureSignal
    rain: RainSignal
    avalanche: AvalancheSignal
    difficulty: DifficultySignal
    timestamp: Optional[str] = None
    tourist_id: Optional[str] = None

    def __str__(self) -> str:
        """Czytelna reprezentacja sygnału"""
        parts = [
            f"Wind={self.wind.value}",
            f"Fog={self.fog.value}",
            f"Temp={self.temperature.value}",
            f"Rain={self.rain.value}",
            f"Avalanche={self.avalanche.value}",
            f"Trail={self.difficulty.value}"
        ]
        return f"Signal({', '.join(parts)})"

    def to_dict(self) -> dict:
        """Konwersja do słownika"""
        return {
            "wind": self.wind.value,
            "fog": self.fog.value,
            "temperature": self.temperature.value,
            "rain": self.rain.value,
            "avalanche": self.avalanche.value,
            "difficulty": self.difficulty.value,
            "timestamp": self.timestamp,
            "tourist_id": self.tourist_id,
        }

    def get_value(self, atom: str) -> bool:
        """
        Sprawdza czy dany atom jest TRUE dla tego sygnału

        Args:
            atom: Atom do sprawdzenia (np. "w2", "f3", "others")

        Returns:
            bool: True jeśli atom jest aktywny w sygnale

        Przykład:
            signal = Signal(wind=WindSignal.W2, ...)
            signal.get_value("w2")  # True
            signal.get_value("w3")  # False
        """
        # "others" jest specjalnym tokenem dla reguł E1 (catch-all)
        # Zwraca False, bo E1 jest przypisywany jako fallback w assess_threat()
        # gdy żaden wyższy poziom (E5-E2) nie pasuje do sygnału.
        # To NIE jest błąd - to zamierzone zachowanie zgodne z artykułem źródłowym.
        # Zobacz: PROJEKT.md sekcja 5.6 "Semantyka tokenu others"
        if atom == "others":
            return False

        # Sprawdź każdą wartość sygnału
        return atom in [
            self.wind.value,
            self.fog.value,
            self.temperature.value,
            self.rain.value,
            self.avalanche.value,
            # difficulty nie jest sprawdzane w wyrażeniu, tylko używane do wyboru reguły
        ]

    @classmethod
    def from_string(cls, line: str) -> 'Signal':
        """
        Parsuje sygnał z formatu CSV

        Format: w2,f3,t1,r2,a1,d3
        lub z timestampem: w2,f3,t1,r2,a1,d3,2025-01-17T10:30:00
        lub z ID: w2,f3,t1,r2,a1,d3,2025-01-17T10:30:00,tourist_123

        Args:
            line: String w formacie CSV

        Returns:
            Signal: Sparsowany sygnał

        Raises:
            ValueError: Jeśli format jest niepoprawny
        """
        parts = [p.strip() for p in line.strip().split(',')]

        if len(parts) < 6:
            raise ValueError(
                f"Invalid signal format. Expected at least 6 values (w,f,t,r,a,d), got {len(parts)}"
            )

        try:
            signal = cls(
                wind=WindSignal(parts[0]),
                fog=FogSignal(parts[1]),
                temperature=TemperatureSignal(parts[2]),
                rain=RainSignal(parts[3]),
                avalanche=AvalancheSignal(parts[4]),
                difficulty=DifficultySignal(parts[5]),
                timestamp=parts[6] if len(parts) > 6 else None,
                tourist_id=parts[7] if len(parts) > 7 else None,
            )
            return signal
        except ValueError as e:
            raise ValueError(f"Invalid signal value in '{line}': {str(e)}") from e

    @classmethod
    def from_dict(cls, data: dict) -> 'Signal':
        """
        Tworzy sygnał ze słownika

        Args:
            data: Słownik z wartościami sygnału

        Returns:
            Signal: Nowy sygnał
        """
        return cls(
            wind=WindSignal(data['wind']),
            fog=FogSignal(data['fog']),
            temperature=TemperatureSignal(data['temperature']),
            rain=RainSignal(data['rain']),
            avalanche=AvalancheSignal(data['avalanche']),
            difficulty=DifficultySignal(data['difficulty']),
            timestamp=data.get('timestamp'),
            tourist_id=data.get('tourist_id'),
        )


# ============================================================================
# Funkcje pomocnicze
# ============================================================================

def parse_signal(text: str) -> Signal:
    """
    Szybkie parsowanie sygnału z stringa

    Args:
        text: String w formacie CSV

    Returns:
        Signal: Sparsowany sygnał

    Przykład:
        signal = parse_signal("w2,f3,t1,r2,a1,d3")
    """
    return Signal.from_string(text)

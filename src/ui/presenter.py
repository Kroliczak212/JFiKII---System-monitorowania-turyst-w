"""
Presenter - formatowanie i wyświetlanie wyników

Ten moduł formatuje wyniki oceny zagrożenia w czytelny sposób.
Używa biblioteki Rich do pięknego formatowania CLI.
"""

import sys
from pathlib import Path
from typing import List, Optional

from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.tree import Tree
from rich.text import Text
from rich.columns import Columns

sys.path.insert(0, str(Path(__file__).parent.parent))
from evaluator.threat_matcher import ThreatAssessment
from evaluator.signal import Signal
from parser.models import ThreatLevel


class ThreatPresenter:
    """
    Presenter wyników oceny zagrożenia

    Formatuje wyniki w piękny, czytelny sposób używając Rich.

    Użycie:
        presenter = ThreatPresenter()
        presenter.show_assessment(assessment)
    """

    # Mapowanie poziomów na kolory
    COLOR_MAP = {
        "E1": "green",
        "E2": "yellow",
        "E3": "orange1",
        "E4": "red",
        "E5": "white on red bold",
    }

    # Mapowanie poziomów na symbole (bez unicode dla Windows)
    SYMBOL_MAP = {
        "E1": "[OK]",
        "E2": "[!]",
        "E3": "[!!]",
        "E4": "[!!!]",
        "E5": "[X]",
    }

    # Pełne opisy poziomów
    DESCRIPTIONS = {
        "E1": "Nothing alarming happens, normal monitoring",
        "E2": "Partially disadvantageous conditions, requires the assessment of a local or temporary threat, monitoring",
        "E3": "Existence of risky situations, possibility of sending a drone, including a BTS-drone, in order to obtain more precise data, intensified monitoring",
        "E4": "Dangerous situations, can cause serious threat and needs to be constantly monitored, climbing only allowed for experienced hikers, possibility of sending a drone, including a camera-drone, in order to obtain more precise data, possibility of an emergency operation, decision about intervention made in a command centre",
        "E5": "Walking is impossible, emergency action is necessary, tourists entering the routes is strictly forbidden",
    }

    # Rekomendacje
    RECOMMENDATIONS = {
        "E1": [
            "Warunki bezpieczne",
            "Standardowy monitoring",
            "Mozna kontynuowac wycieczke",
        ],
        "E2": [
            "Zwiekszony monitoring",
            "Ocena lokalnego zagrozenia",
            "Zachowaj ostroznosc",
        ],
        "E3": [
            "Ryzykowne warunki",
            "Zintensyfikowany monitoring",
            "Mozliwosc wyslania drona (BTS)",
            "Rozważ zawrocenie",
        ],
        "E4": [
            "NIEBEZPIECZNE WARUNKI",
            "Stalymmonitoring wymagany",
            "Tylko doswiadczeni turyści",
            "Mozliwosc wyslania drona (kamera)",
            "Gotowy do operacji ratunkowej",
            "Decyzja w centrum dowodzenia",
        ],
        "E5": [
            "!!! ZAKAZ WSTEPU !!!",
            "Kontynuacja niemozliwa",
            "Konieczna akcja ratunkowa",
            "Natychmiastowa ewakuacja",
        ],
    }

    def __init__(self, console: Optional[Console] = None):
        """
        Inicjalizacja presentera

        Args:
            console: Opcjonalnie własna instancja Console
        """
        self.console = console or Console()

    def show_assessment(
        self,
        assessment: ThreatAssessment,
        show_trace: bool = False,
        show_recommendations: bool = True
    ):
        """
        Wyświetla szczegółową ocenę zagrożenia

        Args:
            assessment: Ocena zagrożenia do wyświetlenia
            show_trace: Czy pokazać trace ewaluacji
            show_recommendations: Czy pokazać rekomendacje
        """
        level = assessment.threat_level.value
        color = self.COLOR_MAP[level]
        symbol = self.SYMBOL_MAP[level]

        # Panel główny z poziomem zagrożenia
        title = f"[{color}]{symbol} THREAT LEVEL: {level}[/{color}]"

        # Zawartość jako lista stringów
        parts = []

        # 1. Aktualne warunki
        parts.append("[bold]Current Conditions:[/bold]")
        parts.append(f"  [cyan]Wind:[/cyan]        {assessment.signal.wind.value} (Increasingly difficult)")
        parts.append(f"  [cyan]Fog:[/cyan]         {assessment.signal.fog.value} (Difficult weather)")
        parts.append(f"  [cyan]Temperature:[/cyan] {assessment.signal.temperature.value} (Increasingly difficult)")
        parts.append(f"  [cyan]Rain:[/cyan]        {assessment.signal.rain.value} (Difficult weather)")
        parts.append(f"  [cyan]Avalanche:[/cyan]   {assessment.signal.avalanche.value} (Threat level)")
        parts.append(f"  [cyan]Trail:[/cyan]       {assessment.signal.difficulty.value} (Difficulty)")
        parts.append("")

        # 2. Dopasowane warunki
        if assessment.matching_atoms:
            parts.append("[bold]Matched Conditions:[/bold]")
            matched_text = ", ".join(
                f"[{color}]{atom}[/{color}]" for atom in assessment.matching_atoms
            )
            parts.append(f"  {matched_text}")
            parts.append("")

        # 3. Opis poziomu
        parts.append("[bold]Description:[/bold]")
        parts.append(self.DESCRIPTIONS[level])
        parts.append("")

        # 4. Rekomendacje
        if show_recommendations:
            parts.append(f"[bold {color}]Recommendations:[/bold {color}]")
            for rec in self.RECOMMENDATIONS[level]:
                parts.append(f"  - {rec}")

        # Utwórz panel
        panel = Panel(
            "\n".join(parts),
            title=title,
            border_style=color,
            padding=(1, 2)
        )

        self.console.print(panel)

        # 5. Trace ewaluacji (opcjonalnie)
        if show_trace and assessment.evaluation_trace:
            self.console.print("\n[bold]Evaluation Trace:[/bold]")
            for step in assessment.evaluation_trace:
                self.console.print(f"  {step}")

    def show_compact(self, assessment: ThreatAssessment):
        """
        Wyświetla kompaktową wersję oceny (jedna linia)

        Args:
            assessment: Ocena zagrożenia
        """
        level = assessment.threat_level.value
        color = self.COLOR_MAP[level]
        symbol = self.SYMBOL_MAP[level]

        # Format: [E5] w=w3 f=f3 t=t3 -> CRITICAL
        signal = assessment.signal
        signal_str = (
            f"w={signal.wind.value} "
            f"f={signal.fog.value} "
            f"t={signal.temperature.value} "
            f"r={signal.rain.value} "
            f"a={signal.avalanche.value} "
            f"d={signal.difficulty.value}"
        )

        self.console.print(
            f"[{color}]{symbol} {level}[/{color}] {signal_str}"
        )

    def show_multiple(
        self,
        assessments: List[ThreatAssessment],
        show_statistics: bool = True
    ):
        """
        Wyświetla wiele ocen w formie tabeli

        Args:
            assessments: Lista ocen
            show_statistics: Czy pokazać statystyki
        """
        table = Table(title="Threat Assessment Results", show_lines=True)

        table.add_column("#", justify="right", style="dim")
        table.add_column("Level", justify="center")
        table.add_column("Conditions")
        table.add_column("Matched")

        for i, assessment in enumerate(assessments, 1):
            level = assessment.threat_level.value
            color = self.COLOR_MAP[level]
            symbol = self.SYMBOL_MAP[level]

            signal = assessment.signal
            conditions = (
                f"w={signal.wind.value} "
                f"f={signal.fog.value} "
                f"t={signal.temperature.value} "
                f"r={signal.rain.value} "
                f"a={signal.avalanche.value} "
                f"d={signal.difficulty.value}"
            )

            matched = ", ".join(assessment.matching_atoms) if assessment.matching_atoms else "-"

            table.add_row(
                str(i),
                f"[{color}]{symbol} {level}[/{color}]",
                f"[dim]{conditions}[/dim]",
                f"[cyan]{matched}[/cyan]"
            )

        self.console.print(table)

        # Statystyki
        if show_statistics:
            self.show_statistics(assessments)

    def show_statistics(self, assessments: List[ThreatAssessment]):
        """
        Wyświetla statystyki dla listy ocen

        Args:
            assessments: Lista ocen zagrożenia
        """
        from evaluator.threat_matcher import ThreatMatcher
        matcher = ThreatMatcher(None)  # Only for statistics
        stats = matcher.get_statistics(assessments)

        self.console.print("\n[bold cyan]Statistics[/bold cyan]\n")

        # Tabela dystrybucji
        table = Table(show_header=True)
        table.add_column("Level", style="bold")
        table.add_column("Count", justify="right")
        table.add_column("Percentage", justify="right")

        total = stats["total"]
        for level in ["E5", "E4", "E3", "E2", "E1"]:
            count = stats["by_level"][level]
            percentage = (count / total * 100) if total > 0 else 0
            color = self.COLOR_MAP[level]

            table.add_row(
                f"[{color}]{level}[/{color}]",
                str(count),
                f"{percentage:.1f}%"
            )

        self.console.print(table)

        # Podsumowanie
        self.console.print(f"\nTotal signals: {total}")
        self.console.print(f"[green]Safe (E1-E2): {stats['safe']}[/green]")
        self.console.print(f"[orange1]Monitoring (E2+): {stats['monitoring']}[/orange1]")
        self.console.print(f"[red]Dangerous (E4-E5): {stats['dangerous']}[/red]")
        self.console.print(f"[white on red]Critical (E5): {stats['critical']}[/white on red]")


# ============================================================================
# Funkcje pomocnicze
# ============================================================================

def show_assessment(assessment: ThreatAssessment, detailed: bool = True):
    """
    Szybkie wyświetlenie oceny

    Args:
        assessment: Ocena do wyświetlenia
        detailed: Czy pokazać szczegóły (True) czy kompakt (False)
    """
    presenter = ThreatPresenter()
    if detailed:
        presenter.show_assessment(assessment)
    else:
        presenter.show_compact(assessment)


def show_multiple_assessments(assessments: List[ThreatAssessment]):
    """
    Szybkie wyświetlenie wielu ocen

    Args:
        assessments: Lista ocen
    """
    presenter = ThreatPresenter()
    presenter.show_multiple(assessments)

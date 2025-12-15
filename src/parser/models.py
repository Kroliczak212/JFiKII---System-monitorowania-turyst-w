"""
Modele danych reprezentujące reguły zagrożeń

Te klasy reprezentują sparsowane reguły w formie łatwej do użycia.
Struktura odpowiada hierarchii z Tabeli 5.
"""

from dataclasses import dataclass
from typing import List, Dict, Optional
from enum import Enum


class ThreatLevel(Enum):
    """Poziomy zagrożenia (E1-E5)"""
    E1 = "E1"  # Niskie (zielony)
    E2 = "E2"  # Średnie (żółty)
    E3 = "E3"  # Podwyższone (pomarańczowy)
    E4 = "E4"  # Wysokie (czerwony)
    E5 = "E5"  # Krytyczne (czarny)

    @property
    def color(self) -> str:
        """Zwraca kolor dla poziomu zagrożenia"""
        colors = {
            "E1": "green",
            "E2": "yellow",
            "E3": "orange",
            "E4": "red",
            "E5": "black",
        }
        return colors[self.value]

    @property
    def description(self) -> str:
        """Zwraca opis poziomu zagrożenia"""
        descriptions = {
            "E1": "Nothing alarming happens, normal monitoring",
            "E2": "Partially disadvantageous conditions, requires assessment of local or temporary threat, monitoring",
            "E3": "Existence of risky situations, possibility of sending a drone, intensified monitoring",
            "E4": "Dangerous situations, constantly monitored, climbing only for experienced hikers, possible drone deployment",
            "E5": "Walking is impossible, emergency action is necessary, tourists entering the routes is strictly forbidden",
        }
        return descriptions[self.value]


class DifficultyLevel(Enum):
    """Poziomy trudności szlaku (d1-d4)"""
    D1 = "d1"  # Łatwy
    D2 = "d2"  # Średni
    D3 = "d3"  # Trudny
    D4 = "d4"  # Bardzo trudny

    @property
    def description(self) -> str:
        """Zwraca opis poziomu trudności"""
        descriptions = {
            "d1": "Easy trail",
            "d2": "Medium difficulty trail",
            "d3": "Difficult trail",
            "d4": "Very difficult trail",
        }
        return descriptions[self.value]


class LogicalOperator(Enum):
    """Operatory logiczne"""
    OR = "|"   # Alternatywa
    AND = "&"  # Koniunkcja
    NOT = "!"  # Negacja


@dataclass
class LogicalExpression:
    """
    Reprezentacja wyrażenia logicznego (AST)

    Może być:
    - Atom (zmienna): operator=None, left=string, right=None
    - Operacja binarna (OR/AND): operator=OR/AND, left=Expression, right=Expression
    - Operacja unarna (NOT): operator=NOT, left=Expression, right=None
    """
    operator: Optional[LogicalOperator]
    left: 'LogicalExpression | str'
    right: Optional['LogicalExpression'] = None

    def __str__(self) -> str:
        """Czytelna reprezentacja tekstowa"""
        if self.operator is None:
            # Atom
            return str(self.left)
        elif self.operator == LogicalOperator.NOT:
            # Negacja
            return f"!{self.left}"
        else:
            # OR lub AND
            return f"({self.left} {self.operator.value} {self.right})"

    def to_simple_string(self) -> str:
        """Uproszczona reprezentacja bez nadmiarowych nawiasów"""
        if self.operator is None:
            return str(self.left)
        elif self.operator == LogicalOperator.NOT:
            if isinstance(self.left, LogicalExpression):
                return f"!({self.left.to_simple_string()})"
            return f"!{self.left}"
        else:
            left_str = self.left.to_simple_string() if isinstance(self.left, LogicalExpression) else str(self.left)
            right_str = self.right.to_simple_string() if isinstance(self.right, LogicalExpression) else str(self.right)
            return f"{left_str} {self.operator.value} {right_str}"


@dataclass
class DifficultyRule:
    """
    Reguła dla konkretnego poziomu trudności

    Przykład: d4: (w2 | w3) | (f2 | f3)
    """
    difficulty: DifficultyLevel
    expression: LogicalExpression

    def __str__(self) -> str:
        return f"{self.difficulty.value}: {self.expression.to_simple_string()}"


@dataclass
class ThreatBlock:
    """
    Blok zagrożenia zawierający reguły dla wszystkich poziomów trudności

    Przykład:
    E5 {
      d4: ...;
      d3: ...;
      d2: ...;
      d1: ...;
    }
    """
    threat_level: ThreatLevel
    rules: Dict[DifficultyLevel, DifficultyRule]

    def get_rule(self, difficulty: DifficultyLevel) -> Optional[DifficultyRule]:
        """Zwraca regułę dla danego poziomu trudności"""
        return self.rules.get(difficulty)

    def __str__(self) -> str:
        rules_str = "\n  ".join(str(rule) for rule in self.rules.values())
        return f"{self.threat_level.value} {{\n  {rules_str}\n}}"


@dataclass
class RulesDatabase:
    """
    Baza danych wszystkich reguł

    Zawiera wszystkie bloki zagrożeń (E1-E5)
    """
    blocks: Dict[ThreatLevel, ThreatBlock]

    def get_block(self, threat_level: ThreatLevel) -> Optional[ThreatBlock]:
        """Zwraca blok dla danego poziomu zagrożenia"""
        return self.blocks.get(threat_level)

    def get_rule(self, threat_level: ThreatLevel, difficulty: DifficultyLevel) -> Optional[DifficultyRule]:
        """Zwraca konkretną regułę"""
        block = self.get_block(threat_level)
        if block:
            return block.get_rule(difficulty)
        return None

    def __str__(self) -> str:
        blocks_str = "\n\n".join(str(block) for block in self.blocks.values())
        return f"Rules Database:\n{blocks_str}"

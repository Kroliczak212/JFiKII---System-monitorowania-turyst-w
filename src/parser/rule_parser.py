"""
Parser reguł zagrożeń - publiczne API

Ten moduł dostarcza główną funkcjonalność parsowania reguł.
Ukrywa szczegóły implementacji ANTLR za prostym interfejsem.
"""

import sys
from pathlib import Path
from typing import Optional
from antlr4 import InputStream, CommonTokenStream
from antlr4.error.ErrorListener import ErrorListener

from .generated.ThreatRulesLexer import ThreatRulesLexer
from .generated.ThreatRulesParser import ThreatRulesParser as AntlrParser
from .visitor import RulesBuilder
from .models import RulesDatabase


class ParserError(Exception):
    """Wyjątek rzucany gdy parsowanie się nie powiedzie"""
    pass


class CustomErrorListener(ErrorListener):
    """
    Custom error listener dla ANTLR

    ANTLR domyślnie wypisuje błędy na stderr.
    Ten listener przechwytuje błędy i rzuca wyjątki.
    """

    def __init__(self):
        super().__init__()
        self.errors = []

    def syntaxError(self, recognizer, offendingSymbol, line, column, msg, e):
        """Wywoływane gdy ANTLR znajdzie błąd składniowy"""
        error_msg = f"Line {line}:{column} - {msg}"
        self.errors.append(error_msg)

    def has_errors(self) -> bool:
        """Sprawdza czy wystąpiły błędy"""
        return len(self.errors) > 0

    def get_error_message(self) -> str:
        """Zwraca połączone komunikaty błędów"""
        return "\n".join(self.errors)


class RulesParser:
    """
    Parser reguł zagrożeń

    Użycie:
        parser = RulesParser()
        rules_db = parser.parse_file("data/rules.txt")
        # lub
        rules_db = parser.parse_string("E5 { d4: w3; d3: w3; d2: w3; d1: w3; }")
    """

    def __init__(self):
        """Inicjalizacja parsera"""
        self.error_listener = CustomErrorListener()

    def parse_file(self, file_path: str | Path) -> RulesDatabase:
        """
        Parsuje plik z regułami

        Args:
            file_path: Ścieżka do pliku z regułami (np. "data/rules.txt")

        Returns:
            RulesDatabase: Sparsowane reguły

        Raises:
            FileNotFoundError: Jeśli plik nie istnieje
            ParserError: Jeśli parsowanie się nie powiedzie
        """
        path = Path(file_path)
        if not path.exists():
            raise FileNotFoundError(f"File not found: {path}")

        with open(path, 'r', encoding='utf-8') as f:
            content = f.read()

        return self.parse_string(content)

    def parse_string(self, text: str) -> RulesDatabase:
        """
        Parsuje string z regułami

        Args:
            text: String zawierający reguły w formacie DSL

        Returns:
            RulesDatabase: Sparsowane reguły

        Raises:
            ParserError: Jeśli parsowanie się nie powiedzie
        """
        try:
            # Reset error listener
            self.error_listener = CustomErrorListener()

            # Krok 1: Tokenizacja (Lexer)
            input_stream = InputStream(text)
            lexer = ThreatRulesLexer(input_stream)
            lexer.removeErrorListeners()
            lexer.addErrorListener(self.error_listener)

            # Krok 2: Parsowanie (Parser)
            token_stream = CommonTokenStream(lexer)
            parser = AntlrParser(token_stream)
            parser.removeErrorListeners()
            parser.addErrorListener(self.error_listener)

            # Krok 3: Budowanie drzewa parsowania
            parse_tree = parser.program()

            # Sprawdź czy były błędy składniowe
            if self.error_listener.has_errors():
                raise ParserError(
                    f"Syntax errors found:\n{self.error_listener.get_error_message()}"
                )

            # Krok 4: Budowanie struktur danych (Visitor)
            builder = RulesBuilder()
            rules_db = builder.visit(parse_tree)

            return rules_db

        except ParserError:
            raise
        except Exception as e:
            raise ParserError(f"Unexpected error during parsing: {str(e)}") from e

    def validate_rules(self, rules_db: RulesDatabase) -> bool:
        """
        Walidacja sparsowanych reguł

        Sprawdza czy:
        - Wszystkie poziomy zagrożeń są zdefiniowane (E1-E5)
        - Każdy poziom ma wszystkie 4 reguły (d1-d4)

        Args:
            rules_db: Baza reguł do walidacji

        Returns:
            bool: True jeśli reguły są poprawne

        Raises:
            ParserError: Jeśli reguły są niepoprawne
        """
        from .models import ThreatLevel, DifficultyLevel

        # Sprawdź czy są wszystkie poziomy zagrożeń
        required_levels = {ThreatLevel.E1, ThreatLevel.E2, ThreatLevel.E3,
                          ThreatLevel.E4, ThreatLevel.E5}
        missing_levels = required_levels - set(rules_db.blocks.keys())
        if missing_levels:
            raise ParserError(
                f"Missing threat levels: {', '.join(l.value for l in missing_levels)}"
            )

        # Sprawdź czy każdy blok ma wszystkie poziomy trudności
        required_difficulties = {DifficultyLevel.D1, DifficultyLevel.D2,
                                DifficultyLevel.D3, DifficultyLevel.D4}
        for threat_level, block in rules_db.blocks.items():
            missing_difficulties = required_difficulties - set(block.rules.keys())
            if missing_difficulties:
                raise ParserError(
                    f"Threat level {threat_level.value} missing difficulty levels: "
                    f"{', '.join(d.value for d in missing_difficulties)}"
                )

        return True


# ============================================================================
# Funkcje pomocnicze (convenience functions)
# ============================================================================

def parse_rules_file(file_path: str | Path) -> RulesDatabase:
    """
    Szybkie parsowanie pliku z regułami

    Args:
        file_path: Ścieżka do pliku

    Returns:
        RulesDatabase: Sparsowane reguły

    Przykład:
        rules = parse_rules_file("data/rules.txt")
        block_e5 = rules.get_block(ThreatLevel.E5)
    """
    parser = RulesParser()
    rules_db = parser.parse_file(file_path)
    parser.validate_rules(rules_db)
    return rules_db


def parse_rules_string(text: str) -> RulesDatabase:
    """
    Szybkie parsowanie stringa z regułami

    Args:
        text: String z regułami

    Returns:
        RulesDatabase: Sparsowane reguły
    """
    parser = RulesParser()
    rules_db = parser.parse_string(text)
    parser.validate_rules(rules_db)
    return rules_db

"""
Parser reguł zagrożeń oparty na ANTLR4

Publiczne API:
    parse_rules_file(path) -> RulesDatabase
    parse_rules_string(text) -> RulesDatabase

Modele:
    ThreatLevel, DifficultyLevel, LogicalExpression, ThreatBlock, RulesDatabase
"""

from .rule_parser import (
    parse_rules_file,
    parse_rules_string,
    RulesParser,
    ParserError,
)
from .models import (
    ThreatLevel,
    DifficultyLevel,
    LogicalOperator,
    LogicalExpression,
    DifficultyRule,
    ThreatBlock,
    RulesDatabase,
)

__all__ = [
    # Parser
    'parse_rules_file',
    'parse_rules_string',
    'RulesParser',
    'ParserError',
    # Models
    'ThreatLevel',
    'DifficultyLevel',
    'LogicalOperator',
    'LogicalExpression',
    'DifficultyRule',
    'ThreatBlock',
    'RulesDatabase',
]

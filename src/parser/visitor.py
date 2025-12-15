"""
Custom Visitor do budowania struktur danych z AST

Ten visitor przechodzi po drzewie parsowania wygenerowanym przez ANTLR
i buduje nasze modele danych (ThreatBlock, DifficultyRule, etc.)
"""

from typing import Dict, List

from .generated.ThreatRulesParser import ThreatRulesParser
from .generated.ThreatRulesVisitor import ThreatRulesVisitor
from .models import (
    ThreatLevel,
    DifficultyLevel,
    LogicalOperator,
    LogicalExpression,
    DifficultyRule,
    ThreatBlock,
    RulesDatabase,
)


class RulesBuilder(ThreatRulesVisitor):
    """
    Visitor budujący struktury danych z AST

    ANTLR generuje drzewo parsowania (Parse Tree).
    Ten visitor przechodzi po tym drzewie i buduje nasze obiekty.
    """

    def visitProgram(self, ctx: ThreatRulesParser.ProgramContext) -> RulesDatabase:
        """
        Punkt wejścia - cały program (wszystkie bloki)

        program: threatBlock* EOF
        """
        blocks: Dict[ThreatLevel, ThreatBlock] = {}

        # Przechodzimy przez wszystkie bloki zagrożeń
        for threat_block_ctx in ctx.threatBlock():
            block = self.visit(threat_block_ctx)
            blocks[block.threat_level] = block

        return RulesDatabase(blocks=blocks)

    def visitThreatBlock(self, ctx: ThreatRulesParser.ThreatBlockContext) -> ThreatBlock:
        """
        Blok zagrożenia (np. E5 { ... })

        threatBlock:
            threatLevel LBRACE
                D4 COLON expression SEMICOLON
                D3 COLON expression SEMICOLON
                D2 COLON expression SEMICOLON
                D1 COLON expression SEMICOLON
            RBRACE
        """
        # Pobierz poziom zagrożenia (E1-E5)
        threat_level = self.visit(ctx.threatLevel())

        # Pobierz wszystkie wyrażenia (jest ich dokładnie 4)
        expressions = [self.visit(expr_ctx) for expr_ctx in ctx.expression()]

        # Utwórz reguły dla każdego poziomu trudności
        # Kolejność w gramatyce: d4, d3, d2, d1
        rules = {
            DifficultyLevel.D4: DifficultyRule(DifficultyLevel.D4, expressions[0]),
            DifficultyLevel.D3: DifficultyRule(DifficultyLevel.D3, expressions[1]),
            DifficultyLevel.D2: DifficultyRule(DifficultyLevel.D2, expressions[2]),
            DifficultyLevel.D1: DifficultyRule(DifficultyLevel.D1, expressions[3]),
        }

        return ThreatBlock(threat_level=threat_level, rules=rules)

    def visitThreatLevel(self, ctx: ThreatRulesParser.ThreatLevelContext) -> ThreatLevel:
        """
        Poziom zagrożenia: E5 | E4 | E3 | E2 | E1
        """
        text = ctx.getText()
        return ThreatLevel(text)

    def visitExpression(self, ctx: ThreatRulesParser.ExpressionContext) -> LogicalExpression:
        """
        expression: orExpression
        """
        return self.visit(ctx.orExpression())

    def visitOrExpression(self, ctx: ThreatRulesParser.OrExpressionContext) -> LogicalExpression:
        """
        orExpression: andExpression (OR andExpression)*

        Budujemy drzewo left-associative:
        a | b | c  =>  ((a | b) | c)
        """
        # Pierwszy element
        result = self.visit(ctx.andExpression(0))

        # Jeśli są kolejne elementy po OR
        for i in range(1, len(ctx.andExpression())):
            right = self.visit(ctx.andExpression(i))
            result = LogicalExpression(
                operator=LogicalOperator.OR,
                left=result,
                right=right
            )

        return result

    def visitAndExpression(self, ctx: ThreatRulesParser.AndExpressionContext) -> LogicalExpression:
        """
        andExpression: unaryExpression (AND unaryExpression)*

        Budujemy drzewo left-associative:
        a & b & c  =>  ((a & b) & c)
        """
        # Pierwszy element
        result = self.visit(ctx.unaryExpression(0))

        # Jeśli są kolejne elementy po AND
        for i in range(1, len(ctx.unaryExpression())):
            right = self.visit(ctx.unaryExpression(i))
            result = LogicalExpression(
                operator=LogicalOperator.AND,
                left=result,
                right=right
            )

        return result

    def visitNotExpression(self, ctx: ThreatRulesParser.NotExpressionContext) -> LogicalExpression:
        """
        NOT unaryExpression

        Przykład: !w2, !(w2 | w3)
        """
        inner = self.visit(ctx.unaryExpression())
        return LogicalExpression(
            operator=LogicalOperator.NOT,
            left=inner,
            right=None
        )

    def visitParenExpression(self, ctx: ThreatRulesParser.ParenExpressionContext) -> LogicalExpression:
        """
        LPAREN expression RPAREN

        Nawiasy - po prostu zwracamy zawartość
        """
        return self.visit(ctx.expression())

    def visitAtomExpression(self, ctx: ThreatRulesParser.AtomExpressionContext) -> LogicalExpression:
        """
        atom

        Podstawowa jednostka - zmienna (w2, f3, etc.) lub 'others'
        """
        atom_text = self.visit(ctx.atom())
        return LogicalExpression(
            operator=None,
            left=atom_text,
            right=None
        )

    def visitAtom(self, ctx: ThreatRulesParser.AtomContext) -> str:
        """
        atom: windLevel | fogLevel | tempLevel | rainLevel | avalancheLevel | OTHERS

        Zwraca string z nazwą atomu (np. "w2", "f3", "others")
        """
        return ctx.getText()

    # Pozostałe metody - po prostu zwracają tekst

    def visitWindLevel(self, ctx: ThreatRulesParser.WindLevelContext) -> str:
        return ctx.getText()

    def visitFogLevel(self, ctx: ThreatRulesParser.FogLevelContext) -> str:
        return ctx.getText()

    def visitTempLevel(self, ctx: ThreatRulesParser.TempLevelContext) -> str:
        return ctx.getText()

    def visitRainLevel(self, ctx: ThreatRulesParser.RainLevelContext) -> str:
        return ctx.getText()

    def visitAvalancheLevel(self, ctx: ThreatRulesParser.AvalancheLevelContext) -> str:
        return ctx.getText()

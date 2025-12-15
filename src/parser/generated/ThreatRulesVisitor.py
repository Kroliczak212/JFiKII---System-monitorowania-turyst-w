# Generated from grammar/ThreatRules.g4 by ANTLR 4.13.1
from antlr4 import *
if "." in __name__:
    from .ThreatRulesParser import ThreatRulesParser
else:
    from ThreatRulesParser import ThreatRulesParser

# This class defines a complete generic visitor for a parse tree produced by ThreatRulesParser.

class ThreatRulesVisitor(ParseTreeVisitor):

    # Visit a parse tree produced by ThreatRulesParser#program.
    def visitProgram(self, ctx:ThreatRulesParser.ProgramContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ThreatRulesParser#threatBlock.
    def visitThreatBlock(self, ctx:ThreatRulesParser.ThreatBlockContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ThreatRulesParser#threatLevel.
    def visitThreatLevel(self, ctx:ThreatRulesParser.ThreatLevelContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ThreatRulesParser#expression.
    def visitExpression(self, ctx:ThreatRulesParser.ExpressionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ThreatRulesParser#orExpression.
    def visitOrExpression(self, ctx:ThreatRulesParser.OrExpressionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ThreatRulesParser#andExpression.
    def visitAndExpression(self, ctx:ThreatRulesParser.AndExpressionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ThreatRulesParser#NotExpression.
    def visitNotExpression(self, ctx:ThreatRulesParser.NotExpressionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ThreatRulesParser#ParenExpression.
    def visitParenExpression(self, ctx:ThreatRulesParser.ParenExpressionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ThreatRulesParser#AtomExpression.
    def visitAtomExpression(self, ctx:ThreatRulesParser.AtomExpressionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ThreatRulesParser#atom.
    def visitAtom(self, ctx:ThreatRulesParser.AtomContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ThreatRulesParser#windLevel.
    def visitWindLevel(self, ctx:ThreatRulesParser.WindLevelContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ThreatRulesParser#fogLevel.
    def visitFogLevel(self, ctx:ThreatRulesParser.FogLevelContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ThreatRulesParser#tempLevel.
    def visitTempLevel(self, ctx:ThreatRulesParser.TempLevelContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ThreatRulesParser#rainLevel.
    def visitRainLevel(self, ctx:ThreatRulesParser.RainLevelContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ThreatRulesParser#avalancheLevel.
    def visitAvalancheLevel(self, ctx:ThreatRulesParser.AvalancheLevelContext):
        return self.visitChildren(ctx)



del ThreatRulesParser
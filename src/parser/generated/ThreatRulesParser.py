# Generated from grammar/ThreatRules.g4 by ANTLR 4.13.1
# encoding: utf-8
from antlr4 import *
from io import StringIO
import sys
if sys.version_info[1] > 5:
	from typing import TextIO
else:
	from typing.io import TextIO

def serializedATN():
    return [
        4,1,40,102,2,0,7,0,2,1,7,1,2,2,7,2,2,3,7,3,2,4,7,4,2,5,7,5,2,6,7,
        6,2,7,7,7,2,8,7,8,2,9,7,9,2,10,7,10,2,11,7,11,2,12,7,12,1,0,5,0,
        28,8,0,10,0,12,0,31,9,0,1,0,1,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,
        1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,2,1,2,1,3,1,3,
        1,4,1,4,1,4,5,4,62,8,4,10,4,12,4,65,9,4,1,5,1,5,1,5,5,5,70,8,5,10,
        5,12,5,73,9,5,1,6,1,6,1,6,1,6,1,6,1,6,1,6,3,6,82,8,6,1,7,1,7,1,7,
        1,7,1,7,1,7,3,7,90,8,7,1,8,1,8,1,9,1,9,1,10,1,10,1,11,1,11,1,12,
        1,12,1,12,0,0,13,0,2,4,6,8,10,12,14,16,18,20,22,24,0,6,1,0,1,5,1,
        0,10,12,1,0,13,15,1,0,16,18,1,0,19,21,1,0,22,26,98,0,29,1,0,0,0,
        2,34,1,0,0,0,4,54,1,0,0,0,6,56,1,0,0,0,8,58,1,0,0,0,10,66,1,0,0,
        0,12,81,1,0,0,0,14,89,1,0,0,0,16,91,1,0,0,0,18,93,1,0,0,0,20,95,
        1,0,0,0,22,97,1,0,0,0,24,99,1,0,0,0,26,28,3,2,1,0,27,26,1,0,0,0,
        28,31,1,0,0,0,29,27,1,0,0,0,29,30,1,0,0,0,30,32,1,0,0,0,31,29,1,
        0,0,0,32,33,5,0,0,1,33,1,1,0,0,0,34,35,3,4,2,0,35,36,5,33,0,0,36,
        37,5,6,0,0,37,38,5,35,0,0,38,39,3,6,3,0,39,40,5,36,0,0,40,41,5,7,
        0,0,41,42,5,35,0,0,42,43,3,6,3,0,43,44,5,36,0,0,44,45,5,8,0,0,45,
        46,5,35,0,0,46,47,3,6,3,0,47,48,5,36,0,0,48,49,5,9,0,0,49,50,5,35,
        0,0,50,51,3,6,3,0,51,52,5,36,0,0,52,53,5,34,0,0,53,3,1,0,0,0,54,
        55,7,0,0,0,55,5,1,0,0,0,56,57,3,8,4,0,57,7,1,0,0,0,58,63,3,10,5,
        0,59,60,5,28,0,0,60,62,3,10,5,0,61,59,1,0,0,0,62,65,1,0,0,0,63,61,
        1,0,0,0,63,64,1,0,0,0,64,9,1,0,0,0,65,63,1,0,0,0,66,71,3,12,6,0,
        67,68,5,29,0,0,68,70,3,12,6,0,69,67,1,0,0,0,70,73,1,0,0,0,71,69,
        1,0,0,0,71,72,1,0,0,0,72,11,1,0,0,0,73,71,1,0,0,0,74,75,5,30,0,0,
        75,82,3,12,6,0,76,77,5,31,0,0,77,78,3,6,3,0,78,79,5,32,0,0,79,82,
        1,0,0,0,80,82,3,14,7,0,81,74,1,0,0,0,81,76,1,0,0,0,81,80,1,0,0,0,
        82,13,1,0,0,0,83,90,3,16,8,0,84,90,3,18,9,0,85,90,3,20,10,0,86,90,
        3,22,11,0,87,90,3,24,12,0,88,90,5,27,0,0,89,83,1,0,0,0,89,84,1,0,
        0,0,89,85,1,0,0,0,89,86,1,0,0,0,89,87,1,0,0,0,89,88,1,0,0,0,90,15,
        1,0,0,0,91,92,7,1,0,0,92,17,1,0,0,0,93,94,7,2,0,0,94,19,1,0,0,0,
        95,96,7,3,0,0,96,21,1,0,0,0,97,98,7,4,0,0,98,23,1,0,0,0,99,100,7,
        5,0,0,100,25,1,0,0,0,5,29,63,71,81,89
    ]

class ThreatRulesParser ( Parser ):

    grammarFileName = "ThreatRules.g4"

    atn = ATNDeserializer().deserialize(serializedATN())

    decisionsToDFA = [ DFA(ds, i) for i, ds in enumerate(atn.decisionToState) ]

    sharedContextCache = PredictionContextCache()

    literalNames = [ "<INVALID>", "'E5'", "'E4'", "'E3'", "'E2'", "'E1'", 
                     "'d4'", "'d3'", "'d2'", "'d1'", "'w1'", "'w2'", "'w3'", 
                     "'f1'", "'f2'", "'f3'", "'t1'", "'t2'", "'t3'", "'r1'", 
                     "'r2'", "'r3'", "'a1'", "'a2'", "'a3'", "'a4'", "'a5'", 
                     "'others'", "'|'", "'&'", "'!'", "'('", "')'", "'{'", 
                     "'}'", "':'", "';'" ]

    symbolicNames = [ "<INVALID>", "E5", "E4", "E3", "E2", "E1", "D4", "D3", 
                      "D2", "D1", "W1", "W2", "W3", "F1", "F2", "F3", "T1", 
                      "T2", "T3", "R1", "R2", "R3", "A1", "A2", "A3", "A4", 
                      "A5", "OTHERS", "OR", "AND", "NOT", "LPAREN", "RPAREN", 
                      "LBRACE", "RBRACE", "COLON", "SEMICOLON", "BLOCK_COMMENT", 
                      "LINE_COMMENT", "WS", "ERROR_CHAR" ]

    RULE_program = 0
    RULE_threatBlock = 1
    RULE_threatLevel = 2
    RULE_expression = 3
    RULE_orExpression = 4
    RULE_andExpression = 5
    RULE_unaryExpression = 6
    RULE_atom = 7
    RULE_windLevel = 8
    RULE_fogLevel = 9
    RULE_tempLevel = 10
    RULE_rainLevel = 11
    RULE_avalancheLevel = 12

    ruleNames =  [ "program", "threatBlock", "threatLevel", "expression", 
                   "orExpression", "andExpression", "unaryExpression", "atom", 
                   "windLevel", "fogLevel", "tempLevel", "rainLevel", "avalancheLevel" ]

    EOF = Token.EOF
    E5=1
    E4=2
    E3=3
    E2=4
    E1=5
    D4=6
    D3=7
    D2=8
    D1=9
    W1=10
    W2=11
    W3=12
    F1=13
    F2=14
    F3=15
    T1=16
    T2=17
    T3=18
    R1=19
    R2=20
    R3=21
    A1=22
    A2=23
    A3=24
    A4=25
    A5=26
    OTHERS=27
    OR=28
    AND=29
    NOT=30
    LPAREN=31
    RPAREN=32
    LBRACE=33
    RBRACE=34
    COLON=35
    SEMICOLON=36
    BLOCK_COMMENT=37
    LINE_COMMENT=38
    WS=39
    ERROR_CHAR=40

    def __init__(self, input:TokenStream, output:TextIO = sys.stdout):
        super().__init__(input, output)
        self.checkVersion("4.13.1")
        self._interp = ParserATNSimulator(self, self.atn, self.decisionsToDFA, self.sharedContextCache)
        self._predicates = None




    class ProgramContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def EOF(self):
            return self.getToken(ThreatRulesParser.EOF, 0)

        def threatBlock(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(ThreatRulesParser.ThreatBlockContext)
            else:
                return self.getTypedRuleContext(ThreatRulesParser.ThreatBlockContext,i)


        def getRuleIndex(self):
            return ThreatRulesParser.RULE_program

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitProgram" ):
                return visitor.visitProgram(self)
            else:
                return visitor.visitChildren(self)




    def program(self):

        localctx = ThreatRulesParser.ProgramContext(self, self._ctx, self.state)
        self.enterRule(localctx, 0, self.RULE_program)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 29
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while (((_la) & ~0x3f) == 0 and ((1 << _la) & 62) != 0):
                self.state = 26
                self.threatBlock()
                self.state = 31
                self._errHandler.sync(self)
                _la = self._input.LA(1)

            self.state = 32
            self.match(ThreatRulesParser.EOF)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class ThreatBlockContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def threatLevel(self):
            return self.getTypedRuleContext(ThreatRulesParser.ThreatLevelContext,0)


        def LBRACE(self):
            return self.getToken(ThreatRulesParser.LBRACE, 0)

        def D4(self):
            return self.getToken(ThreatRulesParser.D4, 0)

        def COLON(self, i:int=None):
            if i is None:
                return self.getTokens(ThreatRulesParser.COLON)
            else:
                return self.getToken(ThreatRulesParser.COLON, i)

        def expression(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(ThreatRulesParser.ExpressionContext)
            else:
                return self.getTypedRuleContext(ThreatRulesParser.ExpressionContext,i)


        def SEMICOLON(self, i:int=None):
            if i is None:
                return self.getTokens(ThreatRulesParser.SEMICOLON)
            else:
                return self.getToken(ThreatRulesParser.SEMICOLON, i)

        def D3(self):
            return self.getToken(ThreatRulesParser.D3, 0)

        def D2(self):
            return self.getToken(ThreatRulesParser.D2, 0)

        def D1(self):
            return self.getToken(ThreatRulesParser.D1, 0)

        def RBRACE(self):
            return self.getToken(ThreatRulesParser.RBRACE, 0)

        def getRuleIndex(self):
            return ThreatRulesParser.RULE_threatBlock

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitThreatBlock" ):
                return visitor.visitThreatBlock(self)
            else:
                return visitor.visitChildren(self)




    def threatBlock(self):

        localctx = ThreatRulesParser.ThreatBlockContext(self, self._ctx, self.state)
        self.enterRule(localctx, 2, self.RULE_threatBlock)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 34
            self.threatLevel()
            self.state = 35
            self.match(ThreatRulesParser.LBRACE)
            self.state = 36
            self.match(ThreatRulesParser.D4)
            self.state = 37
            self.match(ThreatRulesParser.COLON)
            self.state = 38
            self.expression()
            self.state = 39
            self.match(ThreatRulesParser.SEMICOLON)
            self.state = 40
            self.match(ThreatRulesParser.D3)
            self.state = 41
            self.match(ThreatRulesParser.COLON)
            self.state = 42
            self.expression()
            self.state = 43
            self.match(ThreatRulesParser.SEMICOLON)
            self.state = 44
            self.match(ThreatRulesParser.D2)
            self.state = 45
            self.match(ThreatRulesParser.COLON)
            self.state = 46
            self.expression()
            self.state = 47
            self.match(ThreatRulesParser.SEMICOLON)
            self.state = 48
            self.match(ThreatRulesParser.D1)
            self.state = 49
            self.match(ThreatRulesParser.COLON)
            self.state = 50
            self.expression()
            self.state = 51
            self.match(ThreatRulesParser.SEMICOLON)
            self.state = 52
            self.match(ThreatRulesParser.RBRACE)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class ThreatLevelContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def E5(self):
            return self.getToken(ThreatRulesParser.E5, 0)

        def E4(self):
            return self.getToken(ThreatRulesParser.E4, 0)

        def E3(self):
            return self.getToken(ThreatRulesParser.E3, 0)

        def E2(self):
            return self.getToken(ThreatRulesParser.E2, 0)

        def E1(self):
            return self.getToken(ThreatRulesParser.E1, 0)

        def getRuleIndex(self):
            return ThreatRulesParser.RULE_threatLevel

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitThreatLevel" ):
                return visitor.visitThreatLevel(self)
            else:
                return visitor.visitChildren(self)




    def threatLevel(self):

        localctx = ThreatRulesParser.ThreatLevelContext(self, self._ctx, self.state)
        self.enterRule(localctx, 4, self.RULE_threatLevel)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 54
            _la = self._input.LA(1)
            if not((((_la) & ~0x3f) == 0 and ((1 << _la) & 62) != 0)):
                self._errHandler.recoverInline(self)
            else:
                self._errHandler.reportMatch(self)
                self.consume()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class ExpressionContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def orExpression(self):
            return self.getTypedRuleContext(ThreatRulesParser.OrExpressionContext,0)


        def getRuleIndex(self):
            return ThreatRulesParser.RULE_expression

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitExpression" ):
                return visitor.visitExpression(self)
            else:
                return visitor.visitChildren(self)




    def expression(self):

        localctx = ThreatRulesParser.ExpressionContext(self, self._ctx, self.state)
        self.enterRule(localctx, 6, self.RULE_expression)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 56
            self.orExpression()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class OrExpressionContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def andExpression(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(ThreatRulesParser.AndExpressionContext)
            else:
                return self.getTypedRuleContext(ThreatRulesParser.AndExpressionContext,i)


        def OR(self, i:int=None):
            if i is None:
                return self.getTokens(ThreatRulesParser.OR)
            else:
                return self.getToken(ThreatRulesParser.OR, i)

        def getRuleIndex(self):
            return ThreatRulesParser.RULE_orExpression

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitOrExpression" ):
                return visitor.visitOrExpression(self)
            else:
                return visitor.visitChildren(self)




    def orExpression(self):

        localctx = ThreatRulesParser.OrExpressionContext(self, self._ctx, self.state)
        self.enterRule(localctx, 8, self.RULE_orExpression)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 58
            self.andExpression()
            self.state = 63
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while _la==28:
                self.state = 59
                self.match(ThreatRulesParser.OR)
                self.state = 60
                self.andExpression()
                self.state = 65
                self._errHandler.sync(self)
                _la = self._input.LA(1)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class AndExpressionContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def unaryExpression(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(ThreatRulesParser.UnaryExpressionContext)
            else:
                return self.getTypedRuleContext(ThreatRulesParser.UnaryExpressionContext,i)


        def AND(self, i:int=None):
            if i is None:
                return self.getTokens(ThreatRulesParser.AND)
            else:
                return self.getToken(ThreatRulesParser.AND, i)

        def getRuleIndex(self):
            return ThreatRulesParser.RULE_andExpression

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitAndExpression" ):
                return visitor.visitAndExpression(self)
            else:
                return visitor.visitChildren(self)




    def andExpression(self):

        localctx = ThreatRulesParser.AndExpressionContext(self, self._ctx, self.state)
        self.enterRule(localctx, 10, self.RULE_andExpression)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 66
            self.unaryExpression()
            self.state = 71
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while _la==29:
                self.state = 67
                self.match(ThreatRulesParser.AND)
                self.state = 68
                self.unaryExpression()
                self.state = 73
                self._errHandler.sync(self)
                _la = self._input.LA(1)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class UnaryExpressionContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser


        def getRuleIndex(self):
            return ThreatRulesParser.RULE_unaryExpression

     
        def copyFrom(self, ctx:ParserRuleContext):
            super().copyFrom(ctx)



    class ParenExpressionContext(UnaryExpressionContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a ThreatRulesParser.UnaryExpressionContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def LPAREN(self):
            return self.getToken(ThreatRulesParser.LPAREN, 0)
        def expression(self):
            return self.getTypedRuleContext(ThreatRulesParser.ExpressionContext,0)

        def RPAREN(self):
            return self.getToken(ThreatRulesParser.RPAREN, 0)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitParenExpression" ):
                return visitor.visitParenExpression(self)
            else:
                return visitor.visitChildren(self)


    class NotExpressionContext(UnaryExpressionContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a ThreatRulesParser.UnaryExpressionContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def NOT(self):
            return self.getToken(ThreatRulesParser.NOT, 0)
        def unaryExpression(self):
            return self.getTypedRuleContext(ThreatRulesParser.UnaryExpressionContext,0)


        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitNotExpression" ):
                return visitor.visitNotExpression(self)
            else:
                return visitor.visitChildren(self)


    class AtomExpressionContext(UnaryExpressionContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a ThreatRulesParser.UnaryExpressionContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def atom(self):
            return self.getTypedRuleContext(ThreatRulesParser.AtomContext,0)


        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitAtomExpression" ):
                return visitor.visitAtomExpression(self)
            else:
                return visitor.visitChildren(self)



    def unaryExpression(self):

        localctx = ThreatRulesParser.UnaryExpressionContext(self, self._ctx, self.state)
        self.enterRule(localctx, 12, self.RULE_unaryExpression)
        try:
            self.state = 81
            self._errHandler.sync(self)
            token = self._input.LA(1)
            if token in [30]:
                localctx = ThreatRulesParser.NotExpressionContext(self, localctx)
                self.enterOuterAlt(localctx, 1)
                self.state = 74
                self.match(ThreatRulesParser.NOT)
                self.state = 75
                self.unaryExpression()
                pass
            elif token in [31]:
                localctx = ThreatRulesParser.ParenExpressionContext(self, localctx)
                self.enterOuterAlt(localctx, 2)
                self.state = 76
                self.match(ThreatRulesParser.LPAREN)
                self.state = 77
                self.expression()
                self.state = 78
                self.match(ThreatRulesParser.RPAREN)
                pass
            elif token in [10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27]:
                localctx = ThreatRulesParser.AtomExpressionContext(self, localctx)
                self.enterOuterAlt(localctx, 3)
                self.state = 80
                self.atom()
                pass
            else:
                raise NoViableAltException(self)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class AtomContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def windLevel(self):
            return self.getTypedRuleContext(ThreatRulesParser.WindLevelContext,0)


        def fogLevel(self):
            return self.getTypedRuleContext(ThreatRulesParser.FogLevelContext,0)


        def tempLevel(self):
            return self.getTypedRuleContext(ThreatRulesParser.TempLevelContext,0)


        def rainLevel(self):
            return self.getTypedRuleContext(ThreatRulesParser.RainLevelContext,0)


        def avalancheLevel(self):
            return self.getTypedRuleContext(ThreatRulesParser.AvalancheLevelContext,0)


        def OTHERS(self):
            return self.getToken(ThreatRulesParser.OTHERS, 0)

        def getRuleIndex(self):
            return ThreatRulesParser.RULE_atom

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitAtom" ):
                return visitor.visitAtom(self)
            else:
                return visitor.visitChildren(self)




    def atom(self):

        localctx = ThreatRulesParser.AtomContext(self, self._ctx, self.state)
        self.enterRule(localctx, 14, self.RULE_atom)
        try:
            self.state = 89
            self._errHandler.sync(self)
            token = self._input.LA(1)
            if token in [10, 11, 12]:
                self.enterOuterAlt(localctx, 1)
                self.state = 83
                self.windLevel()
                pass
            elif token in [13, 14, 15]:
                self.enterOuterAlt(localctx, 2)
                self.state = 84
                self.fogLevel()
                pass
            elif token in [16, 17, 18]:
                self.enterOuterAlt(localctx, 3)
                self.state = 85
                self.tempLevel()
                pass
            elif token in [19, 20, 21]:
                self.enterOuterAlt(localctx, 4)
                self.state = 86
                self.rainLevel()
                pass
            elif token in [22, 23, 24, 25, 26]:
                self.enterOuterAlt(localctx, 5)
                self.state = 87
                self.avalancheLevel()
                pass
            elif token in [27]:
                self.enterOuterAlt(localctx, 6)
                self.state = 88
                self.match(ThreatRulesParser.OTHERS)
                pass
            else:
                raise NoViableAltException(self)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class WindLevelContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def W1(self):
            return self.getToken(ThreatRulesParser.W1, 0)

        def W2(self):
            return self.getToken(ThreatRulesParser.W2, 0)

        def W3(self):
            return self.getToken(ThreatRulesParser.W3, 0)

        def getRuleIndex(self):
            return ThreatRulesParser.RULE_windLevel

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitWindLevel" ):
                return visitor.visitWindLevel(self)
            else:
                return visitor.visitChildren(self)




    def windLevel(self):

        localctx = ThreatRulesParser.WindLevelContext(self, self._ctx, self.state)
        self.enterRule(localctx, 16, self.RULE_windLevel)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 91
            _la = self._input.LA(1)
            if not((((_la) & ~0x3f) == 0 and ((1 << _la) & 7168) != 0)):
                self._errHandler.recoverInline(self)
            else:
                self._errHandler.reportMatch(self)
                self.consume()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class FogLevelContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def F1(self):
            return self.getToken(ThreatRulesParser.F1, 0)

        def F2(self):
            return self.getToken(ThreatRulesParser.F2, 0)

        def F3(self):
            return self.getToken(ThreatRulesParser.F3, 0)

        def getRuleIndex(self):
            return ThreatRulesParser.RULE_fogLevel

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitFogLevel" ):
                return visitor.visitFogLevel(self)
            else:
                return visitor.visitChildren(self)




    def fogLevel(self):

        localctx = ThreatRulesParser.FogLevelContext(self, self._ctx, self.state)
        self.enterRule(localctx, 18, self.RULE_fogLevel)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 93
            _la = self._input.LA(1)
            if not((((_la) & ~0x3f) == 0 and ((1 << _la) & 57344) != 0)):
                self._errHandler.recoverInline(self)
            else:
                self._errHandler.reportMatch(self)
                self.consume()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class TempLevelContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def T1(self):
            return self.getToken(ThreatRulesParser.T1, 0)

        def T2(self):
            return self.getToken(ThreatRulesParser.T2, 0)

        def T3(self):
            return self.getToken(ThreatRulesParser.T3, 0)

        def getRuleIndex(self):
            return ThreatRulesParser.RULE_tempLevel

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitTempLevel" ):
                return visitor.visitTempLevel(self)
            else:
                return visitor.visitChildren(self)




    def tempLevel(self):

        localctx = ThreatRulesParser.TempLevelContext(self, self._ctx, self.state)
        self.enterRule(localctx, 20, self.RULE_tempLevel)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 95
            _la = self._input.LA(1)
            if not((((_la) & ~0x3f) == 0 and ((1 << _la) & 458752) != 0)):
                self._errHandler.recoverInline(self)
            else:
                self._errHandler.reportMatch(self)
                self.consume()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class RainLevelContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def R1(self):
            return self.getToken(ThreatRulesParser.R1, 0)

        def R2(self):
            return self.getToken(ThreatRulesParser.R2, 0)

        def R3(self):
            return self.getToken(ThreatRulesParser.R3, 0)

        def getRuleIndex(self):
            return ThreatRulesParser.RULE_rainLevel

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitRainLevel" ):
                return visitor.visitRainLevel(self)
            else:
                return visitor.visitChildren(self)




    def rainLevel(self):

        localctx = ThreatRulesParser.RainLevelContext(self, self._ctx, self.state)
        self.enterRule(localctx, 22, self.RULE_rainLevel)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 97
            _la = self._input.LA(1)
            if not((((_la) & ~0x3f) == 0 and ((1 << _la) & 3670016) != 0)):
                self._errHandler.recoverInline(self)
            else:
                self._errHandler.reportMatch(self)
                self.consume()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class AvalancheLevelContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def A1(self):
            return self.getToken(ThreatRulesParser.A1, 0)

        def A2(self):
            return self.getToken(ThreatRulesParser.A2, 0)

        def A3(self):
            return self.getToken(ThreatRulesParser.A3, 0)

        def A4(self):
            return self.getToken(ThreatRulesParser.A4, 0)

        def A5(self):
            return self.getToken(ThreatRulesParser.A5, 0)

        def getRuleIndex(self):
            return ThreatRulesParser.RULE_avalancheLevel

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitAvalancheLevel" ):
                return visitor.visitAvalancheLevel(self)
            else:
                return visitor.visitChildren(self)




    def avalancheLevel(self):

        localctx = ThreatRulesParser.AvalancheLevelContext(self, self._ctx, self.state)
        self.enterRule(localctx, 24, self.RULE_avalancheLevel)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 99
            _la = self._input.LA(1)
            if not((((_la) & ~0x3f) == 0 and ((1 << _la) & 130023424) != 0)):
                self._errHandler.recoverInline(self)
            else:
                self._errHandler.reportMatch(self)
                self.consume()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx






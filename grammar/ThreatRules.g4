/*
 * ============================================================================
 * GRAMATYKA ANTLR4 DLA SYSTEMU MONITOROWANIA TURYSTÓW GÓRSKICH
 * ============================================================================
 *
 * Plik: ThreatRules.g4
 * Opis: Gramatyka bezkontekstowa (CFG) do parsowania reguł zagrożeń z Tabeli 5
 *
 * Autorzy: Szymon Adamczyk, Bartłomiej Król
 * Uczelnia: Akademia Tarnowska
 * Przedmiot: Języki formalne i kompilatory II
 * Rok: 2025/2026
 *
 * ============================================================================
 * STRUKTURA GRAMATYKI:
 *
 * program       -> zbiór bloków zagrożeń (E5, E4, E3, E2, E1)
 * threatBlock   -> blok zagrożenia z 4 regułami dla poziomów trudności
 * difficultyRule -> reguła dla konkretnego poziomu trudności (d1-d4)
 * expression    -> wyrażenie logiczne z operatorami | & !
 *
 * PRECEDENCJA OPERATORÓW: ! (najwyższy) > & (średni) > | (najniższy)
 * ============================================================================
 */

grammar ThreatRules;

// ============================================================================
// REGUŁY SKŁADNIOWE (Parser Rules) - zaczynają się małą literą
// ============================================================================

/*
 * Symbol startowy - cały program składa się z bloków zagrożeń
 * Przykład: E5 {...} E4 {...} E3 {...}
 */
program
    : threatBlock* EOF
    ;

/*
 * Blok zagrożenia - definicja reguł dla jednego poziomu (np. E5)
 * Musi zawierać dokładnie 4 reguły w kolejności: d4, d3, d2, d1
 *
 * Przykład:
 * E5 {
 *   d4: (w2 | w3) | (f2 | f3);
 *   d3: w2 | f3;
 *   d2: w3;
 *   d1: others;
 * }
 */
threatBlock
    : threatLevel LBRACE
        D4 COLON expression SEMICOLON
        D3 COLON expression SEMICOLON
        D2 COLON expression SEMICOLON
        D1 COLON expression SEMICOLON
      RBRACE
    ;

/*
 * Poziom zagrożenia - E1 do E5
 */
threatLevel
    : E5 | E4 | E3 | E2 | E1
    ;

/*
 * WYRAŻENIA LOGICZNE - implementacja precedencji operatorów
 * Budowane od najniższego priorytetu (OR) do najwyższego (NOT)
 */

/*
 * Poziom 1: OR (|) - najniższy priorytet
 * Przykład: w2 | w3 | f2
 */
expression
    : orExpression
    ;

orExpression
    : andExpression (OR andExpression)*
    ;

/*
 * Poziom 2: AND (&) - średni priorytet
 * Przykład: w2 & f3
 */
andExpression
    : unaryExpression (AND unaryExpression)*
    ;

/*
 * Poziom 3: NOT (!) - najwyższy priorytet + nawiasy + atomy
 * Przykład: !w2, !(w2 | w3), w2
 */
unaryExpression
    : NOT unaryExpression           # NotExpression
    | LPAREN expression RPAREN      # ParenExpression
    | atom                          # AtomExpression
    ;

/*
 * Atom - podstawowa jednostka (zmienna lub 'others')
 * Przykład: w2, f3, t1, r2, a5, others
 */
atom
    : windLevel
    | fogLevel
    | tempLevel
    | rainLevel
    | avalancheLevel
    | OTHERS
    ;

/*
 * Definicje poszczególnych typów zmiennych
 */
windLevel      : W1 | W2 | W3 ;
fogLevel       : F1 | F2 | F3 ;
tempLevel      : T1 | T2 | T3 ;
rainLevel      : R1 | R2 | R3 ;
avalancheLevel : A1 | A2 | A3 | A4 | A5 ;

// ============================================================================
// REGUŁY LEKSYKALNE (Lexer Rules) - zaczynają się WIELKĄ literą
// ============================================================================

// Poziomy zagrożenia (Threat Levels)
E5 : 'E5' ;
E4 : 'E4' ;
E3 : 'E3' ;
E2 : 'E2' ;
E1 : 'E1' ;

// Poziomy trudności szlaku (Difficulty Levels)
D4 : 'd4' ;
D3 : 'd3' ;
D2 : 'd2' ;
D1 : 'd1' ;

// Wiatr (Wind)
W1 : 'w1' ;
W2 : 'w2' ;
W3 : 'w3' ;

// Mgła (Fog)
F1 : 'f1' ;
F2 : 'f2' ;
F3 : 'f3' ;

// Temperatura (Temperature)
T1 : 't1' ;
T2 : 't2' ;
T3 : 't3' ;

// Deszcz/Burza (Rain/Storm)
R1 : 'r1' ;
R2 : 'r2' ;
R3 : 'r3' ;

// Lawina (Avalanche)
A1 : 'a1' ;
A2 : 'a2' ;
A3 : 'a3' ;
A4 : 'a4' ;
A5 : 'a5' ;

// Specjalny przypadek - "wszystkie inne"
OTHERS : 'others' ;

// Operatory logiczne
OR   : '|' ;
AND  : '&' ;
NOT  : '!' ;

// Separatory
LPAREN    : '(' ;
RPAREN    : ')' ;
LBRACE    : '{' ;
RBRACE    : '}' ;
COLON     : ':' ;
SEMICOLON : ';' ;

// Komentarze w stylu C (ignorowane)
BLOCK_COMMENT
    : '/*' .*? '*/' -> skip
    ;

LINE_COMMENT
    : '//' ~[\r\n]* -> skip
    ;

// Białe znaki (ignorowane)
WS
    : [ \t\r\n\u000C]+ -> skip
    ;

// Obsługa nieznanych znaków (error handling)
ERROR_CHAR
    : .
    ;

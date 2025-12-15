# Jak działa Lexer i Parser w Mountain Monitor

> Szczegółowe wyjaśnienie tokenizacji i parsowania reguł zagrożeń

---

## 📚 Spis Treści

1. [Podstawy - Co to jest Lexer i Parser?](#1-podstawy)
2. [LEXER - Tokenizacja](#2-lexer---tokenizacja)
3. [PARSER - Budowanie drzewa składniowego](#3-parser---budowanie-drzewa-składniowego)
4. [Precedencja operatorów](#4-precedencja-operatorów)
5. [Pełny przykład krok po kroku](#5-pełny-przykład-krok-po-kroku)
6. [Visitor Pattern - Transformacja AST](#6-visitor-pattern)

---

## 1. Podstawy

### Co to jest Lexer i Parser?

```
WEJŚCIE (tekst)
      ↓
   LEXER (Lexical Analysis)
      ↓
   TOKENY (stream)
      ↓
   PARSER (Syntax Analysis)
      ↓
   AST (Abstract Syntax Tree)
      ↓
   VISITOR (Semantic Analysis)
      ↓
WYJŚCIE (obiekty Python)
```

**LEXER** = Tokenizer
- Czyta tekst znak po znaku
- Grupuje znaki w **tokeny** (słowa, symbole)
- Ignoruje białe znaki i komentarze

**PARSER** = Syntax Analyzer
- Czyta tokeny z lexera
- Buduje **drzewo składniowe** (parse tree / AST)
- Sprawdza poprawność struktury

---

## 2. LEXER - Tokenizacja

### Definicje tokenów w `ThreatRules.g4`

Lexer rozpoznaje **38 typów tokenów**:

#### Grupa 1: Poziomy zagrożenia (5 tokenów)
```antlr
E5 : 'E5' ;
E4 : 'E4' ;
E3 : 'E3' ;
E2 : 'E2' ;
E1 : 'E1' ;
```

**Przykład:**
```
Wejście: "E5"
Token:   E5 (typ: THREAT_LEVEL)
```

#### Grupa 2: Poziomy trudności (4 tokeny)
```antlr
D4 : 'd4' ;
D3 : 'd3' ;
D2 : 'd2' ;
D1 : 'd1' ;
```

#### Grupa 3: Warunki pogodowe (15 tokenów)
```antlr
// Wiatr
W1 : 'w1' ;
W2 : 'w2' ;
W3 : 'w3' ;

// Mgła
F1 : 'f1' ;
F2 : 'f2' ;
F3 : 'f3' ;

// Temperatura
T1 : 't1' ;
T2 : 't2' ;
T3 : 't3' ;

// Deszcz
R1 : 'r1' ;
R2 : 'r2' ;
R3 : 'r3' ;

// Lawina
A1 : 'a1' ;
A2 : 'a2' ;
A3 : 'a3' ;
A4 : 'a4' ;
A5 : 'a5' ;
```

#### Grupa 4: Operatory (3 tokeny)
```antlr
OR  : '|' ;   // lub
AND : '&' ;   // i
NOT : '!' ;   // negacja
```

#### Grupa 5: Separatory (6 tokenów)
```antlr
LPAREN    : '(' ;   // lewy nawias
RPAREN    : ')' ;   // prawy nawias
LBRACE    : '{' ;   // lewy klamrowy
RBRACE    : '}' ;   // prawy klamrowy
COLON     : ':' ;   // dwukropek
SEMICOLON : ';' ;   // średnik
```

#### Grupa 6: Specjalne (1 token)
```antlr
OTHERS : 'others' ;   // catch-all dla E1
```

#### Grupa 7: Ignorowane
```antlr
WS            : [ \t\r\n\u000C]+ -> skip ;  // białe znaki
BLOCK_COMMENT : '/*' .*? '*/' -> skip ;     // /* komentarz */
LINE_COMMENT  : '//' ~[\r\n]* -> skip ;     // // komentarz
```

---

### Przykład tokenizacji

**Wejście:**
```
E5 { d4: w3 & f3; }
```

**Tokeny (stream):**
```
[E5] [LBRACE] [D4] [COLON] [W3] [AND] [F3] [SEMICOLON] [RBRACE]
  ↑      ↑      ↑      ↑      ↑     ↑     ↑       ↑         ↑
  1      2      3      4      5     6     7       8         9
```

**Szczegółowo:**
```
Token 1: E5         (typ: E5, text: "E5")
Token 2: LBRACE     (typ: LBRACE, text: "{")
Token 3: D4         (typ: D4, text: "d4")
Token 4: COLON      (typ: COLON, text: ":")
Token 5: W3         (typ: W3, text: "w3")
Token 6: AND        (typ: AND, text: "&")
Token 7: F3         (typ: F3, text: "f3")
Token 8: SEMICOLON  (typ: SEMICOLON, text: ";")
Token 9: RBRACE     (typ: RBRACE, text: "}")
```

---

## 3. PARSER - Budowanie drzewa składniowego

### Reguły parsera (hierarchia)

Parser ma **11 reguł składniowych**:

```
program              (symbol startowy)
 └─ threatBlock      (blok E5, E4, E3, E2, E1)
     ├─ threatLevel  (E5 | E4 | E3 | E2 | E1)
     └─ expression   (wyrażenie logiczne)
         └─ orExpression      (poziom 1: OR)
             └─ andExpression (poziom 2: AND)
                 └─ unaryExpression (poziom 3: NOT/nawiasy/atomy)
                     └─ atom
                         ├─ windLevel
                         ├─ fogLevel
                         ├─ tempLevel
                         ├─ rainLevel
                         └─ avalancheLevel
```

### Reguła 1: `program` (symbol startowy)

```antlr
program
    : threatBlock* EOF
    ;
```

**Znaczenie:**
- Program składa się z **0 lub więcej** bloków zagrożeń
- Kończy się `EOF` (End Of File)

**Przykład pasujący:**
```
E5 { ... }
E4 { ... }
E3 { ... }
```

**Przykład NIE pasujący:**
```
E5 { ... } coś_innego   ← błąd, oczekiwano EOF lub kolejny threatBlock
```

---

### Reguła 2: `threatBlock` (blok zagrożenia)

```antlr
threatBlock
    : threatLevel LBRACE
        D4 COLON expression SEMICOLON
        D3 COLON expression SEMICOLON
        D2 COLON expression SEMICOLON
        D1 COLON expression SEMICOLON
      RBRACE
    ;
```

**Znaczenie:**
- Każdy blok MUSI mieć **dokładnie 4 reguły** w kolejności: d4, d3, d2, d1
- Składnia: `poziom { d4: expr; d3: expr; d2: expr; d1: expr; }`

**Przykład:**
```
E5 {
    d4: (w3 & f3) | a5;
    d3: w3 | f3;
    d2: w3;
    d1: others;
}
```

**UWAGA:** Kolejność d4→d3→d2→d1 jest **wymuszona** przez gramatykę!

---

### Reguła 3-7: Wyrażenia logiczne (precedencja)

#### `orExpression` - poziom 1 (najniższy priorytet)

```antlr
orExpression
    : andExpression (OR andExpression)*
    ;
```

**Znaczenie:**
- `andExpression OR andExpression OR andExpression ...`
- Operator `|` wiąże **najsłabiej**

**Przykład:**
```
w1 | w2 | w3
```

Parsuje się jako:
```
orExpression
  ├─ andExpression (w1)
  ├─ OR
  ├─ andExpression (w2)
  ├─ OR
  └─ andExpression (w3)
```

---

#### `andExpression` - poziom 2 (średni priorytet)

```antlr
andExpression
    : unaryExpression (AND unaryExpression)*
    ;
```

**Znaczenie:**
- `unaryExpression AND unaryExpression AND ...`
- Operator `&` wiąże **mocniej** niż `|`

**Przykład:**
```
w1 & w2 & w3
```

Parsuje się jako:
```
andExpression
  ├─ unaryExpression (w1)
  ├─ AND
  ├─ unaryExpression (w2)
  ├─ AND
  └─ unaryExpression (w3)
```

---

#### `unaryExpression` - poziom 3 (najwyższy priorytet)

```antlr
unaryExpression
    : NOT unaryExpression           # NotExpression
    | LPAREN expression RPAREN      # ParenExpression
    | atom                          # AtomExpression
    ;
```

**Znaczenie:**
- Operator `!` wiąże **najmocniej**
- Nawiasy `()` wymuszają kolejność
- Atomy (w1, f2, etc.) są najniższym poziomem

**Przykład 1:** Negacja
```
!w1
```
→ `NOT(w1)`

**Przykład 2:** Nawiasy
```
(w1 | w2)
```
→ Wymusza przetworzenie OR przed AND

**Przykład 3:** Atom
```
w3
```
→ Po prostu `w3`

---

### Reguła 8: `atom` (atomy)

```antlr
atom
    : windLevel         # w1, w2, w3
    | fogLevel          # f1, f2, f3
    | tempLevel         # t1, t2, t3
    | rainLevel         # r1, r2, r3
    | avalancheLevel    # a1, a2, a3, a4, a5
    | OTHERS            # 'others'
    ;
```

**Znaczenie:**
- Atom to **podstawowa jednostka** wyrażenia
- Może być zmienną pogodową lub słowem `others`

---

## 4. Precedencja operatorów

### Dlaczego precedencja jest ważna?

**Bez precedencji:**
```
w1 | w2 & w3
```
Można by interpretować jako:
1. `(w1 | w2) & w3` ← błędne
2. `w1 | (w2 & w3)` ← poprawne

**Z precedencją w gramatyce:**
```
expression
 └─ orExpression           ← priorytet 1 (najniższy)
     └─ andExpression      ← priorytet 2
         └─ unaryExpression ← priorytet 3 (najwyższy)
```

AND jest **głębiej** w drzewie → parsowane **przed** OR!

---

### Tabela precedencji

| Operator | Priorytet | Wiązanie | Przykład |
|----------|-----------|----------|----------|
| `!` (NOT) | 1 (najwyższy) | Prawostronne | `!w1` |
| `&` (AND) | 2 | Lewe | `w1 & w2 & w3` = `((w1 & w2) & w3)` |
| `|` (OR) | 3 (najniższy) | Lewe | `w1 | w2 | w3` = `((w1 | w2) | w3)` |

---

### Przykłady z precedencją

#### Przykład 1: AND ma wyższy priorytet niż OR
```
w1 | w2 & w3
```

**Parse tree:**
```
orExpression
  ├─ andExpression
  │   └─ atom (w1)
  ├─ OR
  └─ andExpression
      ├─ atom (w2)
      ├─ AND
      └─ atom (w3)
```

**Wynik:** `w1 | (w2 & w3)`

---

#### Przykład 2: NOT ma najwyższy priorytet
```
!w1 & w2
```

**Parse tree:**
```
andExpression
  ├─ unaryExpression
  │   ├─ NOT
  │   └─ atom (w1)
  ├─ AND
  └─ unaryExpression
      └─ atom (w2)
```

**Wynik:** `(!w1) & w2`

---

#### Przykład 3: Nawiasy wymuszają kolejność
```
(w1 | w2) & w3
```

**Parse tree:**
```
andExpression
  ├─ unaryExpression (ParenExpression)
  │   ├─ LPAREN
  │   ├─ orExpression
  │   │   ├─ andExpression (w1)
  │   │   ├─ OR
  │   │   └─ andExpression (w2)
  │   └─ RPAREN
  ├─ AND
  └─ unaryExpression
      └─ atom (w3)
```

**Wynik:** Nawiasy wymuszają OR przed AND!

---

## 5. Pełny przykład krok po kroku

### Wejście:
```
E5 { d4: (w3 & f3) | a5; }
```

---

### Krok 1: LEXER - Tokenizacja

**Wynik:**
```
Token  1: E5
Token  2: LBRACE      "{"
Token  3: D4          "d4"
Token  4: COLON       ":"
Token  5: LPAREN      "("
Token  6: W3          "w3"
Token  7: AND         "&"
Token  8: F3          "f3"
Token  9: RPAREN      ")"
Token 10: OR          "|"
Token 11: A5          "a5"
Token 12: SEMICOLON   ";"
Token 13: RBRACE      "}"
```

---

### Krok 2: PARSER - Budowanie drzewa

**Parse Tree (uproszczone):**
```
program
 └─ threatBlock
     ├─ threatLevel (E5)
     ├─ LBRACE
     ├─ D4
     ├─ COLON
     ├─ expression
     │   └─ orExpression
     │       ├─ andExpression
     │       │   ├─ unaryExpression (ParenExpression)
     │       │   │   ├─ LPAREN
     │       │   │   ├─ expression
     │       │   │   │   └─ orExpression
     │       │   │   │       └─ andExpression
     │       │   │   │           ├─ unaryExpression (w3)
     │       │   │   │           ├─ AND
     │       │   │   │           └─ unaryExpression (f3)
     │       │   │   └─ RPAREN
     │       ├─ OR
     │       └─ andExpression
     │           └─ unaryExpression (a5)
     ├─ SEMICOLON
     └─ RBRACE
```

**AST (Abstract Syntax Tree - uproszczone):**
```
ThreatBlock(E5)
 └─ DifficultyRule(d4)
     └─ OR
         ├─ AND
         │   ├─ w3
         │   └─ f3
         └─ a5
```

**Interpretacja:**
- E5 dla d4 = `(w3 AND f3) OR a5`
- Znaczenie: KRYTYCZNE gdy:
  - (silny wiatr **I** gęsta mgła) **LUB**
  - (lawina stopnia 5)

---

### Krok 3: VISITOR - Transformacja do obiektów Python

**Kod w `src/parser/visitor.py`:**
```python
class ThreatRulesVisitor(ThreatRulesVisitor):
    def visitThreatBlock(self, ctx):
        level = ctx.threatLevel().getText()  # "E5"

        # Pobierz wszystkie 4 reguły
        rules = []
        for i in range(4):
            difficulty = ...  # d4, d3, d2, d1
            expr = self.visit(ctx.expression(i))  # Rekurencyjnie przetwórz wyrażenie
            rules.append(Rule(difficulty, expr))

        return ThreatBlock(level, rules)

    def visitOrExpression(self, ctx):
        # Jeśli jest operator OR
        if ctx.OR():
            left = self.visit(ctx.andExpression(0))
            right = self.visit(ctx.andExpression(1))
            return BinaryOp(OR, left, right)
        else:
            return self.visit(ctx.andExpression(0))
```

**Wynik:**
```python
ThreatBlock(
    level=ThreatLevel.E5,
    rules=[
        Rule(
            difficulty=DifficultyLevel.D4,
            expression=BinaryOp(
                op=OR,
                left=BinaryOp(op=AND, left=Atom("w3"), right=Atom("f3")),
                right=Atom("a5")
            )
        ),
        # ... d3, d2, d1
    ]
)
```

---

## 6. Visitor Pattern

### Po co Visitor?

**Problem:** ANTLR generuje drzewo parse tree, ale my chcemy obiektów Python (`ThreatBlock`, `Rule`, etc.)

**Rozwiązanie:** Visitor Pattern - przechodzi po drzewie i tworzy nasze obiekty.

---

### Jak działa Visitor?

**1. ANTLR generuje interfejs:**
```python
# src/parser/generated/ThreatRulesVisitor.py (wygenerowany)
class ThreatRulesVisitor:
    def visitProgram(self, ctx):
        pass

    def visitThreatBlock(self, ctx):
        pass

    def visitExpression(self, ctx):
        pass
    # ... etc.
```

**2. My implementujemy:**
```python
# src/parser/visitor.py (nasz kod)
class RulesVisitor(ThreatRulesVisitor):
    def visitProgram(self, ctx):
        """Odwiedza program i zwraca listę ThreatBlock"""
        blocks = []
        for block_ctx in ctx.threatBlock():
            blocks.append(self.visit(block_ctx))
        return blocks

    def visitThreatBlock(self, ctx):
        """Odwiedza blok zagrożenia i zwraca ThreatBlock"""
        level = ctx.threatLevel().getText()  # "E5"
        rules = []

        # Dla każdej z 4 reguł (d4, d3, d2, d1)
        for i in range(4):
            expr_ctx = ctx.expression(i)
            expr = self.visit(expr_ctx)  # Rekurencja!
            rules.append(Rule(f"d{4-i}", expr))

        return ThreatBlock(level, rules)

    def visitOrExpression(self, ctx):
        """Odwiedza wyrażenie OR"""
        and_exprs = [self.visit(e) for e in ctx.andExpression()]

        # Jeśli tylko jedno andExpression, zwróć je
        if len(and_exprs) == 1:
            return and_exprs[0]

        # Jeśli więcej, stwórz drzewo OR
        result = and_exprs[0]
        for expr in and_exprs[1:]:
            result = BinaryOp(OR, result, expr)
        return result
```

---

### Przepływ Visitor (przykład)

**Wejście:** `w1 | w2 & w3`

**1. Parser wywołuje:**
```python
visitor.visit(program_ctx)
```

**2. Visitor przechodzi:**
```
visit(program_ctx)
  → visit(threatBlock_ctx)
      → visit(expression_ctx)
          → visit(orExpression_ctx)           # w1 | (w2 & w3)
              → visit(andExpression_ctx[0])   # w1
                  → visit(atom_ctx)           # w1
                      → return "w1"
              → visit(andExpression_ctx[1])   # w2 & w3
                  → visit(atom_ctx)           # w2
                      → return "w2"
                  → visit(atom_ctx)           # w3
                      → return "w3"
                  → return BinaryOp(AND, "w2", "w3")
              → return BinaryOp(OR, "w1", BinaryOp(AND, "w2", "w3"))
```

**3. Wynik:**
```python
BinaryOp(
    op=OR,
    left="w1",
    right=BinaryOp(op=AND, left="w2", right="w3")
)
```

---

## 🎯 Podsumowanie

### Lexer (Tokenizacja)
- **Wejście:** Tekst `"E5 { d4: w3 & f3; }"`
- **Wyjście:** Stream tokenów `[E5, LBRACE, D4, COLON, W3, AND, F3, ...]`
- **Plik:** `grammar/ThreatRules.g4` (reguły leksykalne - WIELKIE litery)

### Parser (Analiza składniowa)
- **Wejście:** Stream tokenów
- **Wyjście:** Parse tree (drzewo składniowe)
- **Plik:** `grammar/ThreatRules.g4` (reguły składniowe - małe litery)

### Visitor (Transformacja)
- **Wejście:** Parse tree
- **Wyjście:** Obiekty Python (`ThreatBlock`, `Rule`, etc.)
- **Plik:** `src/parser/visitor.py`

---

## 📂 Gdzie szukać w kodzie?

| Co chcesz zobaczyć | Plik |
|--------------------|------|
| Definicje tokenów (lexer) | `grammar/ThreatRules.g4` (linie 130-202) |
| Reguły parsera | `grammar/ThreatRules.g4` (linie 29-124) |
| Wygenerowany lexer | `src/parser/generated/ThreatRulesLexer.py` |
| Wygenerowany parser | `src/parser/generated/ThreatRulesParser.py` |
| Visitor (transformacja) | `src/parser/visitor.py` |
| Modele danych | `src/parser/models.py` |
| Główny parser reguł | `src/parser/rule_parser.py` |

---

## 🧪 Testuj samodzielnie!

### Test 1: Tokenizacja
```bash
python repl.py
>>> :parse "E5 { d4: w3; d3: w2; d2: w1; d1: others; }"
```

### Test 2: Drzewo składniowe
Ustaw breakpoint w `visitor.py` i zobacz jak działa rekurencja!

### Test 3: Precedencja
Spróbuj:
- `w1 | w2 & w3` → `w1 | (w2 & w3)`
- `!w1 & w2` → `(!w1) & w2`
- `(w1 | w2) & w3` → wymuszenie OR przed AND

---

**Powodzenia w zrozumieniu kompilatora!** 🚀

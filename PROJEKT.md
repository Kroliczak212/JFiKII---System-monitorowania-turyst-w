# Mountain Monitor - System Monitorowania Zagrożeń Górskich

**Projekt:** Kompilator reguł zagrożeń dla GOPR
**Kurs:** Języki formalne i kompilatory II
**Uczelnia:** Akademia Tarnowska
**Autorzy:** Szymon Adamczyk, Bartłomiej Król

---

## 1. Opis Projektu

### 1.1 Cel
System klasyfikuje zagrożenia górskie na 5 poziomów (E1-E5) na podstawie warunków pogodowych i trudności szlaku. Implementuje parser reguł zagrożeń używając gramatyki bezkontekstowej (CFG Type-2) z ANTLR4.

### 1.2 Źródło
Projekt bazuje na artykule naukowym:
> "Exploration of Human Activities Using Message Streaming Brokers and Automated Logical Reasoning"
> Tabela 5: Predefined reaction levels for different threat levels

### 1.3 Sygnały Wejściowe
**Format:** `w[1-3],f[1-3],t[1-3],r[1-3],a[1-5],d[1-4]`

| Parametr | Zakres | Znaczenie |
|----------|--------|-----------|
| `w` | 1-3 | Wiatr (1=słaby, 2=średni, 3=silny) |
| `f` | 1-3 | Mgła (1=brak, 2=średnia, 3=gęsta) |
| `t` | 1-3 | Temperatura (1=normalna, 2=niska, 3=bardzo niska) |
| `r` | 1-3 | Deszcz (1=brak, 2=średni, 3=intensywny) |
| `a` | 1-5 | Ryzyko lawiny (rosnące) |
| `d` | 1-4 | Trudność szlaku (1=łatwy, 4=bardzo trudny) |

### 1.4 Poziomy Zagrożenia

| Poziom | Kolor | Opis | Akcja |
|--------|-------|------|-------|
| **E1** | Zielony | Bezpieczne | Normalne monitorowanie |
| **E2** | Żółty | Średnie zagrożenie | Zwiększony monitoring |
| **E3** | Pomarańczowy | Podwyższone | Wzmożone monitorowanie |
| **E4** | Czerwony | Wysokie | Tylko doświadczeni |
| **E5** | Czarny | KRYTYCZNE | **ZAKAZ WSTĘPU** |

---

## 2. Gramatyka

### 2.1 Typ Gramatyki
**Context-Free Grammar (CFG Type-2)** w hierarchii Chomsky'ego

**Dlaczego CFG, nie regularna?**
- Wyrażenia z nawiasami `(w3 & f3) | (w2 & t2)` wymagają liczenia zagnieżdżeń
- Gramatyki regularne (Type-3) nie mają stosu
- CFG jest wystarczająca i wydajna (O(n) dla LL parsera)

### 2.2 Specyfikacja EBNF

```ebnf
rules          = { threat_block } ;
threat_block   = THREAT_LEVEL "{" { rule } "}" ;
rule           = DIFFICULTY ":" or_expression ";" ;

or_expression  = and_expression { "|" and_expression } ;
and_expression = unary_expr { "&" unary_expr } ;
unary_expr     = "!" unary_expr
               | "(" or_expression ")"
               | SIGNAL | "others" ;

THREAT_LEVEL   = "E1" | "E2" | "E3" | "E4" | "E5" ;
DIFFICULTY     = "d1" | "d2" | "d3" | "d4" ;
SIGNAL         = ("w" | "f" | "t" | "r") [1-3] | "a" [1-5] ;
```

### 2.3 Precedencja Operatorów
```
! (NOT)     - najwyższy priorytet
& (AND)     - średni priorytet
| (OR)      - najniższy priorytet
```
**Przykład:** `w1 | w2 & w3` = `w1 | (w2 & w3)` (AND wiąże mocniej)

### 2.4 Parser ANTLR4
- Adaptive LL(*) parser generator
- Złożoność: **O(n)** - liniowa
- Jednoznaczna gramatyka - jedno drzewo parsowania

---

## 3. Problem i Rozwiązanie

### 3.1 Problem: Stare Reguły (BŁĘDNE)
```
E5 { d4: w2 | w3 | f2 | f3 | t2 | t3 | a4 | a5; }
```
**Problem:** Użycie tylko OR - każdy pojedynczy średni warunek dawał E5!

### 3.2 Rozwiązanie: Nowe Reguły (POPRAWNE)
```
E5 { d4: (w3 & f3) | (w3 & t3) | a5 | (a4 & w3); }
E4 { d4: (w3 & f2) | (w3 & t2) | a4; }
E3 { d4: (w2 & f2) | w3 | f3 | t3 | a3; }
E2 { d4: w2 | f2 | t2 | r2 | a2; }
E1 { d4: others; }
```

### 3.3 Porównanie

| Warunki | Stare | Nowe | Poprawne |
|---------|-------|------|----------|
| `w1,f1,t1,r1,a1,d4` | E1 | E1 | E1 ✓ |
| `w2,f1,t1,r1,a1,d4` | E5 ❌ | E2 | E2 ✓ |
| `w2,f2,t1,r1,a1,d4` | E5 ❌ | E3 | E3 ✓ |
| `w3,f2,t1,r1,a1,d4` | E5 ❌ | E4 | E4 ✓ |
| `w3,f3,t1,r1,a1,d4` | E5 ✓ | E5 | E5 ✓ |

**Wynik:** Stare 40% → Nowe **100%**

---

## 4. Uruchomienie Aplikacji

### 4.1 Instalacja
```bash
pip install -r requirements.txt
```

### 4.2 Tryby Uruchomienia

```bash
# Pojedynczy sygnał
python main.py --single "w3,f3,t1,r1,a1,d4"

# Tryb interaktywny
python main.py --interactive

# Plik z sygnałami
python main.py --signals examples/signals.txt
```

### 4.3 REPL (Interaktywny)
```bash
python repl.py
>>> :load data/rules.txt
>>> :test w3,f3,t1,r1,a1,d4
Result: E5
```

**Komendy:** `:load`, `:test`, `:parse`, `:help`, `:quit`

---

## 5. Testy

### 5.1 Uruchomienie
```bash
python run_tests.py
```

**Wynik:** `47 testów, 100% pass rate`

### 5.2 Pokrycie Testowe

| Poziom | Testy | Opis |
|--------|-------|------|
| E1 | 4 | Optymalne warunki |
| E2 | 9 | Pojedyncze średnie |
| E3 | 7 | Kombinacje średnich LUB pojedynczy ekstremalny |
| E4 | 10 | Ekstremalny + średni LUB a4 |
| E5 | 17 | Kombinacje ekstremalnych LUB a5 |

### 5.3 Kluczowe Przypadki

**Granice poziomów:**
```
E1/E2: w1,f1,t1,r1,a1,d4 (E1) vs w2,f1,t1,r1,a1,d4 (E2)
E2/E3: w2,f1,t1,r1,a1,d4 (E2) vs w2,f2,t1,r1,a1,d4 (E3)
E3/E4: w3,f1,t1,r1,a1,d4 (E3) vs w3,f2,t1,r1,a1,d4 (E4)
E4/E5: w3,f2,t1,r1,a1,d4 (E4) vs w3,f3,t1,r1,a1,d4 (E5)
```

**Dominacja lawin:**
- `a4` na KAŻDYM szlaku → E4 (nawet d1!)
- `a5` na KAŻDYM szlaku → E5 (nawet d1!)

**Triple threat:**
- `w3,f3,t3,r1,a1,d1` → E5 (nawet na łatwym szlaku!)

---

## 6. Właściwości Formalne

| Właściwość | Wartość |
|------------|---------|
| Typ gramatyki | CFG Type-2 (Chomsky) |
| Parser | ANTLR4 Adaptive LL(*) |
| Złożoność czasowa | O(n) |
| Złożoność pamięciowa | O(n) |
| Jednoznaczność | Tak |

### Decyzje Projektowe

**Brak notacji @r:** Lokalizacja implicit przez trudność `d1-d4`. Uproszczenie dla kursu.

**Semantyka "others":** Token zwraca `False` - E1 jest fallbackiem gdy żaden wyższy poziom nie pasuje.

---

## 7. Prezentacja (10 min)

### Timeline
| Czas | Sekcja |
|------|--------|
| 0:00-1:00 | Wprowadzenie - problem GOPR |
| 1:00-2:30 | Gramatyka CFG Type-2 |
| 2:30-5:00 | **Live Demo REPL** |
| 5:00-7:00 | Problem OR vs AND |
| 7:00-8:30 | Testy automatyczne |
| 8:30-10:00 | Q&A |

### Demo REPL
```bash
python repl.py
:load data/rules.txt
:test w1,f1,t1,r1,a1,d4    # E1
:test w2,f1,t1,r1,a1,d4    # E2
:test w2,f2,t1,r1,a1,d4    # E3
:test w3,f2,t1,r1,a1,d4    # E4
:test w3,f3,t1,r1,a1,d4    # E5
```

### FAQ

**Q: Dlaczego CFG?**
> Nawiasy wymagają stosu. Gramatyki regularne go nie mają.

**Q: Jak precedencja?**
> Zakodowana strukturalnie: `or_expression → and_expression → unary_expression`

**Q: Dlaczego zmiana reguł?**
> Tylko OR = każdy średni daje E5. AND+OR = poprawna gradacja.

**Q: Złożoność?**
> O(n) czasowa i pamięciowa. LL(*) bez backtrackingu.

---

## 8. Struktura Projektu

```
mountain-monitor/
├── grammar/ThreatRules.g4      # Gramatyka ANTLR4
├── src/
│   ├── parser/                 # Parser reguł
│   └── evaluator/              # Ewaluator + matcher
├── data/rules.txt              # Reguły zagrożeń
├── main.py                     # CLI główny
├── repl.py                     # Interaktywny REPL
├── run_tests.py                # Test runner
├── test_signals_comprehensive.txt  # 47 przypadków
└── docs/EBNF_FORMAL_SPEC.md    # Specyfikacja formalna
```

---

## 9. Podsumowanie

### Osiągnięcia
✅ Gramatyka CFG Type-2 z pełną specyfikacją EBNF
✅ Parser ANTLR4 LL(*), O(n) złożoność
✅ Naprawa błędu w oryginalnych regułach (OR → AND+OR)
✅ 47 testów, **100% pass rate**
✅ Narzędzia demonstracyjne (REPL)

### Kluczowy Wniosek
Zmiana logiki z OR na AND+OR była niezbędna dla poprawnej klasyfikacji zagrożeń zgodnie z wymaganiami GOPR.

---

**Status:** ✅ Projekt gotowy do oddania
**Ostatnia aktualizacja:** 2025-12-15

# Mountain Monitor

> System monitorowania zagrożeń górskich dla GOPR oparty na gramatyce CFG Type-2

![Python Version](https://img.shields.io/badge/python-3.10+-blue.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)
![Tests](https://img.shields.io/badge/tests-47%2F47-brightgreen.svg)
![ANTLR](https://img.shields.io/badge/ANTLR-4.13.1-orange.svg)

**Kurs:** Języki formalne i kompilatory II
**Uczelnia:** Akademia Tarnowska
**Autorzy:** Szymon Adamczyk, Bartłomiej Król

---

## Funkcjonalności

- ✅ **Gramatyka CFG Type-2** z pełną specyfikacją EBNF
- ✅ **Parser ANTLR4 LL(*)** - O(n) złożoność czasowa
- ✅ **5 poziomów zagrożenia** (E1-E5) na podstawie warunków pogodowych
- ✅ **Logika boolean** (AND, OR, NOT) z precedencją operatorów
- ✅ **47 testów** z 100% pass rate
- ✅ **Interaktywny REPL** do testowania reguł
- ✅ **CLI** z 3 trybami pracy

---

## Wymagania

- **Python 3.10+**
- **Java JDK 11+** (do generowania parsera ANTLR)
- **ANTLR 4.13.1** (pobierz [tutaj](https://www.antlr.org/download/antlr-4.13.1-complete.jar))

---

## Instalacja

### 1. Sklonuj repozytorium
```bash
git clone https://github.com/your-username/mountain-monitor.git
cd mountain-monitor
```

### 2. Zainstaluj zależności
```bash
pip install -r requirements.txt
```

### 3. Wygeneruj parser ANTLR (jeśli brakuje plików w `src/parser/generated/`)
```bash
# Windows
generate_parser.bat

# Linux/Mac
./generate_parser.sh
```

---

## Użycie

### Testy (47 przypadków, 100% pass)
```bash
python run_tests.py
```

### Pojedynczy sygnał
```bash
python main.py --single "w3,f3,t1,r1,a1,d4"
# Output: E5 (KRYTYCZNE - ZAKAZ WSTĘPU)
```

### Tryb interaktywny (REPL)
```bash
python repl.py
>>> :load data/rules.txt
>>> :test w3,f3,t1,r1,a1,d4
Result: E5
```

### Plik z sygnałami
```bash
python main.py --signals examples/signals.txt
```

---

## Format Sygnałów

`w[1-3],f[1-3],t[1-3],r[1-3],a[1-5],d[1-4]`

| Parametr | Zakres | Znaczenie |
|----------|--------|-----------|
| `w` | 1-3 | Wiatr (1=słaby, 2=średni, 3=silny) |
| `f` | 1-3 | Mgła (1=brak, 2=średnia, 3=gęsta) |
| `t` | 1-3 | Temperatura (1=normalna, 2=niska, 3=bardzo niska) |
| `r` | 1-3 | Deszcz (1=brak, 2=średni, 3=intensywny) |
| `a` | 1-5 | Ryzyko lawiny (rosnące) |
| `d` | 1-4 | Trudność szlaku (1=łatwy, 4=bardzo trudny) |

---

## Poziomy Zagrożenia

| Poziom | Kolor | Opis | Akcja |
|--------|-------|------|-------|
| **E1** | 🟢 Zielony | Bezpieczne | Normalne monitorowanie |
| **E2** | 🟡 Żółty | Średnie zagrożenie | Zwiększony monitoring |
| **E3** | 🟠 Pomarańczowy | Podwyższone | Wzmożone monitorowanie |
| **E4** | 🔴 Czerwony | Wysokie | Tylko doświadczeni |
| **E5** | ⚫ Czarny | **KRYTYCZNE** | **ZAKAZ WSTĘPU** |

---

## Dokumentacja

- **[PROJEKT.md](PROJEKT.md)** - Kompletny opis projektu (gramatyka, problem/rozwiązanie, testy, prezentacja, FAQ)
- **[grammar/ThreatRules.g4](grammar/ThreatRules.g4)** - Gramatyka ANTLR4
- **[data/rules.txt](data/rules.txt)** - Reguły zagrożeń E1-E5

---

## Struktura Projektu

```
mountain-monitor/
├── grammar/
│   └── ThreatRules.g4          # Gramatyka CFG Type-2
├── src/
│   ├── parser/                 # Parser reguł + modele
│   ├── evaluator/              # Ewaluator logiki + matcher
│   ├── stream/                 # Batch processor
│   └── ui/                     # CLI formatting
├── data/
│   └── rules.txt               # Reguły zagrożeń
├── examples/
│   └── signals.txt             # Przykładowe sygnały
├── main.py                     # CLI główny
├── repl.py                     # REPL interaktywny
├── run_tests.py                # Test runner (47 testów)
└── test_signals_comprehensive.txt  # Przypadki testowe
```

---

## Kluczowe Osiągnięcia

### Problem: Stare Reguły (BŁĘDNE)
```
E5 { d4: w2 | w3 | f2 | f3 | t2 | t3 | a4 | a5; }
```
**Problem:** Użycie tylko OR - każdy pojedynczy średni warunek dawał E5!

### Rozwiązanie: Nowe Reguły (POPRAWNE)
```
E5 { d4: (w3 & f3) | (w3 & t3) | a5 | (a4 & w3); }
E4 { d4: (w3 & f2) | (w3 & t2) | a4; }
E3 { d4: (w2 & f2) | w3 | f3 | t3 | a3; }
E2 { d4: w2 | f2 | t2 | r2 | a2; }
E1 { d4: others; }
```

**Wynik:** Dokładność wzrosła z ~40% do **100%** 🎯

---

## Właściwości Formalne

| Właściwość | Wartość |
|------------|---------|
| Typ gramatyki | CFG Type-2 (Chomsky) |
| Parser | ANTLR4 Adaptive LL(*) |
| Złożoność czasowa | O(n) |
| Złożoność pamięciowa | O(n) |
| Jednoznaczność | Tak |
| Precedencja | `!` > `&` > `|` |

---

## Testy

```bash
python run_tests.py
```

**Pokrycie:**
- E1: 4 testy (optymalne warunki)
- E2: 9 testów (pojedyncze średnie)
- E3: 7 testów (kombinacje)
- E4: 10 testów (wysokie zagrożenie)
- E5: 17 testów (krytyczne)

**Total: 47/47 ✅ (100% pass rate)**

---

## Licencja

MIT License - zobacz [LICENSE](LICENSE)

---

## Autorzy

- **Szymon Adamczyk** - Akademia Tarnowska
- **Bartłomiej Król** - Akademia Tarnowska

---

## Źródła

Projekt bazuje na artykule naukowym:
> Klimek, R. (2018). "Exploration of Human Activities Using Message Streaming Brokers and Automated Logical Reasoning"
> *IEEE Access*, vol. 6, pp. 27127-27139

---

**Gramatyka:** CFG Type-2 | **Parser:** ANTLR4 LL(*) | **Testy:** 47/47 (100%)

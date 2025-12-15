# Mountain Monitor

System monitorowania zagrożeń górskich dla GOPR - projekt akademicki.

**Kurs:** Języki formalne i kompilatory II
**Uczelnia:** Akademia Tarnowska
**Autorzy:** Szymon Adamczyk, Bartłomiej Król

---

## Quick Start

```bash
# Instalacja
pip install -r requirements.txt

# Testy (47 przypadków, 100% pass)
python run_tests.py

# Pojedynczy sygnał
python main.py --single "w3,f3,t1,r1,a1,d4"

# REPL interaktywny
python repl.py
```

---

## Format Sygnałów

`w[1-3],f[1-3],t[1-3],r[1-3],a[1-5],d[1-4]`

| Param | Opis |
|-------|------|
| `w` | Wiatr (1=słaby, 3=silny) |
| `f` | Mgła (1=brak, 3=gęsta) |
| `t` | Temperatura (1=normalna, 3=bardzo niska) |
| `r` | Deszcz (1=brak, 3=intensywny) |
| `a` | Ryzyko lawiny (1-5) |
| `d` | Trudność szlaku (1=łatwy, 4=bardzo trudny) |

---

## Poziomy Zagrożenia

| Poziom | Znaczenie |
|--------|-----------|
| **E1** | Bezpieczne |
| **E2** | Średnie zagrożenie |
| **E3** | Podwyższone |
| **E4** | Wysokie - tylko doświadczeni |
| **E5** | **ZAKAZ WSTĘPU** |

---

## Dokumentacja

- **[PROJEKT.md](PROJEKT.md)** - Kompletny opis (gramatyka, testy, prezentacja)
- **[docs/EBNF_FORMAL_SPEC.md](docs/EBNF_FORMAL_SPEC.md)** - Specyfikacja formalna
- **[grammar/ThreatRules.g4](grammar/ThreatRules.g4)** - Gramatyka ANTLR4
- **[data/rules.txt](data/rules.txt)** - Reguły zagrożeń

---

## Struktura

```
mountain-monitor/
├── grammar/ThreatRules.g4    # Gramatyka
├── src/                      # Kod źródłowy
├── data/rules.txt            # Reguły
├── main.py                   # CLI
├── repl.py                   # REPL
├── run_tests.py              # Testy
└── PROJEKT.md                # Dokumentacja
```

---

**Gramatyka:** CFG Type-2 | **Parser:** ANTLR4 LL(*) | **Testy:** 47/47 (100%)

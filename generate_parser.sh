#!/bin/bash
# Skrypt do generowania parsera ANTLR4 dla Linux/Mac
#
# WYMAGANIA:
#   1. Java JDK 11+ (java -version)
#   2. ANTLR4 JAR - pobierz z: https://www.antlr.org/download/antlr-4.13.1-complete.jar
#   3. Ustaw ANTLR_JAR lub umieść JAR w katalogu projektu
#
# Pobieranie ANTLR:
#   curl -O https://www.antlr.org/download/antlr-4.13.1-complete.jar

echo "========================================"
echo "Generowanie parsera ANTLR4..."
echo "========================================"

# Sprawdź czy ANTLR_JAR jest ustawiony
if [ -n "$ANTLR_JAR" ]; then
    ANTLR="$ANTLR_JAR"
elif [ -f "antlr-4.13.1-complete.jar" ]; then
    ANTLR="antlr-4.13.1-complete.jar"
else
    echo ""
    echo "ERROR: Nie znaleziono ANTLR JAR!"
    echo ""
    echo "Rozwiazanie:"
    echo "  1. Pobierz: https://www.antlr.org/download/antlr-4.13.1-complete.jar"
    echo "  2. Umiesc w katalogu projektu LUB ustaw ANTLR_JAR"
    echo ""
    exit 1
fi

echo "Uzywam ANTLR: $ANTLR"

# Usuń stary kod wygenerowany
if [ -d "src/parser/generated" ]; then
    echo "Usuwanie starego kodu..."
    rm -rf "src/parser/generated"
fi

# Utworz katalog na wygenerowany kod
mkdir -p "src/parser/generated"

# Generuj parser
echo "Generowanie parsera z gramatyki ThreatRules.g4..."
java -jar "$ANTLR" \
    -Dlanguage=Python3 \
    -visitor \
    -no-listener \
    -o src/parser/generated \
    grammar/ThreatRules.g4

if [ $? -ne 0 ]; then
    echo "ERROR: Generowanie nie powiodlo sie!"
    exit 1
fi

# Utworz __init__.py w katalogu generated
echo "# Generated ANTLR4 parser" > src/parser/generated/__init__.py

echo ""
echo "========================================"
echo "Parser wygenerowany pomyslnie!"
echo "Lokalizacja: src/parser/generated/"
echo "========================================"
echo ""

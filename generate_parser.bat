@echo off
REM Skrypt do generowania parsera ANTLR4 dla Windows
REM
REM WYMAGANIA:
REM   1. Java JDK 11+ (java -version)
REM   2. ANTLR4 JAR - pobierz z: https://www.antlr.org/download/antlr-4.13.1-complete.jar
REM   3. Ustaw ANTLR_JAR lub umieść JAR w katalogu projektu
REM
REM Pobieranie ANTLR:
REM   curl -O https://www.antlr.org/download/antlr-4.13.1-complete.jar

echo ========================================
echo Generowanie parsera ANTLR4...
echo ========================================

REM Sprawdź czy ANTLR_JAR jest ustawiony
if defined ANTLR_JAR (
    set ANTLR=%ANTLR_JAR%
) else if exist "antlr-4.13.1-complete.jar" (
    set ANTLR=antlr-4.13.1-complete.jar
) else (
    echo.
    echo ERROR: Nie znaleziono ANTLR JAR!
    echo.
    echo Rozwiazanie:
    echo   1. Pobierz: https://www.antlr.org/download/antlr-4.13.1-complete.jar
    echo   2. Umieść w katalogu projektu LUB ustaw ANTLR_JAR
    echo.
    exit /b 1
)

echo Uzywam ANTLR: %ANTLR%

REM Usuń stary kod wygenerowany
if exist "src\parser\generated" (
    echo Usuwanie starego kodu...
    rmdir /s /q "src\parser\generated"
)

REM Utworz katalog na wygenerowany kod
mkdir "src\parser\generated"

REM Generuj parser
echo Generowanie parsera z gramatyki ThreatRules.g4...
java -jar %ANTLR% ^
    -Dlanguage=Python3 ^
    -visitor ^
    -no-listener ^
    -o src\parser\generated ^
    grammar\ThreatRules.g4

if %errorlevel% neq 0 (
    echo ERROR: Generowanie nie powiodlo sie!
    exit /b 1
)

REM Utworz __init__.py w katalogu generated
echo # Generated ANTLR4 parser > src\parser\generated\__init__.py

echo.
echo ========================================
echo Parser wygenerowany pomyslnie!
echo Lokalizacja: src\parser\generated\
echo ========================================
echo.

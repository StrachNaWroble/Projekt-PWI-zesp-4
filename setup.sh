#!/bin/bash

# Ustawienie flagi błędu - przerwij jeśli którakolwiek komenda zwróci błąd
set -e

echo "=== Rozpoczynanie konfiguracji projektu ==="

cd src_cpp

# Upewnienie się, że skrypty są wykonywalne
chmod +x compile.sh link.sh gen_heu_tabs.sh

echo "[1/3] Kompilacja kodu C++..."
./compile.sh

echo "[2/3] Linkowanie pliku wykonywalnego..."
./link.sh

echo "[3/3] Generowanie tabel heurystyk (to może potrwać chwilę)..."
./gen_heu_tabs.sh

echo "=== Konfiguracja zakończona sukcesem! ==="
echo "Możesz teraz uruchomić program:"
echo "  python3 main.py"

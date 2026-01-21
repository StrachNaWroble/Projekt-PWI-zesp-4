# Projekt z PWI zespół 4
Tematem projektu jest program układający kostkę Rubika.

# Instrukcja Obsługi

## 1. Wymagania wstępne
- System Linux
- Python 3.x z bibliotekami: `tkinter`, `matplotlib`, `argparse`
- Kompilator G++
- Doxygen (opcjonalnie, do dokumentacji)

## 2. Instalacja i Kompilacja (Setup)
Po pobraniu repozytorium należy uruchomić skrypt konfiguracyjny, który skompiluje solver C++ oraz wygeneruje niezbędne tablice heurystyk (może to potrwać kilka minut).

```bash
./setup.sh
```

## 3. Uruchamianie Programu
Głównym punktem wejścia jest skrypt `main.py` w głównym katalogu.

### Tryb Terminalowy (CLI)
Najszybszy sposób na przetestowanie. Wymaga ręcznego wpisania kolorów ścianek.
```bash
python3 main.py --terminal
```
Program poprosi o wpisanie stanu 6 ścianek (U, D, F, B, L, R). Format wejściowy: ciąg 9 znaków (np. `WWWWWWWWW`) dla każdej ściany.
Dozwolone kolory: `W` (Biały), `Y` (Żółty), `B` (Niebieski), `G` (Zielony), `R` (Czerwony), `O` (Pomarańczowy).

### Tryb Graficzny (GUI)
Uruchamia okno z siatką do "wyklikania" kolorów.
```bash
python3 main.py
```

## 4. Generowanie Testów
W katalogu `src_cpp` znajduje się narzędzie do generowania trudniejszych, poprawnych stanów kostki.

Kompilacja i uruchomienie generatora:
```bash
g++ -Isrc_cpp/include src_cpp/gen_test_case.cpp src_cpp/cube.o -o gen_test_case
./gen_test_case
```

## 5. Dokumentacja
Dokumentacja techniczna kodu jest generowana przez Doxygen.
```bash
doxygen Doxyfile
cd documentation/latex && make
```
Plik wynikowy PDF: `documentation/latex/refman.pdf`

## 6. Notacja Ruchów
Szczegółowy opis notacji (co oznaczają symbole `F`, `R'`, `U2` itd.) znajduje się w pliku:
[RUCHY.md](RUCHY.md)

---

# Ramowy plan projektu:
1) Wczytanie danych (Python):
Użytkownik wprowadza stan początkowy kostki na interaktywnej planszy. Program sprawdza poprawność danych (m.in. zgodność liczby pól w danym kolorze). Po zatwierdzeniu generowany jest plik wejściowy .txt zawierający cyfrową reprezentację układu ścianek.

2) Warstwa algorytmiczna (C++): Program wczytuje wygenerowany plik, przetwarza dane i uruchamia algorytm rozwiązujący. Sekwencja ruchów zapisywana jest do osobnego pliku wynikowego .txt.

3) Wizualizacja rozwiązania (Python): Program odczytuje listę ruchów z pliku i prezentuje użytkownikowi instrukcję ułożenia kostki. 

Oraz przy 1) i 3) aspoekcie: możliwość wypisywania (i wczytywania) na standardowe wyjście


# Dane zespołu
Zespół 4, opiekun Piotr Ostropolski-Nalewaja, skład: 
359949 359409 351683 361008 360678 331060 [Python i C++]

### Struktura repozytorium
```text
/Projekt-PWI-zesp-4
│
├── main.py                 # Główny skrypt orkiestrujący (uruchamia CLI/GUI i Solver)
├── setup.sh                # Skrypt instalacyjny (kompilacja C++ i generowanie heurystyk)
├── README.md               # Dokumentacja projektu
├── Doxyfile                # Konfiguracja Doxygen
│
├── /data                   # Folder wymiany danych (pliki tymczasowe)
│   ├── cube_state.txt      # Stan kostki (Wejście dla C++)
│   ├── solution_steps.txt  # Kroki rozwiązania (Wyjście z C++)
│   └── *.txt               # Wygenerowane tablice heurystyk
│
├── /src_cpp                # Kod źródłowy C++ (Solver IDA*)
│   ├── main.cpp            # (C1) Ładuje dane, uruchamia solver
│   ├── cube.cpp / .h       # (C1) Logika kostki i ruchów
│   ├── ida_star.cpp / .h   # (C2) Algorytm IDA*
│   ├── gen_test_case.cpp   # Generator testowych stanów kostki
│   └── pliki .sh           # Skrypty kompilacji (wywoływane przez setup.sh)
│
├── /src_py                 # Kod źródłowy Python (GUI/CLI)
│   ├── input_gui.py        # (P1) Okno wprowadzania danych
│   ├── vis_gui.py          # (P2) Wizualizacja 3D (Matplotlib)
│   └── cli_handler.py      # (P3) Obsługa terminala
│
└── /documentation          # Dokumentacja wygenerowana przez Doxygen
```

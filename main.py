# @file main.py
# @brief Główny skrypt orkiestrujący działanie aplikacji.
# @details Odpowiada za wybór trybu wprowadzania danych (CLI/GUI),
#          uruchomienie solvera C++ oraz wizualizację wyników.

import argparse
import sys
import os
import subprocess
from pathlib import Path
import shutil
import tkinter as tk

# Ustawienie ścieżki bazowej (katalog projektu)
BASE_DIR = Path(__file__).resolve().parent

# Dodanie src_py do sys.path, aby importy działały
sys.path.append(str(BASE_DIR / "src_py"))

try:
    from cli_handler import SolverCLI, DATA_DIR, INPUT_FILE, OUTPUT_FILE
    import input_gui
except ImportError as e:
    print(f"Błąd krytyczny: Nie można zaimportować modułów z src_py. {e}")
    sys.exit(1)

CPP_EXEC = BASE_DIR / "src_cpp" / "main"
GUI_SCRIPT = BASE_DIR / "src_py" / "vis_gui.py"

##
# @brief Uruchamia solver napisany w C++.
# @details Wywołuje plik wykonywalny przekazując stan kostki przez stdin i zapisując wynik do stdout.
#          Ustawia katalog roboczy na src_cpp, aby solver poprawnie znalazł heurystyki w ../data.
# @return True jeśli solver zakończył się sukcesem, False w przeciwnym razie.
def run_cpp_solver():
    """Runs the C++ solver executable."""
    # Sprawdzenie pliku wykonywalnego
    if not CPP_EXEC.exists():
        print(f"Błąd: Nie znaleziono pliku wykonywalnego C++ w {CPP_EXEC}")
        print("Proszę uruchomić skrypt konfiguracyjny w głównym katalogu:")
        print("  ./setup.sh")
        return False

    # Sprawdzenie heurystyk
    heuristics = ["eph.txt", "eoh.txt", "cph.txt"]
    missing_heuristics = [h for h in heuristics if not (DATA_DIR / h).exists()]
    
    if missing_heuristics:
        print(f"Błąd: Brakuje plików heurystyk: {', '.join(missing_heuristics)}")
        print("Proszę uruchomić skrypt konfiguracyjny, aby je wygenerować:")
        print("  ./setup.sh")
        return False
    
    if not INPUT_FILE.exists():
        print(f"Błąd: Nie znaleziono pliku ze stanem kostki {INPUT_FILE}")
        return False
        
    print(f"\nUruchamianie solvera: {CPP_EXEC} < {INPUT_FILE} > {OUTPUT_FILE}")
    try:
        # Kod w C++ oczekuje uruchomienia z katalogu src_cpp, aby ścieżki ../data/ działały
        # Przekazujemy cube_state.txt jako stdin, solution_steps.txt jako stdout
        with open(INPUT_FILE, 'r') as stdin_f, open(OUTPUT_FILE, 'w') as stdout_f:
            subprocess.run(
                [str(CPP_EXEC)], 
                cwd=CPP_EXEC.parent, # Ustawiamy CWD na src_cpp
                stdin=stdin_f, 
                stdout=stdout_f, 
                check=True
            )
        return True
    except subprocess.CalledProcessError as e:
        print(f"Solver zakończył działanie z kodem błędu {e.returncode}")
        return False
    except OSError as e:
        print(f"Wykonanie nie powiodło się: {e}")
        return False

##
# @brief Uruchamia wizualizację rozwiązania.
# @details Kopiuje wynik solvera do pliku test.txt (wymagane przez vis_gui.py)
#          i uruchamia skrypt wizualizacji.
def run_gui():
    """Runs the visualization GUI."""
    print(f"\nUruchamianie wizualizacji...")
    if not GUI_SCRIPT.exists():
        print(f"Błąd: Nie znaleziono skryptu GUI w {GUI_SCRIPT}")
        return

    try:
        # Workaround dla vis_gui.py, który szuka 'test.txt' w CWD (teraz root)
        if OUTPUT_FILE.exists():
            shutil.copy(str(OUTPUT_FILE), "test.txt")
        else:
            print(f"Ostrzeżenie: Nie znaleziono pliku z rozwiązaniem {OUTPUT_FILE}. Wizualizacja może się nie udać.")
    except Exception as e:
        print(f"Nie udało się skopiować rozwiązania do test.txt: {e}")

    try:
        # Upewniamy się, że PYTHONPATH zawiera src_py dla subprocessa
        env = os.environ.copy()
        env["PYTHONPATH"] = str(BASE_DIR / "src_py") + ":" + env.get("PYTHONPATH", "")
        subprocess.run([sys.executable, str(GUI_SCRIPT)], check=True, env=env)
    except Exception as e:
        print(f"Nie udało się uruchomić GUI: {e}")

##
# @brief Główna funkcja programu.
# @details Parsuje argumenty wiersza poleceń, steruje przepływem danych
#          między modułami inputu, solvera i wizualizacji.
def main():
    parser = argparse.ArgumentParser(description="Rubik's Cube Solver Orchestrator")
    parser.add_argument('--terminal', "-t", action='store_true', help="Use terminal input mode")

    args = parser.parse_args()
    
    cube_state_ready = False
    
    if args.terminal:
        cli = SolverCLI()
        print("Uruchamianie trybu terminalowego...")
        # cli.run() executes the input loop and saves to file
        cli.run()
        if INPUT_FILE.exists():
            cube_state_ready = True
    else:
        print("Uruchamianie trybu graficznego (GUI)...")
        try:
            root = tk.Tk()
            root.minsize(600, 500)
            app = input_gui.InputGUI(root)
            root.mainloop()
            
            gui_output = Path.cwd() / "cube_input.txt"
            
            if gui_output.exists():
                print(f"GUI zamknięte. Przenoszenie {gui_output} do {INPUT_FILE}...")
                DATA_DIR.mkdir(exist_ok=True)
                shutil.move(str(gui_output), str(INPUT_FILE))
                cube_state_ready = True
            else:
                print("GUI zamknięte, ale nie znaleziono pliku wyjściowego (może anulowano?).")
                
        except Exception as e:
            print(f"Błąd uruchamiania GUI: {e}")
            print("Zalecane użycie trybu --terminal.")
        
    if cube_state_ready:
        if run_cpp_solver():
            print("Rozwiązanie wygenerowane.")
            run_gui()
        else:
            print("Pomijanie wizualizacji z powodu błędu solvera.")

if __name__ == "__main__":
    main()

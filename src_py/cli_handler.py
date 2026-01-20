## @file cli_handler.py
#  @brief Moduł obsługi interfejsu wiersza poleceń (CLI).
#  @details Odpowiada za pobranie danych od użytkownika, sformatowanie ich do specyfikacji
#           wymaganej przez silnik C++ oraz obsługę procesu.

import sys
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"
INPUT_FILE = DATA_DIR / "cube_state.txt"
OUTPUT_FILE = DATA_DIR / "solution_steps.txt"

# Definicja kolejności ścianek i dozwolonych kolorów
FACES_ORDER = ['U', 'D', 'F', 'B', 'L', 'R']
VALID_COLORS = {'W', 'Y', 'G', 'B', 'O', 'R'}

##
# @brief Klasa zarządzająca komunikacją CLI i integracją.
class SolverCLI:
    
    ##
    # @brief Inicjalizacja z domyślnym timeoutem.
    def __init__(self, timeout_sec=5.0):
        self.timeout = timeout_sec

    ##
    # @brief Formatuje surowy ciąg znaków do formatu wymaganego przez plik .txt.
    # @details Zamienia "WWWWWWWWW" na "U: W W W W W W W W W".
    # @param face Oznaczenie ścianki (np. 'U').
    # @param stickers Ciąg 9 znaków kolorów.
    # @return Sformatowany ciąg dla jednej ścianki.
    def _format_face_string(self, face, stickers):        
        rows = [stickers[i:i+3] for i in range(0, 9, 3)]
        formatted_rows = [" ".join(list(row)) for row in rows]
        
        # Pierwsza linia zawiera prefix "X: "
        result = f"{face}: {formatted_rows[0]}\n\n"
        result += f"{formatted_rows[1]}\n\n"
        result += f"{formatted_rows[2]}"
        
        return result

    ##
    # @brief Interaktywnie pobiera stan kostki od użytkownika.
    # @details Pyta oddzielnie o każdą z 6 ścianek, walidując długość i znaki.
    # @return Sformatowany ciąg gotowy do zapisu do pliku lub None w przypadku przerwania.
    def get_user_input(self):
        print("\n=== WPROWADZANIE STANU KOSTKI ===\n")
        print("Dozwolone kolory: B - Blue, G - Green, O - Orange, R - Red, W - White, Y - Yellow")
        
        # Mapowanie ścianka -> (Nazwa koloru, Oczekiwany kolor środka, Instrukcja perspektywy)
        face_info = {
            'U': ("White (Biała)", 'W', "Górna krawędź to krawędź z Niebieską (F)"),
            'D': ("Yellow (Żółta)", 'Y', "Górna krawędź to krawędź z Niebieską (F)"),
            'F': ("Blue (Niebieska)", 'B', "Górna krawędź to krawędź z Białą (U)"),
            'B': ("Green (Zielona)", 'G', "Górna krawędź to krawędź z Białą (U)"),
            'L': ("Red (Czerwona)", 'R', "Górna krawędź to krawędź z Białą (U)"),
            'R': ("Orange (Pomarańczowa)", 'O', "Górna krawędź to krawędź z Białą (U)")
        }
        
        try:
            while True:
                formatted_parts = []
                all_stickers = ""
                
                for face in FACES_ORDER:
                    color_name, expected_center, orientation_desc = face_info.get(face, ("Unknown", None, "Brak instrukcji"))
                    
                    print(f"\nŚcianka {face} [{color_name}]")
                    print(f"Perspektywa: {orientation_desc}")
                    
                    while True:
                        raw_input = input(f"Wpisz 9 znaków dla ścianki {face}: ").strip().upper()
                        
                        # Walidacja 1: Długość
                        if len(raw_input) != 9:
                            print(f"Błąd: Wymagane dokładnie 9 znaków. Wpisano {len(raw_input)}.")
                            continue
                        
                        # Walidacja 2: Poprawność znaków
                        invalid_chars = set(raw_input) - VALID_COLORS
                        if invalid_chars:
                            print(f"Błąd: Niedozwolone znaki: {invalid_chars}")
                            continue
                        
                        # Walidacja 3: Sprawdzenie środka
                        if raw_input[4] != expected_center:
                            print(f"Błąd: Środkowy element (znak nr 5) musi być koloru {color_name} ({expected_center}).")
                            continue
                        
                        formatted_parts.append(self._format_face_string(face, raw_input))
                        all_stickers += raw_input
                        break
                
                # Walidacja 4: Liczba kolorów
                counts = {c: all_stickers.count(c) for c in VALID_COLORS}
                incorrect_counts = {c: count for c, count in counts.items() if count != 9}
                
                if incorrect_counts:
                    print("\nBŁĄD: Niepoprawna liczba kolorów na kostce!")
                    print("Każdy kolor powinien wystąpić dokładnie 9 razy.")
                    print(f"Znaleziono: {counts}")
                    print("Proszę wprowadzić stan kostki ponownie.\n")
                    continue
                
                full_cube_state = "\n\n".join(formatted_parts)
                return full_cube_state

        except KeyboardInterrupt:
            sys.exit(0)

    ##
    # @brief Zapisuje sformatowany stan kostki do pliku.
    # @param cube_string Gotowy ciąg danych.
    # @return True jeśli zapis się powiódł.
    def save_to_file(self, cube_string):
        try:
            DATA_DIR.mkdir(exist_ok=True)
            with open(INPUT_FILE, 'w') as f:
                f.write(cube_string)
            print(f"\nZapisano plik wejściowy: {INPUT_FILE}")
            return True
        except IOError as e:
            print(f"Błąd zapisu pliku: {e}")
            return False
    
    ##
    # @brief Główna pętla aplikacji.
    def run(self):
        cube_data = self.get_user_input()
        if cube_data:
            if self.save_to_file(cube_data):
                # Tu będzie wywołanie self.run_cpp_solver()
                print("OK")

if __name__ == "__main__":
    cli = SolverCLI()
    cli.run()

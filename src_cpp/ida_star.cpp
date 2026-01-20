#include <bits/stdc++.h>
#include "cube.h"
#include "debug.h"
#include "eoh.h"
#include "eph.h"
#include "cph.h"

using namespace std;

typedef long long LL;

/// Stała reprezentująca „nieskończoność” używaną w IDA*
#define inf 1000000000

/**
 * @brief Lista wszystkich dozwolonych ruchów w fazie 1 algorytmu.
 *
 * Zawiera pełny zestaw obrotów ścian (90°, -90°, 180°).
 */
string moves1[20] = {
    "U", "Up", "U2",
    "D", "Dp", "D2",
    "R", "Rp", "R2",
    "L", "Lp", "L2",
    "F", "Fp", "F2",
    "B", "Bp", "B2"
};

/**
 * @brief Lista dozwolonych ruchów w fazie 2 algorytmu.
 *
 */
string moves2[10] = {
    "U", "Up", "U2",
    "D", "Dp", "D2",
    "R2", "L2", "F2", "B2"
};

/// Heurystyka orientacji krawędzi (Edge Orientation Heuristic)
eoh EOH;

/// Heurystyka pozycji narożników (Corner Permutation Heuristic)
cph CPH;

/// Heurystyka pozycji krawędzi (Edge Permutation Heuristic)
eph EPH;

/**
 * @brief Sprawdza, czy kostka jest rozwiązana w fazie 2.
 *
 */
bool is_goal_phase2(cube& c) {

    /// Sprawdzenie poprawności narożników
    for (int i = 0; i < 8; i++) {
        if (c.cp[i] != i) return false; // narożnik na złej pozycji
        if (c.co[i] != 0) return false; // niepoprawna orientacja narożnika
    }

    /// Sprawdzenie poprawności krawędzi
    for (int i = 0; i < 12; i++) {
        if (c.ep[i] != i) return false; // krawędź na złej pozycji
        if (c.eo[i] != 0) return false; // niepoprawna orientacja krawędzi
    }

    /// Wszystkie elementy są na właściwych miejscach
    return true;
}

/**
 * @brief Sprawdza, czy kostka spełnia warunki końcowe fazy 1.
 *
 */
bool is_goal_phase1(cube& c) {

    /// Sprawdzenie orientacji narożników
    for (int i = 0; i < 8; i++) {
        if (c.co[i] != 0)
            return false;
    }

    /// Sprawdzenie orientacji krawędzi
    for (int i = 0; i < 12; i++) {
        if (c.eo[i] != 0)
            return false;
    }

    /// Sprawdzenie, czy krawędzie UD znajdują się w warstwach UD
    for (int pos = 0; pos < 12; pos++) {
        int edge = c.ep[pos];

        bool is_ud_edge = (edge <= 3) || (edge >= 8); // krawędź typu UD
        bool is_ud_pos  = (pos  <= 3) || (pos  >= 8); // pozycja warstwy UD

        if (is_ud_edge && !is_ud_pos)
            return false;
    }

    return true;
}

/**
 * @brief Oblicza wartość heurystyki dla danego stanu kostki.
 *
 */
int getheuristic(cube &node, int stage){

    if(stage==1)
        return EOH.get_eoh(node); // heurystyka dla fazy 1

    /// Maksimum z heurystyk narożników i krawędzi w fazie 2
    return max(CPH.get_cph(node), EPH.get_eph(node));
}

/**
 * @brief Rekurencyjna funkcja przeszukiwania IDA*.
 *
 * @return Najmniejszy przekroczony koszt lub -1 jeśli znaleziono rozwiązanie
 */
int search(cube node, vector <string> &move_path, int price, int bound, int stage){

    int f = price + getheuristic(node, stage);

    /// Przekroczenie aktualnego limitu
    if(f > bound) return f;

    /// Sprawdzenie warunku końcowego
    if(stage==1 and is_goal_phase1(node)) return -1;
    if(stage==2 and is_goal_phase2(node)) return -1;

    int mint = inf;
    int move_count = (stage == 1 ? 18 : 10);

    /// Iteracja po dozwolonych ruchach
    for (int i = 0; i < move_count; i++){

        cube newcube = node;
        string new_move = (stage == 1 ? moves1[i] : moves2[i]);

        /// Eliminacja powtarzających się ruchów tej samej ściany
        if (!move_path.empty()) {
            if (new_move[0] == move_path.back()[0])
                continue;
        }

        /// Wykonanie ruchu
        newcube.move(new_move);
        move_path.push_back(new_move);

        int t = search(newcube, move_path, price+1, bound, stage);

        if(t == -1) return t;

        mint = min(mint, t);
        move_path.pop_back();
    }

    return mint;
}

/**
 * @brief Implementacja algorytmu IDA* dla danej fazy.
 *
 * @param root Stan początkowy kostki
 * @param stage Faza algorytmu (1 lub 2)
 * @return Para: (lista ruchów, głębokość rozwiązania)
 */
pair<vector<string>, int> ida_star(cube root, int stage){

    /// Początkowy limit oparty o heurystykę
    int bound = getheuristic(root, stage);

    vector <string> move_path;

    while(true){
        int t = search(root, move_path, 0, bound, stage);

        if(t == -1) return {move_path, bound};
        if(t >= inf) return {move_path, -1};

        bound = t;
    }
}


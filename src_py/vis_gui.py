## @file vis_gui.py
# @brief Moduł wizualizacyjny kostki Rubika 3D
# @details Moduł odpowiada za generowanie animacji kostki Rubika 3D na podstawie danych wejściowych.

import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
import time
from matplotlib.animation import FuncAnimation
import math

colour_map={
    'W': 'white',
    'Y': 'yellow',
    'G': 'green',
    'B': 'blue',
    'O': 'orange',
    'R': 'red'
}


## 
# @brief    wczytuje kolejne stany kostki z pliku tekstowego
# @details  Funkcja odczytuje dane z pliku i zamienia je na liste słowników.
#           Każdy stan jest zapisywany jako słownik zawierający sześć ścian (U, D, F, B, L, R),
#           z których każda opisana jest tablicą 3x3 kolorów 
# @param    filename Ścieżka do pliku tekstowego z danymi wejściowymi.
# @return   Lista słowników, gdzie każdy element opisuje jeden pełny stan kostki.
def load_data(filename):

    #  otworzenie pliku
    with open(filename, 'r') as f:
        lines = [line.strip() for line in f if line.strip() and not line.startswith('#')]

    moves=[] 
    # lista z kolejnymi ruchami
    i=0
    while i < len(lines): 
        if(lines[i]=="---"):
            i+=1
            continue

        cube={} 
        # tworzenie slownika w ktorym sa listy  np dla sciany 'U' trzymamy odwzorowanie jej 3x3  

        for wall in ['U', 'D', 'F', 'B', 'R', 'L']:
            cube[wall]=[] 
            cube[wall].append(lines[i][2:].strip().split())
            i+=1
            cube[wall].append(lines[i].strip().split())
            i+=1
            cube[wall].append(lines[i].strip().split())
            i+=1
        
        moves.append(cube)

    return moves


## 
# @brief    Buduje trójwymiarowy model kostki Rubika.
# @details  Funkcja tworzy listę 27 małych sześcianów na podstawie stanu kostki,
#           określając ich współrzędne oraz kolory widocznych ścian.
# @param    Słownik opisujący aktualny stan kostki
# @return   Lista krotek (x, y, z, colours), gdzie colours oznacza słownik kolorów ścian
def build_cube(cube_state):
    """
    Buduje listę 27 cubies zgodnie z wizją opisaną przez C++:
      - U (biała) = z == 2, D (żółta) = z == 0, F (niebieska) = y == 2
      - Dla ścian poza U/D ich 'górna' krawędź to krawędź z U (czyli widoczne rzędy są mapowane wg z)
      - Dla U i D ich 'górna' krawędź to krawędź z F (czyli widoczne rzędy są mapowane wg y)
    Zwraca listę krotek (x,y,z, colours), gdzie colours to słownik {face_letter: color_letter}.
    """
    cube = []
    # współrzędne:
    # x: 0 (L) .. 2 (R)
    # y: 0 (B) .. 2 (F)
    # z: 0 (D) .. 2 (U)

    for x in range(3):
        for y in range(3):
            for z in range(3):
                colours = {}

                # Górna i dolna: chcemy, żeby ich "górna" krawędź była krawędzią do frontu (F).
                # Dlatego wiersz w cube_state['U']/['D'] odpowiada 2 - y (y=2 -> pierwsza linia)
                if z == 2 and 'U' in cube_state:
                    colours['U'] = cube_state['U'][2 - y][x]
                if z == 0 and 'D' in cube_state:
                    colours['D'] = cube_state['D'][2 - y][2 - x]

                # Ściany boczne (F, B, L, R): ich "górna" krawędź to krawędź do U,
                # więc rząd odpowiada 2 - z (z=2 -> pierwsza linia)
                if y == 2 and 'F' in cube_state:
                    # F: kolumny zgodne z x (lewo->prawo = x=0..2)
                    colours['F'] = cube_state['F'][2 - z][2 - x]

                if y == 0 and 'B' in cube_state:
                    # B: potrzebne odbicie poziome względem x (bo to tylnia  ściana)
                    colours['B'] = cube_state['B'][2 - z][x]

                if x == 0 and 'L' in cube_state:
                    # L: lewa ściana, kolumny odpowiadają y, ale orientacja wymaga odbicia
                    colours['L'] = cube_state['L'][2 - z][2 - y]

                if x == 2 and 'R' in cube_state:
                    # R: prawa ściana, kolumny odpowiadają y bez odbicia
                    colours['R'] = cube_state['R'][2 - z][y]

                cube.append((x, y, z, colours))
    return cube

##
# @brief    Rysuje pojedynczy element kostki Rubika w przestrzeni 3D.
# @details  Funkcja rysuje ściany pojedynczego sześcianu na podanej osi 3D.
# param     ax Oś matplotlib 3D, na której rysowany jest sześcian.
# param     x Współrzędna x sześcianu
# param     y Współrzędna y sześcianu
# param     z Współrzędna z sześcianu
# param     colours Słownik kolorów widocznych ścian sześcianu.
# @return   Lista obiektów Poly3DCollection odpowiadających narysowanym ścianom.
def draw_cubie(ax, x, y, z, colours):
    walls = []

    if 'U' in colours:
        U = colours['U']
        walls.append([[x,y,z+1],[x+1,y,z+1],[x+1,y+1,z+1],[x,y+1,z+1], colour_map[U]])

    if 'D' in colours:
        D = colours['D']
        walls.append([[x,y,z],[x+1,y,z],[x+1,y+1,z],[x,y+1,z], colour_map[D]])

    if 'F' in colours:
        F = colours['F']
        walls.append([[x,y+1,z],[x+1,y+1,z],[x+1,y+1,z+1],[x,y+1,z+1], colour_map[F]])

    if 'B' in colours:
        B = colours['B']
        walls.append([[x,y,z],[x+1,y,z],[x+1,y,z+1],[x,y,z+1], colour_map[B]])

    if 'L' in colours:
        L = colours['L']
        walls.append([[x,y,z],[x,y+1,z],[x,y+1,z+1],[x,y,z+1], colour_map[L]])

    if 'R' in colours:
        R = colours['R']
        walls.append([[x+1,y,z],[x+1,y+1,z],[x+1,y+1,z+1],[x+1,y,z+1], colour_map[R]])

    # rysowanie wszystkich scian
    artists = []
    for vert in walls:
        poly = Poly3DCollection([vert[:4]], facecolors=vert[4], edgecolors='black')
        ax.add_collection3d(poly)
        artists.append(poly)
    return artists


##
# @brief    Aktualizuje pojedynczą klatkę animacji.
# @details  Dla podanej klatki czyści osie 
#           i rysuje aktualny stan kostki z czterech różnych perspektyw
# param     Numer aktualnej klatki
# return    Pusta lista, wymagana przez mechanizm FuncAnimation.
def update(frame): 
    # funkcja update koloruje kostke od nowa na kolory z ruchu ktory przetwarza z roznych perspektyw
    for idx, ax in enumerate(axes):
        ax.cla()
        cube_state = moves[frame]
        cube = build_cube(cube_state)
        artists = []
        for x, y, z, colours in cube:
            artists += draw_cubie(ax, x, y, z, colours)
        ax.set_xlim(0,3)
        ax.set_ylim(0,3)
        ax.set_zlim(0,3)
        ax.set_axis_off()
        ax.set_box_aspect([3,3,3])
        ax.set_proj_type('ortho')
        elevs = [30, 30, -30, -30]
        azims = [-60, -120, 60, 120]
        ax.view_init(elev=elevs[idx], azim=azims[idx])
        ax.set_title(f"Obraz {idx+1}")
    return []

moves = load_data("test.txt")  
# odczytywanie kolejnych stanów kostki


# tworzenie figury 3D

fig = plt.figure(figsize=(10,10))
axes=[
    fig.add_subplot(2,2,1, projection='3d'),
    fig.add_subplot(2,2,2, projection='3d'),
    fig.add_subplot(2,2,3, projection='3d'),
    fig.add_subplot(2,2,4, projection='3d')
]

# Utworzenie animacji na podstawie kolejnych stanów kostki

ani = FuncAnimation(fig, update, frames=len(moves), interval=1000)

# zapisywanie animacji do pliku wizualizacja_kostki.gif

ani.save("wizualizacja_kostki.gif", writer="pillow", fps=1)

# Wyświetlenie okna z animacją
plt.show()

# Notacja Ruchów Kostki Rubika

Ten plik opisuje standardową notację używaną przez program do opisu ruchów (rozwiązań). Jest to tzw. notacja Singmastera.

## Ścianki
Kostka ma 6 ścianek, oznaczonych literami od ich angielskich nazw:
- **U** (Up) – Górna (Biała)
- **D** (Down) – Dolna (Żółta)
- **F** (Front) – Przednia (Niebieska)
- **B** (Back) – Tylna (Zielona)
- **L** (Left) – Lewa (Czerwona)
- **R** (Right) – Prawa (Pomarańczowa)

*Uwaga: Kolory w nawiasach są kolorami domyślnymi używanymi w tym projekcie, przy założeniu standardowej orientacji (Biały góra, Niebieski przód).*

## Rodzaje ruchów

Każda litera oznacza obrót danej ścianki **zgodnie z ruchem wskazówek zegara** o 90 stopni (patrząc na wprost na daną ściankę).

### 1. Ruch podstawowy (np. `F`, `R`, `U`)
Obrót ścianki o 90 stopni zgodnie z ruchem wskazówek zegara.
- **F** – Przód w prawo
- **U** – Góra w lewo (patrząc od przodu)

### 2. Ruch odwrotny "Prime" (np. `F'`, `R'`, `U'`)
Obrót ścianki o 90 stopni **przeciwnie** do ruchu wskazówek zegara.
Często oznaczany apostrofem (np. `F'`) lub literą `i`.
**W tym programie ruchy te są oznaczane literą `p` (od słowa "prime"), np. `Up`, `Fp`, `Rp`.**
- **F'** (Fp) – Przód w lewo
- **U'** (Up) – Góra w prawo (patrząc od przodu)

### 3. Ruch podwójny (np. `F2`, `R2`, `U2`)
Obrót ścianki o 180 stopni (dwa ruchy 90 stopni).
Kierunek nie ma znaczenia (wynik jest ten sam).
- **F2** – Przód o 180 stopni

## Przykład
- **R U R' U'** – Prawa w górę, Góra w lewo, Prawa w dół, Góra w prawo.

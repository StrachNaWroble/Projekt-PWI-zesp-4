#!/bin/bash
echo Rozpoczęcie kompilacji: 
g++ -Iinclude -O3 cube.cpp -c 
g++ -Iinclude -O3 lehmer_code.cpp -c 
g++ -Iinclude -O3 eph_gen.cpp -c
g++ -Iinclude -O3 eoh_gen.cpp -c
g++ -Iinclude -O3 cph_gen.cpp -c

echo Zakończenie kompilacji i rozpoczęcie linkowania:
g++ -O3 cube.o lehmer_code.o eph_gen.o -o eph_gen
g++ -O3 cube.o lehmer_code.o eoh_gen.o -o eoh_gen
g++ -O3 cube.o lehmer_code.o cph_gen.o -o cph_gen
echo Zakończenie linkowania

echo Rozpoczęcie generowania tablicy eph:
./eph_gen >../data/eph.txt

echo Rozpoczęcie generowania tablicy eoh:
./eoh_gen >../data/eoh.txt

echo Rozpoczęcie generowania tablicy cph:
./cph_gen >../data/cph.txt

#rm *.o
rm cph_gen
rm eph_gen
rm eoh_gen


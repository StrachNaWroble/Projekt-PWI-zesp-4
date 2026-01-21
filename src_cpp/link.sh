#!/bin/bash
echo linkowanie
g++ -Iinclude ida_star.o eph.o cph.o eoh.o lehmer_code.o cube.o main.o -o main

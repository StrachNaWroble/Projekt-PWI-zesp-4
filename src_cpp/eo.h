#pragma once
#include "cube.h"
struct EO
{
	int eo[4096];
	EO();
	int get_eo(cube& state); 
};

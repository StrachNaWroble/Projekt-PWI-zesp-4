#pragma once
#include "cube.h"
struct eph
{
	int _eph[479001600];
	eph();
	int get_eph(cube& state);
};

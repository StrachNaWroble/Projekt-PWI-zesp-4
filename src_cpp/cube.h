#include<bits/stdc++.h>
using namespace std;
#define MOVES 4
class cube
{
public:
	array<char, 8> cp; //permutacja rogow
	array<char, 8> co; //orientacja rogow
	array<char, 12> ep; //permutacja krawedzi
	array<char, 12> eo; //orientacja krawedzi
	//kostka jest reprezentowana wzgledem orientacji: niebieski center z przodu, biały center u góry, pomarańczowy center z prawej
	cube();

	void move(int id);
};

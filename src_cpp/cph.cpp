#include "cube.h"
#include "cph.h"
#include "lehmer_code.h"
cph::cph()
{
	ifstream file("cph.txt");
	if(!file) 
	{
		cerr<<"Nie wygenerowane danych cph!\n";
		exit(0);
	}
	for(int i=0;i<40320;i++)
		file>>_cph[i];
}
int cph::get_cph(cube& state)
{
	return _cph[lehmer_code(state.cp)];	
}

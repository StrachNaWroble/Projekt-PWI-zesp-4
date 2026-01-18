#include "cube.h"
#include "eph.h"
#include "lehmer_code.h"
eph::eph()
{
	ifstream file("eph.txt");
	if(!file) 
	{
		cerr<<"Nie wygenerowane danych cph!\n";
		exit(0);
	}
	for(int i=0;i<479001600;i++)
		file>>_eph[i];
}
int eph::get_eph(cube& state)
{
	vector<int> ep(state.ep.begin(), state.ep.end());
	return _eph[lehmer_code(ep)];	
}

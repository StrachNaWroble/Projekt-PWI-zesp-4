#include "cube.h"
#include "eo.h"
EO::EO()
{
	ifstream data("eo.txt");
	if(!data)
	{
		cout<<"Dane heurystyki eo nie zostały wygenerowane!\n";
		return;
	}
	for(int i=0;i<4096;i++) data>>eo[i];
}
int EO::get_eo(cube& state)
{	
	auto to_int = [&](cube& obj)
	{
		int res = 0;
		for(int i=0;i<obj.eo.size();i++)
			res += obj.eo[i]*(1<<i);
		return res;
	};
	return eo[to_int(state)];
}

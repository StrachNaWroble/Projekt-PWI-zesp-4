#include "cube.h"
#include "eo.h"
int eo[4096];
void EO_load_table()
{
	ifstream data("eo.txt");
	if(!data)
	{
		cout<<"Dane heurystyki eo nie zostały wygenerowane!\n";
		return;
	}
	for(int i=0;i<4096;i++) cin>>eo[i];
}
int EO(cube& state)
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

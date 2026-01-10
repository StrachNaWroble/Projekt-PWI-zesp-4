#include "debug.h"
#include "cube.h"
int main()
{
	cube solved;
	queue<pair<cube, int> > q;
	q.push(make_pair(solved, 0));
	auto custom_hash = [&](cube& obj)
	{
		int res = 0;
		for(int i=0;i<obj.eo.size();i++)
			res += obj.eo[i]*(1<<i);
		return res;
	};
	vector<int> visited((1<<14), -1);
	while(!q.empty())
	{
		auto [akt, dist] = q.front();
		q.pop();
		visited[custom_hash(akt)] = dist;
		debug(akt.eo);
		debug(custom_hash(akt));
		for(int i=0;i<MOVES;i++)
		{
			cube nxt = akt;
			nxt.move(i);
			if(visited[custom_hash(nxt)] == -1)
				q.push(make_pair(nxt, dist+1));
		}
	}
	for(int i=0;i<visited.size();i++)
		cout<<visited[i]<<"\n";
}

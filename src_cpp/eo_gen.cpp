#include "debug.h"
#include "cube.h"
int main()
{
	cube solved;
	queue<pair<cube, int> > q;
	q.push(make_pair(solved, 0));
	auto to_int = [&](cube& obj)
	{
		int res = 0;
		for(int i=0;i<obj.eo.size();i++)
			res += obj.eo[i]*(1<<i);
		return res;
	};
	vector<int> opt((1<<14), 1e9);
	map<array<int, 12>, int> visited;
	int cnt = 0;
	while(!q.empty())
	{
		cnt++;
		if(cnt%100) debug(cnt);
		if(cnt > 10000000) break;
		auto [akt, dist] = q.front();
		q.pop();
		opt[to_int(akt)] = min(dist, opt[to_int(akt)]);
		visited[akt.ep] = 1;
		for(int i=0;i<MOVES;i++)
		{
			cube nxt = akt;
			nxt.move(i);
			if(visited[nxt.ep] == 0)
				q.push(make_pair(nxt, dist+1));
		}
	}
	for(int i=0;i<opt.size();i++)
		cout<<opt[i]<<"\n";
	for(int i=0;i<=4096;i++)
	{
		if(opt[i] == 1e9)
		{
			int s = 0;
			for(int j=0;j<20;j++) 
				if(i & (1<<j))
					s++;
			if(s%2 == 0)
			{
				cout<<":( "<<i;
				return 0;
			}
		}
	}
}

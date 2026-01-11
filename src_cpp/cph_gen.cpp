#include "debug.h"
#include "cube.h"
int main()
{
	cube state;
	vector<string> moves = {"U", "D", "R2", "L2", "F2", "B2"};
	queue<pair<cube, int> > q;
	q.push(make_pair(state, 0));
	auto custom_hash = [&](cube& obj) //kodowanie Lehmera
	{
		vector<bool> used(8, 0);
		vector<int> fact(8, 1);
		for(int i=2;i<8;i++)
			fact[i] = fact[i-1]*i;
		int res = 0;
		for(int i=0;i<8;i++)
		{
			int smaller = 0;
			for(int j=0;j<obj.cp[i];j++)
				if(!used[j]) smaller++;
			res += smaller * fact[7-i];
			used[obj.cp[i]] = true;
		}
		return res;
	};
	vector<int> distance(40320, -1);
	while(!q.empty())
	{
		auto [akt, dist] = q.front();
		q.pop();
		distance[custom_hash(akt)] = dist;
		for(auto& v : moves)
		{
			cube nw = akt;
			nw.move(v);
			if(distance[custom_hash(nw)] == -1)
			{
				distance[custom_hash(nw)] = dist+1;
				q.push(make_pair(nw, dist+1));
			}
		}
	}
	for(int i=0;i<40320;i++)
		cout<<distance[i]<<"\n";
}

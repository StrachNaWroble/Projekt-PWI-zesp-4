#include "debug.h"
#include "cube.h"
#include "lehmer_code.h"
int main()
{
	cube state;
	vector<string> moves = {"U", "D", "R2", "L2", "F2", "B2"};
	queue<pair<cube, int> > q;
	q.push(make_pair(state, 0));
	unordered_map<int, int> distance;
	while(!q.empty())
	{
		auto [akt, dist] = q.front();
		q.pop();
		vector<int> akt_ep(akt.ep.begin(), akt.ep.end());
		distance[lehmer_code(akt_ep)] = dist;
		for(auto& v : moves)
		{
			cube nw = akt;
			nw.move(v);
			vector<int> ep(nw.ep.begin(),nw.ep.end());
			if(distance.find(lehmer_code(ep)) == distance.end())
			{
				distance[lehmer_code(ep)] = dist+1;
				q.push(make_pair(nw, dist+1));
			}
		}
	}
	for(auto& [key, val] : distance)
		cout<<key<<" "<<val<<"\n";
}


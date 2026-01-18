#include "debug.h"
#include "cube.h"
#include "lehmer_code.h"
int main()
{
	cube state;
	vector<string> moves = {"U", "D", "R2", "L2", "F2", "B2"};
	queue<pair<cube, int> > q;
	q.push(make_pair(state, 0));
	vector<int> distance(40320, -1);
	while(!q.empty())
	{
		auto [akt, dist] = q.front();
		q.pop();
		distance[lehmer_code(akt)] = dist;
		for(auto& v : moves)
		{
			cube nw = akt;
			nw.move(v);
			if(distance[lehmer_code(nw)] == -1)
			{
				distance[lehmer_code(nw)] = dist+1;
				q.push(make_pair(nw, dist+1));
			}
		}
	}
	for(int i=0;i<40320;i++)
		cout<<distance[i]<<"\n";
}

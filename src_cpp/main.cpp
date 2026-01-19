#include "debug.h"
#include "cube.h"
#include "ida_star.h"
int main(int argc, char* argv[])
{
	if(argc == 1)
	{
		

		return 0;
	}
	if(argc == 2 && argv[1] == "--moves")
	{
		#ifndef DEBUG
		cout<<"Podaj liczbę ruchów: ";
		#endif
		int n;
		cin>>n;
		assert(0 <= n && n <= 1000);
		cube state;
		for(int i=0;i<n;i++)
		{
			#ifndef DEBUG
			cout<<"Podaj ruch: ";
			#endif
			string move;
			cin>>move;
			state.move(move);
		}
		#ifndef DEBUG
		cout<<"Rozpoczynanie fazy pierwszej\n";
		#endif
		auto solving_seq = ida_star(state, 1);
		#ifndef DEBUG
		cout<<"Zakończono fazę pierwszą\n";
		cout<<"Ruchy fazy pierwszej: \n";
		#endif
		for(auto& v : solving_seq.first)
			v.print();
		#ifndef DEBUG 
		cout<<"Rozpoczynanie fazy drugiej\n";
		#endif
		solving_seq = ida_star(state, 2);
		#ifndef DEBUG
		cout<<"Zakończenie fazy drugiej\n";
		cout<<"Ruchy fazy drugiej: \n";
		#endif	
		for(auto& v : solving_seq.first)
			v.print();
		return 0;
	}
	if(argc == 2 && argv[2] == "--state")
	{
		
		return 0;
	}
	cerr<<"Nie rozpoznano flag!\n";
}

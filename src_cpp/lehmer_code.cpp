#include "lehmer_code.h"
#include "cube.h"
#include <bits/stdc++.h>
int lehmer_code(cube& obj) //kodowanie Lehmera
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
}

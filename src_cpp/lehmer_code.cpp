#include "lehmer_code.h"
#include "cube.h"
#include <bits/stdc++.h>
int lehmer_code(vector<int> perm) //kodowanie Lehmera
{
	const unsigned int sz = perm.size();
	vector<bool> used(sz, 0);
	vector<int> fact(sz, 1);
	for(int i=2;i<sz;i++)
		fact[i] = fact[i-1]*i;
	int res = 0;
	for(int i=0;i<sz;i++)
	{
		int smaller = 0;
		for(int j=0;j<perm[i];j++)
			if(!used[j]) smaller++;
		res += smaller * fact[7-i];
		used[perm[i]] = true;
	}
	return res;
}

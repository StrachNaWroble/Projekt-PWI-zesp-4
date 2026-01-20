#include "lehmer_code.h"
#include "cube.h"
#include <bits/stdc++.h>
constexpr int fact[12] = {
    1, 1, 2, 6, 24, 120, 720, 5040,
    40320, 362880, 3628800, 39916800
};
int lehmer_code(vector<int>& perm) //kodowanie Lehmera
{
	const unsigned int sz = perm.size();
	int used = 0;
	int fact[sz];
	fact[0] = fact[1] = 1;
	for(int i=2;i<sz;i++)
		fact[i] = fact[i-1]*i;
	int res = 0;
	for(int i=0;i<sz;i++)
	{
		int p = perm[i];
		int smaller = p - __builtin_popcount(used & ((1<<p)-1));
	//	for(int j=0;j<perm[i];j++)
	//		if(!used[j]) smaller++;
		res += smaller * fact[sz-1-i];
		used |= (1<<p);
	}
	return res;
}

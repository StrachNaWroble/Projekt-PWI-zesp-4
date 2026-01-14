#include <bits/stdc++.h>
#include "cube.h"
#include "debug.h"
using namespace std;
typedef long long LL;

#define inf 1000

string moves[20]={
"U", "Up", "U2", 
"D", "Dp", "D2", 
"R", "Rp", "R2", 
"L", "Lp", "L2", 
"F", "Fp", "F2", 
"B", "Bp", "B2"
};

bool is_goal(cube& node) {

    // sprawdzamy narożniki
    for (int i = 0; i < 8; i++) {
        if (node.cp[i] != i) return false; // narożnik na złym miejscu
        if (node.co[i] != 0) return false; // złe ustawienie narożnika
    }

    // sprawdzamy krawędzie
    for (int i = 0; i < 12; i++) {
        if (node.ep[i] != i) return false; // krawędź na złym miejscu
        if (node.eo[i] != 0) return false; // złe ustawienie krawędzi
    }

    return true; // wszystko poprawnie
}


int search(vector <cube> &path, int price, int bound){

	cube node = path.back();
	
	int f = price + /*h(node)*/;
	
	if(f > bound) return f;
	if(is_goal(node)) return -1;

	int mint = inf;
	for (int i = 0; i < 18; i++){
		cube newcube=node;
		
		newcube.move(moves[i]);
		
		if (find(path.begin(), path.end(), newcube) != path.end())
    		continue;
    	
		path.push_back(newcube);

		int t = search(path, price+1, bound);
		if(t == -1) return t;
		mint = min(mint, t);
		
		path.pop_back();
	
	}
	return mint;
	
}

pair<vector<cube>, int> ida_star(cube root){

	int bound = h(root);
	vector <cube> path;
	path.push_back(root);
	
	while(true){
		int t = search(path, 0, bound);
		if(t == -1) return {path, bound};
		if(t >= inf) return {path, -1};
		bound = t;
	}
}

int main (){

	cube a, b;
	b=a;
	b.move("U");
	
	auto result = ida_star(a);
	if(result.second != -1){
    cout << "Found solution of length " << result.second << endl;
	}



	return 0;
}

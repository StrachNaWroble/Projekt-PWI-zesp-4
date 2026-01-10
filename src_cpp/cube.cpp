#include<bits/stdc++.h>
#include "cube.h"
using namespace std;
cube::cube()
{
	iota(cp.begin(), cp.end(), 0);
	iota(ep.begin(), ep.end(), 0);
	for(auto &v : co) v = 0;
	for(auto &v : eo) v = 0;
}
void cube::U() {
    int swp = cp[3];
    cp[3] = cp[2];
    cp[2] = cp[1];
    cp[1] = cp[0];
    cp[0] = swp;

    swp = ep[3];
    ep[3] = ep[2];
    ep[2] = ep[1];
    ep[1] = ep[0];
    ep[0] = swp;
}

void cube::D() {
    int swp = cp[7];
    cp[7] = cp[4];
    cp[4] = cp[5];
    cp[5] = cp[6];
    cp[6] = swp;

    swp = ep[11];
    ep[11] = ep[8];
    ep[8] = ep[9];
    ep[9] = ep[10];
    ep[10] = swp;

}

void cube::R() {
    co[2] = (co[2]+1)%3;
    co[3] = (co[3]+1)%3;
    co[6] = (co[6]+2)%3;
    co[7] = (co[7]+2)%3;

    int swp = cp[3];
    cp[3] = cp[2];
    cp[2] = cp[6];
    cp[6] = cp[7];
    cp[7] = swp;

    swp = ep[3];
    ep[3] = ep[7];
    ep[7] = ep[6];
    ep[6] = ep[11];
    ep[11] = swp;

}

void cube::L() {
    co[0] = (co[0]+2)%3;
    co[1] = (co[1]+2)%3;
    co[4] = (co[4]+1)%3;
    co[5] = (co[5]+1)%3;

    int swp = cp[0];
    cp[0] = cp[4];
    cp[4] = cp[5];
    cp[5] = cp[1];
    cp[1] = swp;

    swp = ep[0];
    ep[0] = ep[4];
    ep[4] = ep[5];
    ep[5] = ep[9];
    ep[9] = swp;

}

void cube::F() {
    co[0] = (co[0]+1)%3;
    co[3] = (co[3]+2)%3;
    co[4] = (co[4]+2)%3;
    co[7] = (co[7]+1)%3;

    int swp = cp[0];
    cp[0] = cp[4];
    cp[4] = cp[7];
    cp[7] = cp[3];
    cp[3] = swp;

    swp = ep[0];
    ep[0] = ep[4];
    ep[4] = ep[7];
    ep[7] = ep[3];
    ep[3] = swp;

    eo[0] ^= 1;
    eo[3] ^= 1;
    eo[4] ^= 1;
    eo[7] ^= 1;
}

void cube::B() {
    co[1] = (co[1]+1)%3;
    co[2] = (co[2]+2)%3;
    co[5] = (co[5]+2)%3;
    co[6] = (co[6]+1)%3;

    int swp = cp[1];
    cp[1] = cp[5];
    cp[5] = cp[6];
    cp[6] = cp[2];
    cp[2] = swp;

    swp = ep[1];
    ep[1] = ep[5];
    ep[5] = ep[6];
    ep[6] = ep[2];
    ep[2] = swp;

    eo[1] ^= 1;
    eo[2] ^= 1;
    eo[5] ^= 1;
    eo[6] ^= 1;
}

void cube::move(int id) {
    if(id==0) U();
    if(id==1) D();
    if(id==2) R();
    if(id==3) L();
    if(id==4) F();
    if(id==5) B();
}


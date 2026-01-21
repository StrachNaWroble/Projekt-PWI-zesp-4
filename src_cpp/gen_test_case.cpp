#include <iostream>
#include <vector>
#include <string>
#include <cstdlib>
#include <ctime>
#include "cube.h"

using namespace std;

int main() 
{
    cube c;
    
    vector<string> moves = {"R", "U", "F", "L", "B", "D"};
    
    cout << "Generowanie stanu po ruchach: ";
    for(const auto& m : moves) {
        cout << m << " ";
        c.move(m);
    }
    cout << "\n\n";
    
    c.print();

    return 0;
}

#include <iostream>
#include <fstream>
#include <string>
#include <sstream>
#include "SecondOrderSystem.h"

int main() {
    // Read parameters from file
    std::ifstream paramsFile("system_params.txt");
    double f, zeta, r;
    
    // Fast system parameters
    paramsFile >> f >> zeta >> r;
    SecondOrderSystem fastSystem(f, zeta, r);
    
    // Smooth system parameters
    paramsFile >> f >> zeta >> r;
    SecondOrderSystem smoothSystem(f, zeta, r);
    
    // Overshoot system parameters
    paramsFile >> f >> zeta >> r;
    SecondOrderSystem overshootSystem(f, zeta, r);

    const double target = 5.0;
    const double dt = 1.0/60.0;
    const int steps = 100;

    // Data collection
    std::ofstream dataFile("animation_data.csv");
    dataFile << "Frame,Fast,Smoothed,Overshoot\n";

    for(int i = 0; i < steps; ++i) {
        double fastPos = fastSystem.update(target, dt);
        double smoothPos = smoothSystem.update(target, dt);
        double overshootPos = overshootSystem.update(target, dt);
        
        dataFile << i << ","
                 << fastPos << ","
                 << smoothPos << ","
                 << overshootPos << "\n";
    }

    dataFile.close();
    return 0;
}
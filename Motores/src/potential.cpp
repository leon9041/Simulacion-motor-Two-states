#include "Potential.h"
#include <cmath>

// Implementación de U(x) = 0.5 * k * (x - x_min)^2
double HarmonicPotential::U(double x) const {
    double dx = x - x_min;
    return 0.5 * k * dx * dx;
}

// Implementación de F(x) = -dU/dx = -k * (x - x_min)
double HarmonicPotential::F(double x) const {
    return -k * (x - x_min);
}
#include "ChemicalState.h"
#include <cmath>

ChemicalState::ChemicalState(double t_off, double t_on)
    : s(0), T_off(t_off), T_cycle(t_on + t_off) {}

// Implementación determinista de conmutación de estado
void ChemicalState::update(double t, double dt) {
    // Si el tiempo dentro del ciclo es menor a T_off, estamos en estado 0.
    if (std::fmod(t, T_cycle) < T_off) {
        s = 0; // U0 activo
    } else {
        s = 1; // U1 activo
    }
}
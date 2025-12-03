#include "MotorModel.h"
#include <random>
#include <iostream>

// Inicializar el generador de números aleatorios para la simulación
static std::random_device rd;
static std::mt19937 generator(rd());
// Distribución Gaussiana estándar (media 0, desviación estándar 1)
static std::normal_distribution<> normal_dist(0.0, 1.0); 

// CONSTRUCTOR MODIFICADO - k0 y k1 separados
MotorModel::MotorModel(double mass, double k0, double k1, double l, double t_off, double t_on, 
                       double gamma_val, double kBT_val, double initial_x, double initial_v)
    // Inicialización de miembros
    : p(mass, initial_x, initial_v), 
      chemicalState(t_off, t_on),
      U0(k0, 0.0),   // Estado 0: potencial en x=0 con constante k0
      U1(k1, l),     // Estado 1: potencial en x=l con constante k1
      gamma(gamma_val), 
      kBT(kBT_val)
{
    currentPotential = &U0;
    std::cout << "Motor creado:" << std::endl;
    std::cout << "  - Estado 0: U0(k=" << k0 << ", x_min=0.0)" << std::endl;
    std::cout << "  - Estado 1: U1(k=" << k1 << ", x_min=" << l << ")" << std::endl;
}

void MotorModel::updateChemicalState(double t, double dt) {
    chemicalState.update(t, dt);

    if (chemicalState.getState() == 0) {
        currentPotential = &U0;
    } else {
        currentPotential = &U1;
    }
}

// Retorna solo la fuerza determinista del potencial (F(x,t)).
// La fricción y el ruido se manejan en el Integrador.
double MotorModel::force(double t) const {
    return currentPotential->F(p.x); 
}

// Nueva función para generar el ruido estocástico
double MotorModel::generateGaussianNoise() const {
    return normal_dist(generator);
}

// DEFINICIÓN de la función getPotentialEnergy()
double MotorModel::getPotentialEnergy() const {
    return currentPotential->U(p.x);
}

// DEFINICIONES de los métodos para parámetros de Langevin
double MotorModel::getGamma() const { return gamma; }
double MotorModel::getKBT() const { return kBT; }
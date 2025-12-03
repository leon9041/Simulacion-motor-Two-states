#ifndef MOTORMODEL_H
#define MOTORMODEL_H

#include "Particle.h"
#include "Potential.h"
#include "ChemicalState.h"

class MotorModel {
private:
    Particle p;
    Potential* currentPotential;
    ChemicalState chemicalState;
    HarmonicPotential U0;  // Potencial para estado 0 (unión débil)
    HarmonicPotential U1;  // Potencial para estado 1 (unión fuerte)
    double gamma, kBT;

public:
    // Constructor con k0 y k1 separados
    MotorModel(double mass, double k0, double k1, double l, double t_off, double t_on, 
               double gamma_val, double kBT_val, double initial_x = 0.0, double initial_v = 0.0);
    
    double force(double t = 0.0) const;
    void updateChemicalState(double t, double dt);
    double getPotentialEnergy() const; 
    
    // Métodos de acceso
    Particle& getParticle() { return p; }
    int getCurrentState() const { return chemicalState.getState(); }

    // Métodos para parámetros de Langevin
    double getGamma() const;
    double getKBT() const;
    double generateGaussianNoise() const;
};

#endif // MOTORMODEL_H
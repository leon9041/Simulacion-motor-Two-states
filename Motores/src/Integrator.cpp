#include "Integrator.h"
#include "MotorModel.h"
#include <cmath> // Necesario para exp y sqrt

// Implementación de Stochastic Velocity Verlet (tipo BAOAB)
// Este método integra la Ecuación de Langevin correctamente.
void StochasticVelocityVerletIntegrator::step(MotorModel& motor, double dt) {
    Particle& p = motor.getParticle();
    double m = p.m;
    double gamma = motor.getGamma();
    double kBT = motor.getKBT();
    
    // --- Coeficientes del paso de Fricción/Ruido (A) ---
    // c1: Factor de amortiguamiento de la fricción (Friction factor)
    double c1 = std::exp(-gamma * dt);
    // sigma: Amplitud del ruido Gaussiano (Noise amplitude)
    // Se asegura la relación Fluctuation-Dissipation: sigma = sqrt(kBT * (1-c1^2))
    double sigma = std::sqrt(kBT * (1.0 - c1 * c1));

    // --- 1. Paso B (Force Half-Step) ---
    // Aplicar la mitad de la fuerza determinista (potencial)
    double F_old = motor.force(0.0);
    p.v += F_old / m * (0.5 * dt);

    // --- 2. Paso A (Friction & Noise) ---
    // Aplicar fricción y ruido (Movement, Friction, Noise)
    double R_t = motor.generateGaussianNoise(); // Ruido Gaussiano
    p.v = c1 * p.v + sigma * R_t / std::sqrt(m);

    // --- 3. Paso O (Position Full-Step) ---
    // Actualizar la posición
    p.x += p.v * dt;

    // --- 4. Paso B (Force Half-Step) ---
    // Recalcular la fuerza con la nueva posición y aplicar la otra mitad
    // Nota: El potencial ya fue conmutado por updateChemicalState() en Simulator.run()
    double F_new = motor.force(0.0);
    p.v += F_new / m * (0.5 * dt);
}
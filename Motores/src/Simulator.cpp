/**
 * @file     Simulator.cpp
 * @brief    simulacion de motor molecular de dos estados con velocity-verlet
 * @author   Angie Gomez, Leonardo Tovar
 * @date     02/12/25
 * @version  1.0
 * @license  owner
 */
#include "Simulator.h"
#include "MotorModel.h"
#include "Integrator.h"
#include <stdexcept>
#include <cmath>

Simulator::Simulator(MotorModel& m, Integrator& i, double T_t, double delta_t, const std::string& filename)
    : motor(m), integrator(i), T_total(T_t), dt(delta_t)
{
    // Crear directorio si no existe
    system("mkdir -p results");
    
    data_file.open(filename);
    if (!data_file.is_open()) {
        throw std::runtime_error("No se pudo abrir el archivo de salida para la simulación.");
    }
    // Encabezado para el archivo de datos
    data_file << "# t\tx\tv\ts\tE_total\n";
}

void Simulator::logData(double t) {
    const Particle& p = motor.getParticle();
    int s = motor.getCurrentState();
    
    double E_kin = p.getKineticEnergy();
    // Uso del método corregido
    double E_pot = motor.getPotentialEnergy(); 
    
    // Escribe las columnas: t, x, v, s, E_total
    data_file << t << "\t" << p.x << "\t" << p.v << "\t" << s << "\t" << (E_kin + E_pot) << "\n";
}

void Simulator::run() {
    double t = 0.0;
    while (t < T_total) {
        // 1. Actualizar el estado químico (U0 o U1)
        motor.updateChemicalState(t, dt);
        
        // 2. Registrar el estado actual
        logData(t);
        
        // 3. Integrar un paso de tiempo
        integrator.step(motor, dt);
        
        t += dt;
    }
    
    data_file.close();

}

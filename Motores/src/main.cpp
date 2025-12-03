/**
 * @file     main.cpp
 * @brief    simulacion de motor molecular de dos estados con velocity-verlet
 * @author   Angie Gomez, Leonardo Tovar
 * @date     02/12/25
 * @version  1.0
 * @license  owner
 */
#include "MotorModel.h"
#include "Integrator.h"
#include "Simulator.h"
#include <iostream>
#include <stdexcept>

int main() {
    std::cout << "Iniciando simulacion del Motor de Dos Estados (Langevin-Verlet Estocástico)...\n";

    // --- PARAMETROS FISICOS ---
    double m = 1.0;         // Masa de la partícula
    
    // Constantes elásticas diferentes para cada estado
    double k0 = 10.0;        // Estado 0: Unión débil (potencial suave)
    double k1 = 10.0;       // Estado 1: Unión fuerte (potencial rígido)
    
    double l = 0.5;         // Desplazamiento del mínimo para U1
    double T_off = 2;     // Duración del estado 0 (unión débil)
    double T_on = 2;      // Duración del estado 1 (unión fuerte)
    
    // --- PARAMETROS DE LANGEVIN ---
    double gamma = 10.0;    // Coeficiente de fricción
    double kBT = 0.01;      // Energía térmica
    
    // --- PARAMETROS DE SIMULACION ---
    double T_total = 10.0;  // Tiempo total
    double dt = 0.001;      // Paso de tiempo

    // --- CONDICIONES INICIALES ---
    double initial_x = l / 2.0; 
    double initial_v = 0.0;     

    try {
        // Crear modelo con constantes diferentes
        MotorModel motor(m, k0, k1, l, T_off, T_on, gamma, kBT, initial_x, initial_v);
        
        StochasticVelocityVerletIntegrator pv_integrator; 
        
        Simulator simulator(motor, pv_integrator, T_total, dt, "results/datos_motor_dos_estados_langevin.txt");
        simulator.run();
        
        std::cout << "Simulacion completada. Datos guardados en results/datos_motor_dos_estados_langevin.txt\n";
        
    } catch (const std::exception& e) {
        std::cerr << "Error en la simulacion: " << e.what() << std::endl;
        return 1;
    } catch (...) {
        std::cerr << "Error desconocido durante la simulación." << std::endl;
        return 1;
    }

    return 0;

}

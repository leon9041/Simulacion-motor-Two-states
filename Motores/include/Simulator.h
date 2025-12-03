#ifndef SIMULATOR_H
#define SIMULATOR_H

#include <fstream>
#include <string>

class MotorModel;
class Integrator;

class Simulator {
private:
    MotorModel& motor;
    Integrator& integrator;
    double T_total;
    double dt;
    std::ofstream data_file;

public:
    Simulator(MotorModel& m, Integrator& i, double T_t, double delta_t, const std::string& filename);
    void run();
    void logData(double t);
};

#endif // SIMULATOR_H
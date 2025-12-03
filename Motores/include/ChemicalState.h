#ifndef CHEMICALSTATE_H
#define CHEMICALSTATE_H

class ChemicalState {
private:
    int s;          // Estado químico actual (0 o 1)
    double T_off;   // Duración del estado 0
    double T_cycle; // T_off + T_on

public:
    ChemicalState(double t_off, double t_on);
    void update(double t, double dt);
    int getState() const { return s; }
};

#endif // CHEMICALSTATE_H
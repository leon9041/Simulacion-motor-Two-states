#ifndef PARTICLE_H
#define PARTICLE_H

class Particle {
public:
    double x, v, m;
    Particle(double mass, double initial_x = 0.0, double initial_v = 0.0)
        : x(initial_x), v(initial_v), m(mass) {}
    double getKineticEnergy() const { return 0.5 * m * v * v; }
};

#endif // PARTICLE_H
#ifndef POTENTIAL_H
#define POTENTIAL_H

class Potential {
public:
    virtual double U(double x) const = 0;
    virtual double F(double x) const = 0;
    virtual ~Potential() {}
};

class HarmonicPotential : public Potential {
private:
    double k, x_min;
public:
    HarmonicPotential(double elastic_k, double minimum_pos) : k(elastic_k), x_min(minimum_pos) {}
    double U(double x) const override;
    double F(double x) const override;
};

#endif // POTENTIAL_H
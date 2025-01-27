#pragma once

class SecondOrderSystem {
public:
    SecondOrderSystem(double f, double zeta, double r, double initial_position = 0.0);
    
    double update(double target_position, double delta_time);
    
    void setParameters(double f, double zeta, double r);
    void setNaturalFrequency(double f);
    void setDamping(double zeta);
    void setResponse(double r);

private:
    void recalculateCoefficients();
    
    // System parameters
    double m_f;
    double m_zeta;
    double m_r;
    
    // System state
    double m_position;
    double m_velocity;
    double m_prev_input;
    
    // Derived coefficients
    double m_k1;
    double m_k2;
    double m_k3;
    double m_T_crit;
};
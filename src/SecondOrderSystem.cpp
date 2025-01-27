#include "SecondOrderSystem.h"
#include <cmath>

SecondOrderSystem::SecondOrderSystem(double f, double zeta, double r, double initial_position)
    : m_f(f), m_zeta(zeta), m_r(r),
      m_position(initial_position), m_velocity(0.0),
      m_prev_input(initial_position) {
    recalculateCoefficients();
}

void SecondOrderSystem::recalculateCoefficients() {
    m_k2 = 1.0 / std::pow(2.0 * M_PI * m_f, 2);
    m_k1 = 2.0 * m_zeta * std::sqrt(m_k2);
    m_k3 = (m_r * m_k1) / 2.0;
    
    // Calculate critical time step for stability
    m_T_crit = std::sqrt(4.0 * m_k2 + m_k1 * m_k1) - m_k1;
}

double SecondOrderSystem::update(double target_position, double delta_time) {
    // Estimate input velocity using finite differences
    double input_velocity = (target_position - m_prev_input) / delta_time;
    
    // Semi-implicit Euler integration
    // 1. Update position using current velocity
    double new_position = m_position + m_velocity * delta_time;
    
    // 2. Calculate acceleration using updated position
    double acceleration = (target_position + m_k3 * input_velocity
                          - new_position - m_k1 * m_velocity) / m_k2;
    
    // 3. Update velocity using calculated acceleration
    double new_velocity = m_velocity + acceleration * delta_time;
    
    // Store state for next iteration
    m_position = new_position;
    m_velocity = new_velocity;
    m_prev_input = target_position;
    
    return m_position;
}

// Parameter setters
void SecondOrderSystem::setParameters(double f, double zeta, double r) {
    m_f = f;
    m_zeta = zeta;
    m_r = r;
    recalculateCoefficients();
}

void SecondOrderSystem::setNaturalFrequency(double f) {
    m_f = f;
    recalculateCoefficients();
}

void SecondOrderSystem::setDamping(double zeta) {
    m_zeta = zeta;
    recalculateCoefficients();
}

void SecondOrderSystem::setResponse(double r) {
    m_r = r;
    recalculateCoefficients();
}
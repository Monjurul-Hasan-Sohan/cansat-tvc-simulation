# -*- coding: utf-8 -*-
"""
Last Update on Fri May  2 19:34:56 2025

@author: Monjurul Hasan Bhuiyan
"""

class PIDController:
    def __init__(self, Kp, Ki, Kd, setpoint, dt):
        self.Kp = Kp
        self.Ki = Ki
        self.Kd = Kd
        self.setpoint = setpoint
        self.dt = dt
        self.integral = 0
        self.prev_error = 0

    def compute(self, measurement):
        error = self.setpoint - measurement
        self.integral += error * self.dt
        derivative = (error - self.prev_error) / self.dt
        output = self.Kp * error + self.Ki * self.integral + self.Kd * derivative
        self.prev_error = error
        return output
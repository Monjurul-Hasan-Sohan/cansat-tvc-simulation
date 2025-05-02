# -*- coding: utf-8 -*-
"""
Last Update on Fri May  2 19:39:46 2025

@author: Monjurul Hasan bhuiyan
"""

import numpy as np

class TVCDynamics:
    def __init__(self):
        self.I = 0.1  # Moment of inertia (kg·m²)
        self.dt = 0.01
        self.orientation = np.zeros(3)  # [pitch, yaw, roll]
        
    def update(self, control_input, disturbance=0):
        torque = control_input + disturbance
        angular_accel = torque / self.I
        self.orientation += angular_accel * self.dt
        return self.orientation.copy()
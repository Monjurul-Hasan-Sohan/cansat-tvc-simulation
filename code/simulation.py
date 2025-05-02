# -*- coding: utf-8 -*-
"""
CanSat TVC Simulation System
Last Modified: Fri May  2 19:45:00 2025
"""

import numpy as np
import matplotlib.pyplot as plt
import os
from datetime import datetime
from pid_controller import PIDController
from system_dynamics import TVCDynamics

def run_simulation(setpoint, duration, disturbance_func=None, Kp=1.2, Ki=0.01, Kd=0.05):
    dt = 0.01
    steps = int(duration/dt)
    time = np.arange(0, duration, dt)
    
    controller = PIDController(Kp, Ki, Kd, setpoint, dt)
    system = TVCDynamics()
    
    orientations = np.zeros((steps, 3))
    outputs = np.zeros(steps)
    
    for i in range(steps):
        disturbance = disturbance_func(time[i]) if disturbance_func else 0
        control_output = controller.compute(system.orientation[0])
        orientation = system.update(control_output, disturbance)
        
        orientations[i] = orientation
        outputs[i] = control_output
        
    return time, orientations, outputs

def plot_results(time, orientations, outputs, filename, scenario_name=""):
    plt.style.use('seaborn-v0_8-darkgrid')
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 8), sharex=True)
    
    # Orientation plot
    ax1.plot(time, orientations[:, 0], 'b-', lw=2, label='Pitch')
    ax1.plot(time, orientations[:, 1], 'r--', lw=2, label='Yaw')
    ax1.plot(time, orientations[:, 2], 'g-.', lw=2, label='Roll')
    ax1.set_ylabel('Orientation (rad)', fontsize=12)
    ax1.legend(loc='upper right', frameon=True)
    ax1.set_title(f'CanSat TVC Response: {scenario_name}', fontsize=14)
    
    # Control output plot
    ax2.plot(time, outputs, 'k-', lw=2, label='Control Output')
    ax2.set_xlabel('Time (s)', fontsize=12)
    ax2.set_ylabel('Thrust Command', fontsize=12)
    ax2.legend(loc='upper right')
    
    plt.tight_layout()
    plt.savefig(filename, dpi=300, bbox_inches='tight')
    plt.close()

def simulate_scenarios():
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_dir = f"simulations/{timestamp}"
    os.makedirs(output_dir, exist_ok=True)
    
    # Scenario 1: Step Response
    print("Running step response test...")
    time, orient, out = run_simulation(setpoint=0.5, duration=5)
    plot_results(time, orient, out, 
               f"{output_dir}/step_response.png",
               "Step Response (0.5 rad)")
    
    # Scenario 2: Wind Disturbance
    print("Running wind disturbance test...")
    def wind(t):
        return 0.3 * np.sin(2*t) if 1 < t < 4 else 0
    
    time, orient, out = run_simulation(setpoint=0, duration=10, 
                                     disturbance_func=wind)
    plot_results(time, orient, out,
               f"{output_dir}/wind_disturbance.png",
               "Wind Disturbance Rejection")
    
    print(f"\nSimulation outputs saved to: {output_dir}")
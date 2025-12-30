#!/usr/bin/env python3
"""
Generate sample torque measurement data for a rotating pulley.
Simulates a 25 Hz dominant forcing frequency with some noise.
"""
import numpy as np
import pandas as pd

def generate_torque_data():
    # Sampling parameters
    fs = 1000.0          # sampling frequency [Hz]
    T = 1.0              # total duration [s]
    N = int(fs * T)      # number of samples
    t = np.linspace(0, T, N, endpoint=False)
    
    # Signal composition
    # Dominant forcing frequency at 25 Hz (pulley rotation/blade engagement)
    f1 = 25.0
    A1 = 100.0           # amplitude [Nm]
    # Secondary frequency at 60 Hz (motor harmonics)
    f2 = 60.0
    A2 = 15.0
    # Random noise
    noise = np.random.normal(0, 5.0, N)
    
    torque = A1 * np.sin(2 * np.pi * f1 * t) + A2 * np.sin(2 * np.pi * f2 * t) + noise
    
    # Create DataFrame
    df = pd.DataFrame({'Time (s)': t, 'Torque (Nm)': torque})
    return df

if __name__ == '__main__':
    df = generate_torque_data()
    df.to_csv('../data/pulley_torque_data.csv', index=False)
    print(f"Generated {len(df)} samples saved to ../data/pulley_torque_data.csv")
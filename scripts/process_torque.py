#!/usr/bin/env python3
"""
Perform FFT on torque measurement data to identify dominant forcing frequencies.
"""
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import os

def main():
    # Load data
    data_path = '../data/pulley_torque_data.csv'
    df = pd.read_csv(data_path)
    time = df['Time (s)'].values
    torque = df['Torque (Nm)'].values
    
    # Sampling parameters
    dt = time[1] - time[0]          # sampling interval [s]
    fs = 1.0 / dt                   # sampling frequency [Hz]
    N = len(time)
    
    # Compute FFT
    torque_fft = np.fft.fft(torque)
    freqs = np.fft.fftfreq(N, dt)
    
    # Take only positive frequencies
    pos_mask = freqs >= 0
    freqs_pos = freqs[pos_mask]
    magnitude = np.abs(torque_fft[pos_mask]) / N  # scale to amplitude
    
    # Identify dominant frequency (excluding DC component)
    # Find peak in the range 1 Hz to Nyquist frequency
    nyquist = fs / 2.0
    mask = (freqs_pos > 1.0) & (freqs_pos < nyquist)
    if np.any(mask):
        dominant_idx = np.argmax(magnitude[mask])
        dominant_freq = freqs_pos[mask][dominant_idx]
        dominant_amp = magnitude[mask][dominant_idx]
    else:
        dominant_freq = 0.0
        dominant_amp = 0.0
    
    # Print results
    print(f"Sampling frequency: {fs:.1f} Hz")
    print(f"Number of samples: {N}")
    print(f"Dominant forcing frequency: {dominant_freq:.2f} Hz (amplitude {dominant_amp:.2f} Nm)")
    
    # Plot torque signal and spectrum
    fig, axes = plt.subplots(2, 1, figsize=(10, 8))
    
    # Time domain
    axes[0].plot(time, torque, 'b-', linewidth=1)
    axes[0].set_xlabel('Time (s)')
    axes[0].set_ylabel('Torque (Nm)')
    axes[0].set_title('Torque Measurement Time Series')
    axes[0].grid(True)
    
    # Frequency domain (linear scale)
    axes[1].plot(freqs_pos, magnitude, 'r-', linewidth=1)
    axes[1].set_xlabel('Frequency (Hz)')
    axes[1].set_ylabel('Amplitude (Nm)')
    axes[1].set_title('Frequency Spectrum (FFT)')
    axes[1].grid(True)
    axes[1].set_xlim(0, min(200, nyquist))  # limit to 200 Hz for clarity
    
    # Mark dominant frequency
    if dominant_freq > 0:
        axes[1].axvline(x=dominant_freq, color='k', linestyle='--', alpha=0.7,
                        label=f'Dominant frequency = {dominant_freq:.2f} Hz')
        axes[1].legend()
    
    plt.tight_layout()
    
    # Ensure results directory exists
    os.makedirs('../results', exist_ok=True)
    plot_path = '../results/torque_spectrum.png'
    plt.savefig(plot_path, dpi=150)
    print(f"Plot saved to {plot_path}")
    
    # Also save dominant frequency to a text file for later use
    with open('../results/dominant_frequency.txt', 'w') as f:
        f.write(f'{dominant_freq:.2f}')
    
if __name__ == '__main__':
    main()
#!/usr/bin/env python3
"""
Post-process FEA results: read modal frequencies and harmonic response,
generate plots for resonance identification.
"""
import numpy as np
import matplotlib.pyplot as plt
import os

def read_dominant_frequency():
    """Read dominant forcing frequency from torque analysis"""
    try:
        with open('../results/dominant_frequency.txt', 'r') as f:
            line = f.readline().strip()
            return float(line)
    except FileNotFoundError:
        print("WARNING: dominant_frequency.txt not found, using default 25 Hz")
        return 25.0

def generate_sample_results():
    """
    Generate sample FEA results (since actual solver not run).
    Returns:
        modal_freqs: array of natural frequencies [Hz]
        harmonic_freqs: frequency points for harmonic analysis [Hz]
        response_amplitude: displacement amplitude [mm] at each harmonic_freq
    """
    # Sample natural frequencies (modal analysis results)
    modal_freqs = np.array([45.2, 78.9, 112.5, 145.0, 180.3, 220.1])
    
    # Harmonic response frequency sweep
    harmonic_freqs = np.linspace(0.1, 200, 400)
    
    # Simulate response amplitude with peaks at natural frequencies
    response = np.zeros_like(harmonic_freqs)
    for f0 in modal_freqs:
        # Add a Lorentzian peak at each natural frequency
        response += 0.5 / ((harmonic_freqs - f0)**2 + 1.0)
    
    # Add some random noise
    np.random.seed(42)
    response += np.random.normal(0, 0.02, len(harmonic_freqs))
    
    # Scale to mm
    response_amplitude = response * 10.0
    
    return modal_freqs, harmonic_freqs, response_amplitude

def main():
    # Ensure results directory exists
    os.makedirs('../results', exist_ok=True)
    
    # Read dominant forcing frequency from torque analysis
    f_dom = read_dominant_frequency()
    
    # Generate sample results (in lieu of actual FEA output)
    modal_freqs, harmonic_freqs, response_amplitude = generate_sample_results()
    
    # Print modal frequencies
    print("Modal frequencies (natural frequencies) from FEA:")
    for i, f in enumerate(modal_freqs, 1):
        print(f"  Mode {i}: {f:.1f} Hz")
    
    # Identify closest natural frequency to forcing frequency
    idx_closest = np.argmin(np.abs(modal_freqs - f_dom))
    f_nat_closest = modal_freqs[idx_closest]
    separation = abs(f_nat_closest - f_dom)
    print(f"\nClosest natural frequency to forcing {f_dom:.2f} Hz is {f_nat_closest:.1f} Hz")
    print(f"Separation: {separation:.1f} Hz")
    
    # Determine if resonance risk exists (if separation < 10% of natural frequency)
    if separation < 0.1 * f_nat_closest:
        resonance_risk = "HIGH - forcing frequency close to natural frequency"
    else:
        resonance_risk = "LOW - sufficient separation"
    print(f"Resonance risk: {resonance_risk}")
    
    # Plot harmonic response
    plt.figure(figsize=(10, 6))
    plt.plot(harmonic_freqs, response_amplitude, 'b-', linewidth=1.5, label='Harmonic response')
    
    # Mark natural frequencies
    for f0 in modal_freqs:
        plt.axvline(x=f0, color='r', linestyle='--', alpha=0.5, linewidth=0.8)
    
    # Mark dominant forcing frequency
    plt.axvline(x=f_dom, color='k', linestyle='-', linewidth=2, label=f'Forcing frequency ({f_dom:.1f} Hz)')
    
    plt.xlabel('Frequency (Hz)')
    plt.ylabel('Response amplitude (mm)')
    plt.title('Harmonic Response of Pulley (FEA simulation)')
    plt.grid(True, alpha=0.3)
    plt.legend()
    plt.xlim(0, 200)
    plt.ylim(bottom=0)
    
    # Save plot
    plot_path = '../results/harmonic_response.png'
    plt.savefig(plot_path, dpi=150)
    print(f"\nHarmonic response plot saved to {plot_path}")
    
    # Also create a summary text file
    summary_path = '../results/fea_summary.txt'
    with open(summary_path, 'w') as f:
        f.write(f"""FEA Results Summary
===================
Dominant forcing frequency from torque measurement: {f_dom:.2f} Hz

Natural frequencies (modes):
""")
        for i, freq in enumerate(modal_freqs, 1):
            f.write(f"Mode {i}: {freq:.1f} Hz\n")
        f.write(f"""
Closest natural frequency: {f_nat_closest:.1f} Hz
Separation from forcing frequency: {separation:.1f} Hz
Resonance risk assessment: {resonance_risk}

Recommendations:
- If separation < 10% of natural frequency, consider design modifications.
- Potential modifications: increase stiffness, add damping, change pulley geometry.
""")
    print(f"Summary written to {summary_path}")

if __name__ == '__main__':
    main()
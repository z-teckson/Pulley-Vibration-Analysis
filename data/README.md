# Torque Measurement Data

## Source
Measured on the larger pulley of a fodder crushing machine using a rotary torque sensor.

## File Format
- **File**: `pulley_torque_data.csv`
- **Columns**: 
  - `Time (s)`: time in seconds
  - `Torque (Nm)`: torque in Newton-meters
- **Sampling rate**: 1 kHz (Δt = 0.001 s)
- **Duration**: 1.0 s (1000 samples)

## Notes
The raw data contains periodic fluctuations due to the cyclic loading of the crushing process. The dominant forcing frequency is expected to be around 25 Hz (corresponding to the pulley rotational speed and blade engagement frequency).

## Generating Sample Data
If you wish to regenerate the sample data with the same statistical properties, run the script `scripts/generate_sample_data.py`. It requires `numpy` and `pandas`.

```bash
cd scripts
python generate_sample_data.py
```
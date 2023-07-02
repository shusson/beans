from datetime import timedelta
import pandas as pd
import matplotlib.pyplot as plt
import argparse
import numpy as np
from scipy import signal

parser = argparse.ArgumentParser(description="Process accelerometer data file")
parser.add_argument("file_path", type=str, help="Path to the data file")

args = parser.parse_args()

data = pd.read_csv(args.file_path)

data["General.Time"] = pd.to_datetime(data["General.Time"])

start_time = data["General.Time"].min() + timedelta(seconds=120)
end_time = data["General.Time"].max() - timedelta(seconds=120)
data = data[(data["General.Time"] >= start_time) & (data["General.Time"] <= end_time)]


pressure_column = "MicroPressure.Pressure (Pa)"

# Detrend the data
detrended_data = signal.detrend(data[pressure_column].values)

fft_vals = np.abs(np.fft.rfft(detrended_data))
fft_freq = np.fft.rfftfreq(
    len(detrended_data), 0.1
)  # Adjust the time step according to your sampling rate


# Plot time domain
plt.figure(figsize=(20, 10))
plt.subplot(2, 1, 1)
plt.plot(data["General.Time"], detrended_data, label=pressure_column)
plt.xlabel("Time")
plt.ylabel("Amplitude")
plt.title("Pressure Readings over Time")
plt.legend()

# Plot frequency domain
plt.subplot(2, 1, 2)
plt.plot(
    fft_freq, 20 * np.log10(fft_vals), label="FFT of " + pressure_column
)  # Plot in dB scale
plt.xlabel("Frequency (Hz)")
plt.ylabel("Magnitude (dB)")
plt.title("Frequency Analysis of Pressure Readings")
plt.legend()

plt.tight_layout()
plt.show()

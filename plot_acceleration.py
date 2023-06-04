import pandas as pd
import matplotlib.pyplot as plt
import argparse
from datetime import timedelta
import numpy as np

parser = argparse.ArgumentParser(description="Process accelerometer data file")
parser.add_argument("file_path", type=str, help="Path to the data file")
parser.add_argument(
    "--start_buffer", type=int, default=60, help="Start buffer in seconds"
)
parser.add_argument("--end_buffer", type=int, default=60, help="End buffer in seconds")
args = parser.parse_args()

data = pd.read_csv(args.file_path)

data["General.Time"] = pd.to_datetime(data["General.Time"])

# Apply buffers
start_time = data["General.Time"].min() + timedelta(seconds=args.start_buffer)
end_time = data["General.Time"].max() - timedelta(seconds=args.end_buffer)
data = data[(data["General.Time"] >= start_time) & (data["General.Time"] <= end_time)]

# plot ISM330.Accel X (milli-g)
plt.figure(figsize=(10, 5))

data["magnitude"] = np.sqrt(
    data["ISM330.Accel X (milli-g)"] ** 2
    + data["ISM330.Accel Y (milli-g)"] ** 2
    + data["ISM330.Accel Z (milli-g)"] ** 2
)

fft_vals = np.fft.rfft(data["magnitude"])
fft_freq = np.fft.rfftfreq(
    len(data["magnitude"]), 0.1
)  # 0.1 is the time step in seconds

# Remove the DC component (first element of fft_vals)
fft_vals = fft_vals[1:]
fft_freq = fft_freq[1:]

# Plot FFT
plt.figure(figsize=(10, 5))
plt.plot(fft_freq, np.abs(fft_vals))
plt.xlabel("Frequency (Hz)")
plt.ylabel("Amplitude")
plt.title("Frequency Spectrum of Acceleration Magnitude (DC component removed)")
plt.xlim([0, 1])  # Limit x-axis to display frequencies below 1 Hz
plt.show()

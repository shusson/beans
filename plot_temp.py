import pandas as pd
import matplotlib.pyplot as plt
import argparse


parser = argparse.ArgumentParser(description="Process accelerometer data file")
parser.add_argument("file_path", type=str, help="Path to the data file")

args = parser.parse_args()

data = pd.read_csv(args.file_path)

data["General.Time"] = pd.to_datetime(data["General.Time"])

plt.figure(figsize=(10, 5))

columns = [
    "ISM330.Temperature (C)",
    "MMC5983.Temperature (C)",
    "BME68x.TemperatureC",
]

for column in columns:
    plt.plot(data["General.Time"], data[column], label=column)

plt.xlabel("Time")
plt.ylabel("Temperature (C)")
plt.title("Temperature Readings over Time")
plt.legend()
plt.show()

import csv
from datetime import datetime

from matplotlib import pyplot as plt

# Get dates, high, and low temperatures from file.
filename = 'estadisticas_normales_9120.csv'
with open(filename) as f:
    reader = csv.reader(f)
    header_row = next(reader)

    dates, highs, lows = [], [], []
    for row in reader:
        try:
            current_date = row[0]
            high = float(row[2])
            low = float(row[3])
        except ValueError:
            print(current_date, 'missing data')
        else:
            dates.append(current_date)
            highs.append(high)
            lows.append(low)

print(highs)
print(lows)

# Plot data.
fig = plt.figure(dpi=128, figsize=(15, 10))
plt.plot(dates, highs, c='red', alpha=0.5)
plt.plot(dates, lows, c='blue', alpha=0.5)
plt.fill_between(dates, highs, lows, facecolor='blue', alpha=0.2)

# Format plot.
title = "Datos históricos - Temperatura 1991-2020\nCorrientes"
plt.title(title, fontsize=12)
plt.xlabel('', fontsize=10)
fig.autofmt_xdate()
plt.ylabel("Temperatur (°C)", fontsize=10)
plt.tick_params(axis='both', which='major', labelsize=12)

plt.show()

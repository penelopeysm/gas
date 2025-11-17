import matplotlib.pyplot as plt
import json
from datetime import datetime

try:
    with open("gas_readings.json") as f:
        readings = json.load(f)
except FileNotFoundError as e:
    print("Error: 'gas_readings.json' file not found. Run `a.py` to create it first.")
    exit(1)

timestamps = [datetime.fromisoformat(r["timestamp"]) for r in readings]
values = [r["reading"] for r in readings]

# Plot
fig, ax = plt.subplots(figsize=(10, 6))
ax.plot(timestamps, values, marker='o', linestyle='-')
ax.set(title="Penny's Gas Meter", xlabel="Date", ylabel="Gas reading (m³)")
ax.set_title("Penny's Gas Meter", fontsize=16)
ax.grid(True)
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig("gas_readings_plot.png", dpi=300)

import discord
import warnings
import os
import json
import numpy as np
from pathlib import Path
from datetime import datetime, timedelta, time
from dataclasses import dataclass

intents = discord.Intents.all()
client = discord.Client(intents=intents)
GAS_CHAN_ID = 1350936583557087262

WEB_DATA_DIR = Path(__file__).parent / "web" / "data"
CUMULATIVE_OUTPUT_FILE = WEB_DATA_DIR / "readings.json"
DAILY_USAGE_OUTPUT_FILE = WEB_DATA_DIR / "daily_usage.json"

@dataclass
class GasMeterReading:
    datetime: datetime
    reading: float

    def to_json_dict(self):
        return {
            "datetime": self.datetime.isoformat(),
            "reading": self.reading,
        }

    def __lt__(self, other):
        return self.datetime < other.datetime

    def to_unix_tuple(self):
        return (int(self.datetime.timestamp()), self.reading)

@dataclass
class DailyGasUsage:
    date: datetime
    usage: float

    def to_json_dict(self):
        return {
            "date": self.date.isoformat(),
            "usage": self.usage,
        }

@client.event
async def on_ready():
    print(f"Logged on as {client.user}")
    chan = client.get_channel(GAS_CHAN_ID)
    if chan is None:
        raise RuntimeError("gas meter channel not found")
    readings = []
    async for message in chan.history(limit=None):
        try:
            readings.append(
                GasMeterReading(
                    message.created_at,
                    float(message.content),
                )
            )
        except ValueError:
            warnings.warn(
                f"Could not parse gas meter reading from message: `{message.content}`"
            )
    readings.sort()
    print(f"Found {len(readings)} gas meter readings")

    # Cumulative readings
    readings_as_dict = [r.to_json_dict() for r in readings]
    with open(CUMULATIVE_OUTPUT_FILE, "w") as f:
        json.dump(readings_as_dict, f, indent=4)
    print(f"Wrote cumulative readings to {CUMULATIVE_OUTPUT_FILE}")

    # Interpolated daily usage
    # Determine min and max dates
    first_date = min(r.datetime.date() for r in readings)
    tz = readings[0].datetime.tzinfo
    last_date = datetime.now(tz=tz).date()
    # construct x and y arrays
    readings_x, readings_y = zip(*(r.to_unix_tuple() for r in readings))
    readings_x = np.array(readings_x)
    readings_y = np.array(readings_y)
    # construct the points to interpolate to (6 am every day)
    time_obj = time(6, 0, 0, tzinfo=tz)
    ndays = (last_date - first_date).days + 2
    interp_x = np.array(
        [
            int(datetime.combine(d, time_obj).timestamp())
            for d in (first_date + timedelta(days=n) for n in range(ndays))
        ]
    )
    daily_readings = np.interp(interp_x, readings_x, readings_y)
    # then we take the diff to get daily usage
    daily_usage = np.diff(daily_readings)
    daily_usage_output = [
        DailyGasUsage(date=first_date + timedelta(days=n), usage=usage)
        for n, usage in enumerate(daily_usage)
    ]
    daily_usage_as_dict = [du.to_json_dict() for du in daily_usage_output]
    with open(DAILY_USAGE_OUTPUT_FILE, "w") as f:
        json.dump(daily_usage_as_dict, f, indent=4)
    print(f"Wrote daily usage to {DAILY_USAGE_OUTPUT_FILE}")

    await client.close()


client.run(os.environ["DISCORD_TOKEN"])

import discord
import warnings
import os
import json
from pathlib import Path

intents = discord.Intents.all()
client = discord.Client(intents=intents)

GAS_CHAN_ID = 1350936583557087262

OUTPUT_FILE = Path(__file__).parent / "web" / "readings.json"

@client.event
async def on_ready():
    print(f'Logged on as {client.user}')
    chan = client.get_channel(GAS_CHAN_ID)
    if chan is None:
        raise RuntimeError("gas meter channel not found")
    readings = []
    async for message in chan.history(limit=None):
        try:
            readings.append({
                "reading": float(message.content),
                "timestamp": message.created_at.isoformat()
            })
        except ValueError:
            warnings.warn(f"Could not parse gas meter reading from message: `{message.content}`")
    with open(OUTPUT_FILE, "w") as f:
        json.dump(readings, f, indent=4)
    print(f"Saved {len(readings)} gas meter readings to {OUTPUT_FILE}")
    await client.close()

client.run(os.environ["DISCORD_TOKEN"])

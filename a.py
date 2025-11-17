import discord
import warnings
import os
import json

intents = discord.Intents.all()
client = discord.Client(intents=intents)

GAS_CHAN_ID = 1350936583557087262

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
    with open("gas_readings.json", "w") as f:
        json.dump(readings, f, indent=4)
    print(f"Saved {len(readings)} gas meter readings to gas_readings.json")
    await client.close()

client.run(os.environ["DISCORD_TOKEN"])

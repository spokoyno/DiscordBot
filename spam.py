import discord
from discord.ext import commands
import asyncio

intents = discord.Intents.all()
intents.members = True
client = commands.Bot(command_prefix="!", intents=intents)

@client.event
async def on_ready():
    print(f'Logged in as {client.user.name}')

@client.command()
async def dm_all(ctx, *, message):
    members = ctx.guild.members
    for member in members:
        if not any(role.name in ["Booster", "Operator"] for role in member.roles):
            try:
                await member.send(message)
                await asyncio.sleep(1)
            except:
                print(f"Failed to send message to {member.name}")
    print("Messages sent!")

client.run('MTA2MDczNTE1NjExNTIxODUyMw.G2EuhE.7uQvSaO5xwupb5ZDfGNU5zhW_GKa9wlKRFj7qI')
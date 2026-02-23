import os
import discord
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()

bot = commands.Bot(command_prefix="!", intents=discord.Intents.default())

@bot.event
async def on_ready():
    print("Clearing global commands...")
    bot.tree.clear_commands(guild=None)
    await bot.tree.sync()
    print("Done!")
    await bot.close()

bot.run(os.getenv("DISCORD_TOKEN"))
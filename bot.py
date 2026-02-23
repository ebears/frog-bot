import os
import asyncio
import discord
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

# Load the guild ID from .env and create a Discord object from it
# int() is necessary because os.getenv() always returns a string
TEST_GUILD = discord.Object(id=int(os.getenv("GUILD_ID")))

@bot.event
async def on_message(message):
    print(f"Message received: {message.content}")
    await bot.process_commands(message)  # Still process commands

@bot.command()
@commands.is_owner()
async def sync(ctx: commands.Context, scope: str = "guild"):
    if scope == "global":
        synced = await bot.tree.sync()
        await ctx.send(f"Synced {len(synced)} commands globally.")
    else:
        bot.tree.copy_global_to(guild=TEST_GUILD)
        synced = await bot.tree.sync(guild=TEST_GUILD)
        await ctx.send(f"Synced {len(synced)} commands to this guild.")

async def main():
    async with bot:
        await bot.load_extension("cogs.general")
        await bot.start(os.getenv("DISCORD_TOKEN"))

asyncio.run(main())
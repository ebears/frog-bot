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
ENVIRONMENT = os.getenv("ENVIRONMENT", "development")

async def setup_hook():
    # Load cogs
    await bot.load_extension("cogs.general")
    await bot.load_extension("cogs.moderation")

    # Sync commands once on startup
    print(f"Environment: {ENVIRONMENT}")
    if ENVIRONMENT == "production":
        synced = await bot.tree.sync()
        print(f"Synced {len(synced)} commands globally.")
    else:
        bot.tree.copy_global_to(guild=TEST_GUILD)
        synced = await bot.tree.sync(guild=TEST_GUILD)
        print(f"Synced {len(synced)} commands to guild.")

bot.setup_hook = setup_hook

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user} (ID: {bot.user.id})")

@bot.event
async def on_message(message):
    print(f"Message received: {message.content}")
    await bot.process_commands(message)


asyncio.run(bot.start(os.getenv("DISCORD_TOKEN")))
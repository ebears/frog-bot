import discord
from discord import app_commands
from discord.ext import commands


class General(commands.Cog):

    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(name="hello", description="Get a greeting from the bot")
    async def hello(self, interaction: discord.Interaction):
        await interaction.response.send_message(f"Hey {interaction.user.mention}! 👋")

    @app_commands.command(name="say", description="Make the bot repeat a message")
    async def say(self, interaction: discord.Interaction, message: str):
        await interaction.response.send_message(message)


async def setup(bot: commands.Bot):
    await bot.add_cog(General(bot))
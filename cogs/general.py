import discord
from discord import app_commands
from discord.ext import commands


class General(commands.Cog):

    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(name="ping", description="Check the bot's latency")
    async def ping(self, interaction: discord.Interaction):
        latency = round(self.bot.latency * 1000)
        await interaction.response.send_message(f"Pong! 🏓 `{latency}ms`")

    @app_commands.command(name="hello", description="Get a greeting from the bot")
    async def hello(self, interaction: discord.Interaction):
        await interaction.response.send_message(f"Hey {interaction.user.mention}! 👋")

    @app_commands.command(name="info", description="Display info about the server")
    async def info(self, interaction: discord.Interaction):
        await interaction.response.defer()
    
        guild = interaction.guild
    
        # Fetch the owner directly from the API instead of relying on cache
        owner = await guild.fetch_member(guild.owner_id)
    
        embed = discord.Embed(
            title=guild.name,
            description="Here's some info about this server.",
            color=discord.Color.blurple()
        )
        embed.add_field(name="Owner", value=owner.mention, inline=True)
        embed.add_field(name="Members", value=guild.member_count, inline=True)
        embed.add_field(name="Created", value=guild.created_at.strftime("%b %d, %Y"), inline=True)
    
        if guild.icon:
            embed.set_thumbnail(url=guild.icon.url)
    
        await interaction.followup.send(embed=embed)

    @app_commands.command(name="say", description="Make the bot repeat a message")
    async def say(self, interaction: discord.Interaction, message: str):
        await interaction.response.send_message(message)


async def setup(bot: commands.Bot):
    await bot.add_cog(General(bot))
import discord
from discord import app_commands
from discord.ext import commands
from datetime import datetime, timezone


def format_duration(seconds: int) -> str:
    """Convert a number of seconds into a human-readable duration string."""
    days, remainder = divmod(seconds, 86400)
    hours, remainder = divmod(remainder, 3600)
    minutes, seconds = divmod(remainder, 60)

    parts = []
    if days:
        parts.append(f"{days}d")
    if hours:
        parts.append(f"{hours}h")
    if minutes:
        parts.append(f"{minutes}m")
    if seconds or not parts:
        parts.append(f"{seconds}s")

    return " ".join(parts)


class Info(commands.Cog):
    """General-purpose utility commands."""

    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(name="ping", description="Check the bot's latency")
    async def ping(self, interaction: discord.Interaction):
        latency = round(self.bot.latency * 1000)
        await interaction.response.send_message(f"Pong! 🏓 `{latency}ms`")

    @app_commands.command(name="serverinfo", description="Display info about the server")
    async def serverinfo(self, interaction: discord.Interaction):
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

    @app_commands.command(name="memberinfo", description="Display detailed info about a user")
    @app_commands.describe(member="The member to look up (defaults to yourself)")
    async def memberinfo(self, interaction: discord.Interaction, member: discord.Member = None):
        await interaction.response.defer()

        # Default to the invoking user if no member is specified
        member = member or interaction.user

        now = datetime.now(timezone.utc)
        account_age = (now - member.created_at).days
        join_age = (now - member.joined_at).days

        # Sort roles by position (highest first), excluding @everyone
        roles = [r.mention for r in reversed(member.roles) if r.name != "@everyone"]
        roles_display = " ".join(roles) if roles else "None"

        embed = discord.Embed(
            title=str(member),
            color=member.color if member.color.value else discord.Color.blurple()
        )
        embed.set_thumbnail(url=member.display_avatar.url)

        embed.add_field(
            name="Account Created",
            value=f"{member.created_at.strftime('%b %d, %Y')}\n({account_age} days ago)",
            inline=True
        )
        embed.add_field(
            name="Joined Server",
            value=f"{member.joined_at.strftime('%b %d, %Y')}\n({join_age} days ago)",
            inline=True
        )
        embed.add_field(
            name=f"Roles ({len(roles)})",
            value=roles_display,
            inline=False
        )

        embed.set_footer(text=f"User ID: {member.id}")

        await interaction.followup.send(embed=embed)

    @app_commands.command(name="uptime", description="Show how long the bot has been running")
    async def uptime(self, interaction: discord.Interaction):
        start_time = getattr(self.bot, "start_time", None)
        if start_time is None:
            await interaction.response.send_message("Uptime is not available yet.", ephemeral=True)
            return

        elapsed = int((datetime.now(timezone.utc) - start_time).total_seconds())
        await interaction.response.send_message(f"⏱️ Uptime: `{format_duration(elapsed)}`")


async def setup(bot: commands.Bot):
    await bot.add_cog(Info(bot))
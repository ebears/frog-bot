# cogs/moderation.py

import discord
from discord import app_commands
from discord.ext import commands


class Moderation(commands.Cog):
    """
    A cog for moderation commands.
    These commands are restricted to users with the Manage Messages permission.
    """

    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(name="nuke", description="Delete messages in this channel, optionally filtered by a phrase")
    @app_commands.describe(
        phrase="Only delete messages containing this phrase. If omitted, deletes all messages.",
        limit="How many messages to search through (default: 100, max: 500)"
    )
    @app_commands.checks.has_permissions(manage_messages=True)
    async def nuke(self, interaction: discord.Interaction, phrase: str = None, limit: int = 100):
        # Clamp limit to a sensible maximum to avoid hitting API rate limits
        limit = min(limit, 500)

        # Defer early since this may take a while
        await interaction.response.defer(ephemeral=True)

        if phrase:
            # Fetch messages and filter to only those containing the phrase
            # check() is passed to purge() to filter messages on the fly
            def check(message: discord.Message) -> bool:
                return phrase.lower() in message.content.lower()

            deleted = await interaction.channel.purge(limit=limit, check=check)
            summary = f"Deleted {len(deleted)} message(s) containing `{phrase}`."
        else:
            # No phrase provided — delete everything in range
            deleted = await interaction.channel.purge(limit=limit)
            summary = f"Deleted {len(deleted)} message(s)."

        # ephemeral=True means only the moderator who ran the command can see this
        await interaction.followup.send(summary, ephemeral=True)

    @nuke.error
    async def nuke_error(self, interaction: discord.Interaction, error: app_commands.AppCommandError):
        # Use followup if we already deferred, otherwise use response
        send = interaction.followup.send if interaction.response.is_done() else interaction.response.send_message
    
        if isinstance(error, app_commands.MissingPermissions):
            await send("You need the **Manage Messages** permission to use this command.", ephemeral=True)
        else:
            await send(f"An error occurred: {error}", ephemeral=True)


async def setup(bot: commands.Bot):
    await bot.add_cog(Moderation(bot))
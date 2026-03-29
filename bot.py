import os
import discord
from discord.ext import commands
from discord import app_commands
from config import TOKEN

class BoboBot(commands.Bot):
    def __init__(self):
        intents = discord.Intents.default()
        intents.message_content = True
        intents.voice_states = True
        
        super().__init__(
            command_prefix="!", # Slash commands primarily, but prefix is required
            intents=intents,
            help_command=None
        )

    async def setup_hook(self):
        """Standard setup hook to load cogs."""
        # Load our music cog
        await self.load_extension('cogs.music')
        
        # Sync slash commands with Discord
        # Note: In production, global sync can take up to an hour. 
        # For testing, you can sync to a specific guild.
        print(f"Syncing slash commands...")
        await self.tree.sync()
        print(f"Slash commands synced.")

    async def on_ready(self):
        print(f'Logged in as {self.user} (ID: {self.user.id})')
        print('------')

if __name__ == "__main__":
    bot = BoboBot()
    bot.run(TOKEN)

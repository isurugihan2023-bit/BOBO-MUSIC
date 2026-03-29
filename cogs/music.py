import discord
from discord import app_commands
from discord.ext import commands
from utils.yt import YTSession
from utils.queue import MusicQueue
from config import EMBED_COLOR, FOOTER_TEXT

class MusicCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.queues = {} # State store per guild
        self.yt = YTSession()

    def get_queue(self, guild_id):
        if guild_id not in self.queues:
            self.queues[guild_id] = MusicQueue(self.bot, guild_id)
        return self.queues[guild_id]

    @app_commands.command(name="play", description="Play a song from YouTube or search for one.")
    @app_commands.describe(query="The YouTube URL or search query for the song.")
    async def play(self, interaction: discord.Interaction, query: str):
        # Initial response to avoid timeout
        await interaction.response.defer()
        
        # Check if user is in a voice channel
        if not interaction.user.voice:
            embed = discord.Embed(title="❌ Error", description="You must be in a voice channel to use this command.", color=EMBED_COLOR)
            return await interaction.followup.send(embed=embed)

        queue = self.get_queue(interaction.guild_id)
        
        # Connect to voice if not already connected
        if not interaction.guild.voice_client:
            queue.voice_client = await interaction.user.voice.channel.connect()
            # Start the background play loop
            self.bot.loop.create_task(queue.play_next(interaction.channel))
        else:
            queue.voice_client = interaction.guild.voice_client

        # Extract info (search or via URL)
        try:
            song_info = await self.yt.get_info(query)
            song_info['requester'] = interaction.user.mention
            song_info['duration'] = self.yt.format_duration(song_info['duration'])
            
            # Add to queue
            await queue.songs.put(song_info)
            
            # Send Queued Embed
            embed = discord.Embed(
                title="✅ Song Queued",
                description=f"[{song_info['title']}]({song_info['url']})",
                color=EMBED_COLOR
            )
            embed.set_thumbnail(url=song_info['thumbnail'])
            embed.add_field(name="Position", value=f"{queue.songs.qsize()}", inline=True)
            embed.set_footer(text=FOOTER_TEXT)
            
            await interaction.followup.send(embed=embed)
            
        except Exception as e:
            embed = discord.Embed(title="❌ Extraction Error", description=f"An error occurred while fetching information: {str(e)}", color=0xFF0000)
            await interaction.followup.send(embed=embed)

    @app_commands.command(name="skip", description="Skip the current song.")
    async def skip(self, interaction: discord.Interaction):
        queue = self.get_queue(interaction.guild_id)
        if not queue.voice_client or not queue.voice_client.is_playing():
             embed = discord.Embed(title="❌ Error", description="Nothing is currently playing.", color=EMBED_COLOR)
             return await interaction.response.send_message(embed=embed)
        
        queue.skip()
        embed = discord.Embed(title="⏭️ Skipped", description="Skipping to the next song...", color=EMBED_COLOR)
        await interaction.response.send_message(embed=embed)

    @app_commands.command(name="pause", description="Pause the music.")
    async def pause(self, interaction: discord.Interaction):
        if interaction.guild.voice_client and interaction.guild.voice_client.is_playing():
            interaction.guild.voice_client.pause()
            embed = discord.Embed(title="⏸️ Paused", description="Playback has been paused.", color=EMBED_COLOR)
            await interaction.response.send_message(embed=embed)
        else:
            embed = discord.Embed(title="❌ Error", description="Nothing is playing or already paused.", color=EMBED_COLOR)
            await interaction.response.send_message(embed=embed)

    @app_commands.command(name="resume", description="Resume the music.")
    async def resume(self, interaction: discord.Interaction):
        if interaction.guild.voice_client and interaction.guild.voice_client.is_paused():
            interaction.guild.voice_client.resume()
            embed = discord.Embed(title="▶️ Resumed", description="Playback has been resumed.", color=EMBED_COLOR)
            await interaction.response.send_message(embed=embed)
        else:
            embed = discord.Embed(title="❌ Error", description="Nothing is paused.", color=EMBED_COLOR)
            await interaction.response.send_message(embed=embed)

    @app_commands.command(name="stop", description="Stop music and clear the queue.")
    async def stop(self, interaction: discord.Interaction):
        queue = self.get_queue(interaction.guild_id)
        queue.stop()
        if interaction.guild.voice_client:
            await interaction.guild.voice_client.disconnect()
        
        embed = discord.Embed(title="⏹️ Stopped", description="Music stopped and queue cleared.", color=EMBED_COLOR)
        await interaction.response.send_message(embed=embed)

    @app_commands.command(name="nowplaying", description="Show the current playing song.")
    async def nowplaying(self, interaction: discord.Interaction):
        queue = self.get_queue(interaction.guild_id)
        if not queue.current_song:
            embed = discord.Embed(title="❌ Error", description="Nothing is playing.", color=EMBED_COLOR)
            return await interaction.response.send_message(embed=embed)
            
        embed = discord.Embed(
            title="🎶 Now Playing",
            description=f"[{queue.current_song['title']}]({queue.current_song['url']})",
            color=EMBED_COLOR
        )
        embed.set_thumbnail(url=queue.current_song['thumbnail'])
        embed.add_field(name="Duration", value=queue.current_song['duration'], inline=True)
        embed.add_field(name="Requested By", value=queue.current_song['requester'], inline=True)
        embed.set_footer(text=FOOTER_TEXT)
        await interaction.response.send_message(embed=embed)

    @app_commands.command(name="queue", description="Show the current server queue.")
    async def queue(self, interaction: discord.Interaction):
        queue = self.get_queue(interaction.guild_id)
        if queue.songs.empty() and not queue.current_song:
            embed = discord.Embed(title="📭 Queue Empty", description="There are no songs in the queue.", color=EMBED_COLOR)
            return await interaction.response.send_message(embed=embed)
            
        description = ""
        if queue.current_song:
            description += f"**Now Playing:** [{queue.current_song['title']}]({queue.current_song['url']})\n\n"
        
        # We can't actually peek as easily into queue.Queue
        # So we'll show up to the next 5 items
        queue_list = list(queue.songs._queue)
        if queue_list:
            description += "**Upcoming:**\n"
            for i, song in enumerate(queue_list[:10], 1):
                description += f"{i}. [{song['title']}]({song['url']})\n"
        
        embed = discord.Embed(title=f"📜 Queue for {interaction.guild.name}", description=description, color=EMBED_COLOR)
        embed.set_footer(text=f"Total: {len(queue_list)} songs")
        await interaction.response.send_message(embed=embed)

    @app_commands.command(name="volume", description="Set the bot's volume.")
    @app_commands.describe(level="Volume level from 0 to 100.")
    async def volume(self, interaction: discord.Interaction, level: int):
        if not 0 <= level <= 100:
            return await interaction.response.send_message("Volume must be between 0 and 100.")
            
        queue = self.get_queue(interaction.guild_id)
        queue.volume = level / 100
        
        if interaction.guild.voice_client and interaction.guild.voice_client.source:
            interaction.guild.voice_client.source.volume = queue.volume
            
        embed = discord.Embed(title="🔊 Volume Changed", description=f"Volume set to **{level}%**.", color=EMBED_COLOR)
        await interaction.response.send_message(embed=embed)

async def setup(bot):
    await bot.add_cog(MusicCog(bot))

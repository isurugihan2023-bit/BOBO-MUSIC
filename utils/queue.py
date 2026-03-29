import asyncio
import discord
from config import FFMPEG_OPTIONS, EMBED_COLOR, FOOTER_TEXT

class MusicQueue:
    def __init__(self, bot, guild_id):
        self.bot = bot
        self.guild_id = guild_id
        self.songs = asyncio.Queue()
        self.current_song = None
        self.voice_client = None
        self.volume = 0.5 # Default 50%
        self.skip_event = asyncio.Event()

    async def play_next(self, ctx):
        """Infinite loop to process the queue."""
        while True:
            self.skip_event.clear()
            
            try:
                # Wait for next song
                self.current_song = await asyncio.wait_for(self.songs.get(), timeout=300) # 5 min timeout
            except asyncio.TimeoutError:
                # Disconnect if empty for 5 minutes
                if self.voice_client:
                    await self.voice_client.disconnect()
                return

            # Prepare audio source
            source = discord.FFmpegPCMAudio(self.current_song['source'], **FFMPEG_OPTIONS)
            # Use volume transformer
            source = discord.PCMVolumeTransformer(source, volume=self.volume)
            
            self.voice_client.play(source, after=lambda e: self.bot.loop.call_soon_threadsafe(self.skip_event.set))
            
            # Send Now Playing Embed
            embed = discord.Embed(
                title="🎵 Now Playing",
                description=f"[{self.current_song['title']}]({self.current_song['url']})",
                color=EMBED_COLOR
            )
            embed.set_thumbnail(url=self.current_song['thumbnail'])
            embed.add_field(name="Duration", value=self.current_song['duration'], inline=True)
            embed.add_field(name="Requested By", value=self.current_song['requester'], inline=True)
            embed.set_footer(text=FOOTER_TEXT)
            
            await ctx.send(embed=embed)

            # Wait for song to finish or skip
            await self.skip_event.wait()
            self.current_song = None

    def skip(self):
        if self.voice_client and self.voice_client.is_playing():
            self.voice_client.stop()

    def stop(self):
        self.songs = asyncio.Queue() # Clear queue
        if self.voice_client and self.voice_client.is_playing():
            self.voice_client.stop()

import asyncio
import yt_dlp
import discord
from config import YDL_OPTIONS

class YTSession:
    def __init__(self):
        self.ydl = yt_dlp.YoutubeDL(YDL_OPTIONS)

    async def get_info(self, query):
        """Extracts info for a song/URL using yt-dlp."""
        loop = asyncio.get_event_loop()
        
        # Determine if it's a URL or search query
        # If not a URL, yt-dlp will treat it as a search query due to 'ytsearch:' prefix or default search option
        info = await loop.run_in_executor(None, lambda: self.ydl.extract_info(query, download=False))
        
        if 'entries' in info:
            # We take the first result from the search query
            info = info['entries'][0]
            
        return {
            'source': info['url'],
            'title': info.get('title', 'Unknown Title'),
            'thumbnail': info.get('thumbnail', None),
            'duration': info.get('duration', 0),
            'url': info.get('webpage_url', info.get('url')),
            'id': info.get('id')
        }

    @staticmethod
    def format_duration(seconds):
        """Converts seconds to HH:MM:SS format."""
        if not seconds:
            return "Unknown"
        minutes, seconds = divmod(seconds, 60)
        hours, minutes = divmod(minutes, 60)
        if hours > 0:
            return f"{hours:d}:{minutes:02d}:{seconds:02d}"
        return f"{minutes:02d}:{seconds:02d}"

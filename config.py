import os
from dotenv import load_dotenv

load_dotenv()

# Bot Configuration
TOKEN = os.getenv("DISCORD_TOKEN")
CLIENT_ID = os.getenv("CLIENT_ID")

if not TOKEN or TOKEN == "your_token_here":
    print("❌ ERROR: DISCORD_TOKEN is missing or is set to 'your_token_here' in the .env file.")
    exit(1)

if not CLIENT_ID or CLIENT_ID == "your_client_id":
    print("⚠️ WARNING: CLIENT_ID is missing.")

# Styling
EMBED_COLOR = 0xFF0000  # Red
FOOTER_TEXT = "BOBO MUSIC | Premium Gaming Sound"
THUMBNAIL_URL = "https://i.imgur.com/8Qq8Qq8.png"

# FFmpeg Options
FFMPEG_OPTIONS = {
    'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5',
    'options': '-vn',
}

# yt-dlp Options
YDL_OPTIONS = {
    'format': 'm4a/bestaudio/best',
    'cookiefile': 'cookies.txt',
    'extractor_args': {'youtube': ['player_client=android,web,ios']},
    'user_agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36',
    'extractaudio': True,
    'audioformat': 'mp3',
    'outtmpl': '%(extractor)s-%(id)s-%(title)s.%(ext)s',
    'restrictfilenames': True,
    'noplaylist': True,
    'nocheckcertificate': True,
    'ignoreerrors': False,
    'logtostderr': False,
    'quiet': True,
    'no_warnings': True,
    'default_search': 'ytsearch',
    'source_address': '0.0.0.0',
}

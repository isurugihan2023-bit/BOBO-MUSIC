import os
from dotenv import load_dotenv

load_dotenv()

# Bot Configuration
TOKEN = os.getenv("DISCORD_TOKEN")
CLIENT_ID = os.getenv("CLIENT_ID")

if not TOKEN or TOKEN == "your_token_here":
    print("❌ ERROR: DISCORD_TOKEN is missing or is set to 'your_token_here' in the .env file.")
    print("Please go to https://discord.com/developers/applications, create a bot, and paste your token in .env")
    exit(1)

if not CLIENT_ID or CLIENT_ID == "your_client_id":
    print("⚠️ WARNING: CLIENT_ID is missing or is set to 'your_client_id' in the .env file.")
    print("Slash commands might not sync correctly without a valid Client ID.")

# Styling
EMBED_COLOR = 0xFF0000  # Red
FOOTER_TEXT = "BOBO MUSIC | Premium Gaming Sound"
THUMBNAIL_URL = "https://i.imgur.com/8Qq8Qq8.png" # Placeholder icon

# FFmpeg Options
FFMPEG_OPTIONS = {
    'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5',
    'options': '-vn',
}

# yt-dlp Options
YDL_OPTIONS = {
    'format': 'ba/best',
    'cookiefile': 'cookies.txt',
    'extractor_args': {'youtube': ['player_client=ios']},
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
    'default_search': 'auto',
    'source_address': '0.0.0.0',
}

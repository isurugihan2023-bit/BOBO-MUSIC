# 🎵 BOBO MUSIC - Discord Music Bot 🎵

A production-ready Discord Music Bot powered by **Python 3.10+**, **discord.py**, **yt-dlp**, and **FFmpeg**.

## 🚀 Features

- **YouTube Search & URL Support**: Just type the song name or paste a link.
- **Slash Commands Only**: Modern, clean, and intuitive.
- **Per-Server Queue**: Each server has its own playback state and queue.
- **High Fidelity**: Optimized FFmpeg streaming for high-quality audio.
- **Gaming Aesthetic**: Red and Black themed embeds for a premium look.

## ⚙️ Requirements

1. **Python 3.10+** (Required)
2. **FFmpeg** (Must be installed and in your system's PATH)
3. **PyNaCl** (For voice support)
4. **Discord Bot Token** (Get it from the [Discord Developer Portal](https://discord.com/developers/applications))

## 🛠️ Installation

1. **Clone or Download** this directory.
2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```
3. **Configure your environment**:
   - Open `.env` and replace `your_token_here` with your Discord Bot Token.
   - Replace `your_client_id` with your Bot's Client ID.
4. **Run the bot**:
   ```bash
   python bot.py
   ```

## 📜 Commands

| Command | Description |
| :--- | :--- |
| `/play <query>` | Play a song from a YouTube URL or search query. |
| `/pause` | Pause the current song. |
| `/resume` | Resume playback. |
| `/skip` | Skip to the next song in the queue. |
| `/stop` | Stop music and clear the server's queue. |
| `/queue` | View the current server's queue. |
| `/nowplaying` | Show details about the current song. |
| `/volume <0-100>` | Adjust the bot's volume level. |

## ⚠️ Common Errors & Fixes

### FFmpeg not found
- **Error**: `discord.ext.commands.errors.CommandInvokeError: Command raised an exception: ClientException: ffmpeg was not found.`
- **Fix**: Download FFmpeg from [ffmpeg.org](https://ffmpeg.org/download.html) and add the `bin` folder to your system environment variables.

### Voice not working (PyNaCl)
- **Error**: `RuntimeError: PyNaCl is not installed.`
- **Fix**: Run `pip install pynacl` and ensure you have C++ Build Tools installed on Windows if it fails to compile.

### Slash Commands Not Showing
- **Note**: It can take up to 1 hour for slash commands to register globally.
- **Tip**: For testing, you can modify `bot.tree.sync(guild=discord.Object(id=YOUR_GUILD_ID))` in `bot.py` to sync instantly to one server.

---

Built with ❤️ by **BOBO MUSIC**

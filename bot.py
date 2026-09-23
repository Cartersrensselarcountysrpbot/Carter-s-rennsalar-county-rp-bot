import os
import threading
from flask import Flask
import discord
from discord.ext import commands

# 1. Initialize Flask Web Server for Render
app = Flask(__name__)

@app.route('/')
def home():
    return "Bot is alive!"

def run_flask():
    # Force port 10000 for Render health checks
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)

# 2. Start Flask on a background thread so it opens immediately
flask_thread = threading.Thread(target=run_flask)
flask_thread.daemon = True
flask_thread.start()

# 3. Initialize Discord Bot
bot = commands.Bot(command_prefix="!", intents=discord.Intents.default())

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user.name}")

# 4. Run Bot
token = os.environ.get("DISCORD_TOKEN")
if token:
    print(f"Token found! Length: {len(token)}, Starting bot...")
    bot.run(token)
else:
    print("ERROR: DISCORD_TOKEN is missing!")

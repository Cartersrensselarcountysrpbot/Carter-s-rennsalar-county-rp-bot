import os
import discord
from discord.ext import commands

# Enable privileged intents (Required for member joins and message content)
intents = discord.Intents.default()
intents.members = True
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

# Configuration: Update these with your server's details
WELCOME_CHANNEL_ID = 1552134040285610079  # Replace with your actual Welcome Channel ID
ALLOWED_ROLE_NAME = "Staff"             # Replace with the exact name of your moderator role

@bot.event
async def on_ready():
    print(f"Bot logged in as {bot.user}")

# ----------------------------
# 1. AUTO-WELCOME NEW MEMBERS
# ----------------------------
@bot.event
async def on_member_join(member):
    channel = bot.get_channel(WELCOME_CHANNEL_ID)
    if channel:
        embed = discord.Embed(
            title=f"Welcome to the server, {member.name}! 🎉",
            description=f"Hey {member.mention}, welcome to Rensselaer County Roleplay! Make sure to read the rules.",
            color=discord.Color.blue()
        )
        embed.set_thumbnail(url=member.display_avatar.url)
        await channel.send(embed=embed)

# ----------------------------
# 2. CLEAR CHAT COMMAND (!clear <amount>)
# ----------------------------
@bot.command()
@commands.has_role(ALLOWED_ROLE_NAME)
async def clear(ctx, amount: int):
    """Deletes a specified number of messages."""
    if amount <= 0:
        await ctx.send("Please specify a number greater than 0.", delete_after=5)
        return
    
    # +1 to delete the command message itself
    deleted = await ctx.channel.purge(limit=amount + 1)
    await ctx.send(f"🧹 Cleared {len(deleted) - 1} messages.", delete_after=5)

# Error handling if user lacks the required role
@clear.error
async def clear_error(ctx, error):
    if isinstance(error, commands.MissingRole):
        await ctx.send("❌ You do not have permission to use this command.", delete_after=5)

# ----------------------------
# 3. DELETE SPECIFIC MESSAGE (!delete <message_id>)
# ----------------------------
@bot.command()
@commands.has_role(ALLOWED_ROLE_NAME)
async def delete(ctx, message_id: int):
    """Deletes a specific message by its ID."""
    try:
        msg = await ctx.channel.fetch_message(message_id)
        await msg.delete()
        await ctx.message.delete()  # Deletes the command trigger message
        await ctx.send(f"✅ Deleted message `{message_id}`.", delete_after=5)
    except discord.NotFound:
        await ctx.send("❌ Message not found in this channel.", delete_after=5)
    except discord.Forbidden:
        await ctx.send("❌ I don't have permission to delete that message.", delete_after=5)

@delete.error
async def delete_error(ctx, error):
    if isinstance(error, commands.MissingRole):
        await ctx.send("❌ You do not have permission to use this command.", delete_after=5)

# Paste your bot token from the Discord Developer Portal below
import os
bot.run("MTU1MjE1MjM0OTU5Njk3NTE2NA.GPuHgh.8wOfbw-GS0Wyy6gMXtW2QvNathdbAetV0V3B6U")

import discord
import re
import os
from discord.ext import commands

# --- CONFIGURATION ---
BOT_TOKEN = os.environ.get('TOKEN')
BOT_NAME = 'Mini Blanket'
SERVER_IP = 'play.astralclub.xyz'

# --- SETUP (Bot + Intents) ---
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='!', intents=intents)


# --- on_ready() ---
@bot.event
async def on_ready():
    print(f'Bot: {BOT_NAME} is online and connected.')
    await bot.change_presence(activity=discord.Game(name=f"on {SERVER_IP}"))


# --- EMBED GENERATOR ---
def create_ip_embed():
    embed = discord.Embed(
        title="🌟 Welcome to Astral Club! 🌟",
        description="Click the server address below to copy it easily!",
        color=discord.Color.teal()
    )

    embed.add_field(
        name="🚀 Server Address (Java/Bedrock)",
        value=f"```fix\n{SERVER_IP}\n```",
        inline=False
    )

    embed.add_field(
        name="🔗 Bedrock Port (Default)",
        value="`19132`",
        inline=True
    )

    embed.set_footer(text=f"Enjoy your stay! | Responded by {BOT_NAME}")
    return embed


# --- COMMAND: !ip ---
@bot.command()
async def ip(ctx):
    await ctx.send(f"**Attention {ctx.author.mention}!!**", embed=create_ip_embed())


# --- SMART LISTENER (Regex IP trigger) ---
@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    # Prevent double-trigger if user types !ip
    if message.content.lower().startswith("!ip"):
        await bot.process_commands(message)
        return

    # Regex detect "ip" as a separate word
    match_found = re.search(r"\bip\b", message.content, re.IGNORECASE)

    if match_found:
        await message.channel.send(
            f"**<a:ping:801234567890123456> Hey {message.author.mention}!!! <a:ping:801234567890123456>**",
            embed=create_ip_embed()
        )

    await bot.process_commands(message)


# --- RUN BOT ---
try:
    if BOT_TOKEN:
        bot.run(BOT_TOKEN)
    else:
        print("ERROR: TOKEN environment variable not set.")
except Exception as e:
    print(f"ERROR during bot run: {e}")

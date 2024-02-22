import discord
from discord.ext import commands
import aiohttp
import io
import json
import requests
import random

poses = ["default", "marching", "walking", "crouching", "crossed", "criss_cross", "cheering", "relaxing", "trudging", "cowering", "pointing", "lunging", "dungeons", "facepalm", "sleeping", "archer", "kicking"]

# Initialize the bot
intents = discord.Intents.default()
bot = commands.Bot(command_prefix="/", intents=intents)

# Register the /skin command
@bot.slash_command(name='skin', description='Get a Minecraft users skin')
async def skinget(ctx, username: str):
    
    render_url = f"https://starlightskins.lunareclipse.studio/skin-render/{random.choice(poses)}/{username}/full"
    download_url = f"https://minotar.net/download/{username}.png"

    async with aiohttp.ClientSession() as session:
        async with session.get(download_url) as resp:
            if resp.status == 200:
                data = io.BytesIO(await resp.read())
                file = discord.File(data, filename=f"{username}_skin.png")
                embed = discord.Embed(title=f"Skin for {username}", description=f"[Download]({download_url})", color=discord.Color.dark_red())
                embed.set_image(url=render_url)
                await ctx.respond(embed=embed)
            else:
                await ctx.respond("Sorry, I couldn't find that skin.")

@bot.slash_command(name='ping', description="Sends the bot's latency.")
async def ping(ctx):
    await ctx.respond(f"Pong! Latency is {bot.latency}")

# Run the bot
with open("token.txt") as tokenfile:
    bot.run(tokenfile.read())
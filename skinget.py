import discord
from discord.ext import commands
import aiohttp
import io
import json
import requests

# Initialize the bot
intents = discord.Intents.default()
bot = commands.Bot(command_prefix="/", intents=intents)

# Register the /skin command
@bot.slash_command(name='skin', description='Get a Minecraft users skin')
async def skinget(ctx, username: str):
    try:
        uuidrequest = requests.get(f"https://api.mojang.com/users/profiles/minecraft/{username}")
        uuid = json.loads(uuidrequest.content)["id"]
    except KeyError:
        await ctx.respond("Sorry, I couldn't find that skin.")
    render_url = f"https://api.mineatar.io/body/full/{uuid}"
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
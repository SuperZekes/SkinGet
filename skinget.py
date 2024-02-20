import discord
from discord.ext import commands
import aiohttp
import io

# Initialize the bot
intents = discord.Intents.default()
bot = commands.Bot(command_prefix="/", intents=intents)

# Register the /skinget command
@bot.slash_command(name='skin', description='Get a Minecraft users skin')
async def skinget(ctx, username: str):
    skin_url = f"https://minotar.net/skin/{username}.png"

    async with aiohttp.ClientSession() as session:
        async with session.get(skin_url) as resp:
            if resp.status == 200:
                data = io.BytesIO(await resp.read())
                file = discord.File(data, filename=f"{username}_skin.png")
                await ctx.respond(f"Here is the skin for {username}:", file=file)
            else:
                await ctx.respond("Sorry, I couldn't find that skin.")

# Run the bot
bot.run('TOKEN')

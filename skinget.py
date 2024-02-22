import discord
from discord.ext import commands
import aiohttp
import io
import requests
import random

poses = ["default"]
# Initialize the bot
intents = discord.Intents.default()
bot = commands.Bot(command_prefix="/", intents=intents)


# Register the /skin command
@bot.slash_command(name="skin", description="Get a Minecraft users skin")
async def skinget(ctx, username: str):
    render_url = f"https://starlightskins.lunareclipse.studio/skin-render/{random.choice(poses)}/{username}/full"
    download_url = f"https://minotar.net/download/{username}.png"

    async with aiohttp.ClientSession() as session:
        async with session.get(download_url) as resp:
            if resp.status == 200:
                data = io.BytesIO(await resp.read())
                file = discord.File(data, filename=f"{username}_skin.png")
                embed = discord.Embed(
                    title=f"Skin for {username}",
                    description=f"[Download]({download_url})",
                    color=discord.Color.dark_red(),
                )
                embed.set_image(url=render_url)
                await ctx.respond(embed=embed)
            else:
                await ctx.respond("Sorry, I couldn't find that skin.")

# Register the /ping command
@bot.slash_command(name='ping', description="Sends the bot's latency.")
async def ping(ctx):
    await ctx.respond(f"Pong! Latency is {bot.latency}")


@bot.slash_command(name="create", description="Design a skin")
async def create(
    ctx,
    skin_type: discord.Option(str, choices=skin_creator_options["skin_type"].keys()),  # type: ignore
    base: discord.Option(str, choices=skin_creator_options["base_textures"].keys()),  # type: ignore
    base_color: discord.Option(str, choices=base_colors),  # type: ignore
    eyes: discord.Option(str, choices=skin_creator_options["eyes_textures"].keys()),  # type: ignore
    eye_color: discord.Option(str, choices=colors),  # type: ignore
    hair: discord.Option(str, choices=list(islice(skin_creator_options["hair_textures"].keys(), 25))),  # type: ignore
    hair_color: discord.Option(str, choices=colors),  # type: ignore
    top: discord.Option(str, choices=skin_creator_options["top_textures"].keys()),  # type: ignore
    bottom: discord.Option(str, choices=skin_creator_options["bottom_textures"].keys()),  # type: ignore
    shoes: discord.Option(str, choices=skin_creator_options["footwear_textures"].keys()),  # type: ignore
):
    skin_url = f"https://starlightskins.lunareclipse.studio/create-skin/{base}/{base_color}/{skin_type}/?eyes_texture={eyes}&eyes_color={eye_color}&hair_texture={hair}&hair_color={hair_color}&top_texture={top}&bottom_texture={bottom}&footwear_texture={shoes}"
    render_url = f'https://starlightskins.lunareclipse.studio/skin-render/default/MHF_Steve/full?skinUrl={urllib.parse.quote(skin_url, safe="")}'
    embed = discord.Embed(title=f"Skin Generated for {ctx.author.display_name}", description=f"[Get Skin]({skin_url})", color=discord.Color.blue())
    embed.set_image(url=render_url)
    await ctx.send(embed=embed)


# Run the bot
with open("token.txt") as tokenfile:
    bot.run(tokenfile.read())

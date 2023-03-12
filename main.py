import discord
import os
from discord.ext import commands
import aiohttp

intents = discord.Intents.default()
intents.members = True
intents.message_content = True

bot = commands.Bot(command_prefix='s&', intents=intents)

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user} (ID: {bot.user.id})')
    activity = discord.Activity(type=discord.ActivityType.listening, name="s&cat")
    await bot.change_presence(activity=activity)
    print('------')

@bot.command()
async def cat(ctx):
    """Displays a random cat picture."""
    async with aiohttp.ClientSession() as session:
        max_retries = 5
        retry_count = 0
        while retry_count < max_retries:
            retry_count += 1
            response = await session.get('https://display-a.sand.cat/cat.php')
            if response.status != 200:
                continue
            content_type = response.headers.get('Content-Type')
            if content_type == 'image/jpeg' or content_type == 'image/png':
                embed = discord.Embed(colour=discord.Colour.green())
                embed.set_image(url=response.url)
                embed.set_footer(text=f'Requested by: {ctx.author.name}', icon_url=ctx.author.avatar.url)
                await ctx.send(embed=embed)
                return
            elif content_type == 'video/mp4':
                continue
            else:
                return await ctx.send(f'Error requesting cat image: Invalid Content-Type: {content_type}')
        return await ctx.send(f'Error requesting cat image: Maximum retries ({max_retries}) reached')

bot.run(os.getenv('TOKEN'))

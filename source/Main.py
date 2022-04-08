import os
import discord
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

client = discord.Client()

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith("!?mundo"):
        await message.channel.send("https://media.discordapp.net/attachments/768840996347052042/831901847190372362/real.png")


client.run(TOKEN)
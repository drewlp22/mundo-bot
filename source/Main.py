import os
import discord
import time
import plankton
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

    if message.content.startswith("!?date"):
        plankton.create_image()
        time.sleep(1)
        date_image = open('buffer/image_date.png')
        await message.channel.send(file=date_image)

    if message.content == "!?pronouns":
        await message.channel.send("My preferred pronouns are he/they/bot/it")


client.run(TOKEN)
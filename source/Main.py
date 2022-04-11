import os
import discord
import time
import plankton
import mungoid
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
        date_image = discord.File(fp='buffer/image_date.png')
        await message.channel.send(file=date_image)

    if message.content == "!?pronouns":
        await message.channel.send("My preferred pronouns are he/they/bot/it")

    if message.content.startswith("!?mungoid"):
        ustring = message.content
        imgcreated = False
        if ustring.find('rgb') == 10:
            rgbhex = ustring[14:]
            rgbtuple = mungoid.hex_to_rgb(rgbhex)
            mungoid.create_image(rgb=rgbtuple)
            imgcreated = True
        else:
            try:
                mungoid.create_image(color=ustring[10:])
                imgcreated = True
            except ValueError:
                await message.channel.send("Unrecognized color. Use `!?mungoid rgb <hex-value>` for custom colors.")

        if imgcreated:
            time.sleep(1.5)
            am_image = discord.File('buffer/mungoid.png')
            await message.channel.send(file=am_image)


    if message.content == "!?help":
        htext = open('assets/help.txt')
        await message.channel.send(htext.read())

    if message.content.find("she") != -1 or message.content.find("her") != -1:
        print("Kicking User:", message.author.name)
        await message.channel.send("https://cdn.discordapp.com/attachments/656309791194349576/962183853601079346/laser.png")

client.run(TOKEN)
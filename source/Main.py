import asyncio
import os
import discord
import plankton
import mungoid
import mundochain
import pickle
from dotenv import load_dotenv

#from source.mundochain import CooldownError


load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
client = discord.Client()

#Global Variables
players = dict()
modified_buffer = False
BACKUP_COOLDOWN = 300

async def backup_chain():
    global modified_buffer
    while True:
        await asyncio.sleep(BACKUP_COOLDOWN)
        try:
            if modified_buffer:
                print("Backing up player data...")
                with open('buffer/mc-leger.pickle', 'wb') as f:
                    global players
                    pickle.dump(players, f, pickle.HIGHEST_PROTOCOL)
                modified_buffer = False
        except UnboundLocalError:
            modified_buffer = False

client.loop.create_task(backup_chain())

@client.event
async def on_ready():
    #Attempt to open leger file for mundochain
    try:
        with open('buffer/mc-leger.pickle', 'rb') as f:
            global players
            players = pickle.load(f)
    except EOFError:
        print("Chian file not found")
    print('We have logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
    global modified_buffer

    if message.author == client.user:
        return

    if message.content.startswith("!?mundo"):
        await message.channel.send("https://media.discordapp.net/attachments/768840996347052042/831901847190372362/real.png")

    if message.content.startswith("!?date"):
        plankton.create_image()
        asyncio.sleep(1)
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
            asyncio.sleep(1.5)
            am_image = discord.File('buffer/mungoid.png')
            await message.channel.send(file=am_image)

    if message.content.startswith('!?init'):
        if message.content == '!?init -forcereset':
            players[message.author.id] = mundochain.Player(message.author.name)
            modified_buffer = True
        else:
            try:
                players[message.author.id]
                await message.channel.send("You have already setup an account on MundoChain, use `!?init -forcereset` to reset your account\n**You will lose all coins!!!**")
            except KeyError:
                players[message.author.id] = mundochain.Player(message.author.name)
                await message.channel.send("Account has been setup, start mining and minting!")
                modified_buffer = True

    if message.content.startswith('!?coin mine'):
        #Confirm User ID is valid in player dictionary
        try:
            #Confirm cooldown has not been reached
            try:
                amount = players[message.author.id].mine()
                await message.channel.send("You just successfully mined **" + str(int(amount)) + "** MundoCoins")
                modified_buffer = True
            except mundochain.CooldownError:
                #TODO: replace with timer
                await message.channel.send("Mining is on cooldown! Wait until: " + str(players[message.author.id].mining_cooldown))
        except KeyError:
            await message.channel.send("Your account has not been initalized, use `!?init`")

    if message.content.startswith('!?coin bal'):
        try:
            bal = players[message.author.id].balance
            await message.channel.send("Your balance is " + str(bal) + " MundoCoins")
        except KeyError:
            await message.channel.send("Your account has not been initalized, use `!?init`")

    if message.content.startswith('!?nft mint'):
        try:
            try:
                created_nft = message.content[11:]
                players[message.author.id].add_nft(created_nft, True)
                modified_buffer = True
                await message.channel.send("NFT: " + created_nft + " has been created!")
            except mundochain.CooldownError:
                await message.channel.send("Minting is on cooldown! Wait until: " + str(players[message.author.id].minting_cooldown))

        except KeyError:
            await message.channel.send("Your account has not been initalized, use `!?init`")

    if message.content == '!?nft owned':
        try:
            tosend = message.author.name + "'s owned NFTs\n"
            if len(players[message.author.id].owned) == 0:
                await message.channel.send("You do not own any NFTs! Use `!?nft mint` to create one.")
            else:
                for item in players[message.author.id].owned:
                    tosend += "-" + item + "\n"
                await message.channel.send(tosend)

        except KeyError:
             await message.channel.send("Your account has not been initalized, use `!?init`")

    if message.content.startswith('!!buff'):
        await message.channel.send(str(modified_buffer))
    
    if message.content.startswith('!!fb'):
        modified_buffer = True

    if message.content == "!?hello":
        await message.channel.send("Hello " + message.author.name)
    if message.content == "!?help":
        htext = open('assets/help.txt')
        await message.channel.send(htext.read())

    if message.content.find(" she ") != -1 or message.content.find(" her ") != -1:
        print("Kicking User:", message.author.name)
        await message.channel.send("https://cdn.discordapp.com/attachments/656309791194349576/962183853601079346/laser.png")

client.run(TOKEN)
import asyncio
import time
import datetime as dt
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
BACKUP_COOLDOWN = 150

async def backup_chain():
    global modified_buffer
    while True:
        await asyncio.sleep(BACKUP_COOLDOWN)
        try:
            if modified_buffer:
                curtime = time.localtime()
                stime = time.strftime("%H:%M:%S", curtime)
                print("Backing up player data..." + stime)
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
            await message.channel.send("Account has been setup, start mining and minting!")
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
                await message.channel.send("You just successfully mined **" + str(int(amount)) + "** MundoCoin")
                modified_buffer = True
            except mundochain.CooldownError:
                #Timer
                c_tup = mundochain.timeconvert(players[message.author.id].mining_cooldown)
                min_remain = c_tup[2]
                sec_remain = c_tup[3]
                await message.channel.send("Mining is on cooldown! Wait: " + str(min_remain) + " minutes " + str(sec_remain) + " seconds.")
                #await message.channel.send("Mining is on cooldown! Wait until: " + str(players[message.author.id].mining_cooldown))
        except KeyError:
            await message.channel.send("Your account has not been initalized, use `!?init`")

    if message.content.startswith('!?coin bal'):
        try:
            target_player = message.mentions[0] #throws IndexError
            try:
                bal = players[target_player.id].balance
                await message.channel.send(target_player.name + "'s balance is " + str(bal) + " MundoCoins")
            except KeyError:
                await message.channel.send("Mentioned user is not initalized in MundoChain")
        except IndexError:
            try:
                bal = players[message.author.id].balance
                await message.channel.send("Your balance is " + str(bal) + " MundoCoins")
            except KeyError:
                await message.channel.send("Your account has not been initalized, use `!?init`")

    if message.content.startswith('!?coin top'):
        leaderboard = [] #List of tuples with form (Name, Balance)
        index = 0
        for key in players:
            leaderboard.append((players[key].user, players[key].balance))
        leaderboard.sort(key = lambda x: x[1], reverse=True) #Sort leaderboard by balance
        index = 1
        output = "Top Balances:\n"
        for x in leaderboard:
            output += str(index)
            output += ". "
            output += x[0]
            output += " - "
            output += str(x[1])
            output += "\n"
            index += 1
            if index > 10:
                break
        await message.channel.send(output)    


    if message.content.startswith('!?nft mint'):
        try:
            try:
                created_nft = message.content[11:]
                players[message.author.id].add_nft(created_nft, True)
                modified_buffer = True
                await message.channel.send("NFT: " + created_nft + " has been created!")
            except mundochain.CooldownError:
                #Calculate time difference between now and cooldown
                c_tup = mundochain.timeconvert(players[message.author.id].minting_cooldown)
                days_remain = c_tup[0]
                hours_remain = c_tup[1]
                min_remain = c_tup[2]
                sec_remain = c_tup[3]
                await message.channel.send("Minting is on cooldown! Wait: " + str(days_remain) + " days, " + str(hours_remain) + " hours, " + str(min_remain) + " minutes, " + str(sec_remain) + " seconds.")
                #await message.channel.send("Minting is on cooldown! Wait until: " + str(players[message.author.id].minting_cooldown))

        except KeyError:
            await message.channel.send("Your account has not been initalized, use `!?init`")

    if message.content.startswith('!?nft prev'):
        created_nft = message.content[11:]
        await message.channel.send("NFT will display as: " + created_nft)

    if message.content.startswith('!?nft cd'):
        cooldown = players[message.author.id].minting_cooldown
        c_tup = mundochain.timeconvert(cooldown)
        days_remain = c_tup[0]
        hours_remain = c_tup[1]
        min_remain = c_tup[2]
        sec_remain = c_tup[3]
        if dt.datetime.now() < cooldown:
            await message.channel.send("Minting cooldown: " + str(days_remain) + " days, " + str(hours_remain) + " hours, " + str(min_remain) + " minutes, " + str(sec_remain) + " seconds.")
        else:
            await message.channel.send("Minting is ready!")


    if message.content.startswith('!?nft owned'):
        try:
            target_player = message.mentions[0] #Throws IndexError if no player is mentioned
            try:
                tosend = target_player.name + "'s owned NFTs\n"
                if len(players[target_player.id].owned) == 0:
                    await message.channel.send(target_player.name + " does not own any NFTs!")
                else:
                    nft_id = 1
                    for item in players[target_player.id].owned:
                        tosend += str(nft_id) + ". " + item + "\n"
                        nft_id += 1
                    await message.channel.send(tosend)
            except KeyError:
                await message.channel.send("Mentioned user is not initalized in MundoChain")
        except IndexError:
            try:
                tosend = message.author.name + "'s owned NFTs\n"
                if len(players[message.author.id].owned) == 0:
                    await message.channel.send("You do not own any NFTs! Use `!?nft mint` to create one.")
                else:
                    nft_id = 1
                    for item in players[message.author.id].owned:
                        tosend += str(nft_id) + ". " + item + "\n"
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
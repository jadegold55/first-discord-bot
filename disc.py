# bot.py
# This example requires the 'message_content' intent.
import asyncio
import operator
import random
from typing_extensions import List
import discord
import nacl
from os import environ as env
import crawl

from dotenv import load_dotenv

load_dotenv()

token = env["TOKEN"]
global parroted_user
global infected_user
global voice_mentioned
global spongecmdCounter
global ignore_user
spongecmdCounter = 0
quotes = crawl.quote
guild_id = int(env["GUILD_ID"])
gen_chnl_txt_id = int(env["GENERAL_CHAT"])
channel_one = int(env["CHANNEL1"])
channel_two = int(env["CHANNEL2"])
channel_three = int(env["CHANNEL3"])
channel_four = int(env["CHANNEL4"])

# clean up data storing
# create regex for quotes
# figure out arrays in config files
# add more emotes features
# long term goal- switch to slash commands
# upload bot for public use
# have bot run in cloud server

class spongeBot(discord.Client):
    async def on_ready(self):
        print(f"logged in as {self.user}")
        print("----")

    async def on_message(self, message: discord.Message):
        global infected_user
        global mommmy
        list_of_things_to_respond_with_quote = ['show', 'spongebob', 'patrick', 'gary',
                                                'sad', 'depressed', 'bad day', 'bob', 'crying', 'hey',
                                                'miserable', 'squid', 'squidward', 'bikini', 'bikini bottom',
                                                'pineapple', 'rock']
        if (
            message.author.id == self.user.id or message.raw_mentions == self.user.id
        ):  # if bot is called in an @ for any commands(current build)
            return
        elif any(word in message.content for word in list_of_things_to_respond_with_quote):
            await message.channel.send(random.choice(quotes)) 
            #regex it
        elif message.content.startswith("!sponge"):
            # If user is running a command
            await on_sponge_cmd(message)
        elif message.content.startswith("!join") or message.content.startswith("!move"):
            # sends to seperate cmd handler for voice
            await on_voice_cmd(message)
        elif message.content.__contains__("sponge"):
            # emote(more features can be added)
            await message.add_reaction("<:spongebob_bored:1181025239426138202>")
        elif (
            infected_user is not None and message.author.id == infected_user
        ):  # follows user once tagged with infect
            await reply_with_squawk(message)
            # add cooldown for this command to avoid rate limit
            # user will continue to be tracked 


async def on_sponge_cmd(message: discord.Message):
    global infected_user
    global parroted_user
    clean_message = message.content.replace("!sponge", "")  # Message without !sponge
    msg_lst = message.content
    if operator.contains(msg_lst, "@") and operator.contains(msg_lst, "infect"):
        # If user was tagged, track them
        infected_user = message.raw_mentions[0]  # store user
    elif operator.contains(msg_lst, '@') and operator.contains(msg_lst, 'parrot'):
        parroted_user = message.raw_mentions[0]
        await look_through_history_messages_from_parroted(message=message)
    elif len(clean_message) > 0:
        # If no user was tagged, reply to them with squawk
        await reply_with_squawk(message) # Reply with squawked message
    else: # if not greater than 0 and no actions asked for from user
        global spongecmdCounter
        global ignore_users
        ignore_user = [] # create list of user annoying sponge
        ignore_user.append(message.author.id) # 
        if ignore_user.__contains__(message.author.id):
            spongecmdCounter += 1
        if spongecmdCounter == 5:
            await message.channel.send('not listening anymore')
            spongecmdCounter = 0
            ignore_user = message.author.id
            guild = client.get_guild(guild_id)
            mutedRole = await guild.create_role(name="Muted")
            for channel in guild.channels:
                await channel.set_permissions(mutedRole, send_messages=False)
            await message.author.add_roles(mutedRole,reason='annoying')
            await message.channel.send(f"Muted <@{message.author.id}> for disrupting sponge")
            await asyncio.sleep(30)
            await message.author.remove_roles(mutedRole)

        else:
            list_of_responses = ['WHAT', 'what is it', '...', 'hello', 'im ready, im ready, im ready, im ready', 'listening', 'yes', 'LISTENING', 'WHATTTTTTTT' ]
            await message.channel.send(random.choice(list_of_responses)) #mute reset not working properly, when other users annoy sponge
            # the bot should optimally count the times that user sent it and keep track of each user's annoyance


async def look_through_history_messages_from_parroted(message: discord.Message): 
    # looks through history and replies with a random user message that has been previously sent
    channel_id = client.get_channel(gen_chnl_txt_id)
    i = 0
    async for messages in channel_id.history(limit=100):
        i += 1
        if messages.author.id == parroted_user and i < 50:
            parrot_message = messages       
    needed_message = await message.channel.fetch_message(parrot_message.id)
    await message.channel.send(needed_message.content)


async def reply_with_squawk(message: discord.Message):
    msg_wo_cmd = message.content.replace("!sponge", "")
    new_msg = squawk_str(msg_wo_cmd)
    await message.reply(new_msg, mention_author=False)


def squawk_str(squawk):
    index = random.randint(0, 1)
    parrot = ""
    for char in squawk:
        index += 1
        if index % 2 == 0:
            parrot += char.lower()
        else:
            parrot += char.upper()
    return parrot


async def connect_and_play(member: discord.Member):
    channel = (
        member.voice.channel
    )  # creates channel object for the current user's channel
    vc = await channel.connect()
    list_of_sounds = [
        r"C:/Users/cgold/Desktop/bot/r.mp3",
        r"C:/Users/cgold/Desktop/bot/hi.mp3",
        r"C:/Users/cgold/Desktop/bot/foghorn.mp3",
    ] # config variable
    rand = random.randint(0, 2)
    length = 3
    if rand == 2:
        length = 7
    player = discord.FFmpegPCMAudio(
        source=list_of_sounds[rand],
        executable=r"C:/ffmpeg/ffmpeg.exe",
    )
    vc.play(player)
    await asyncio.sleep(length) # can add more sounds, also figure out how to store length as data for the path

    await vc.disconnect()


async def on_voice_cmd(message: discord.Message):
    global voice_mentioned  
    guild = client.get_guild(guild_id)  # create guild object
    if message.content.__contains__("@"):
        voice_mentioned = message.raw_mentions[0]  # grab the reference user's id
        member = guild.get_member(voice_mentioned)  # make user a member object
        if message.content.startswith("!join"):  # bot joins user's channel
            await connect_and_play(member=member)
        else:
            await message.reply(
                f"i aM mOvInG yOu, <@{member.id}>,  BaHaHaHa HaHahahAha!!!!!!",
                mention_author=False,
            )
            await move_user(member=member, guild=guild)
    else:
        if message.author.voice is not None:
            member = guild.get_member(
                message.author.id
            )  # member object from message author since no mention
            if message.content.startswith("!join"):
                await connect_and_play(member=member)
            else:
                await message.reply("i Am MoViNg YoU ", mention_author=True)
                await move_user(member=member, guild=guild)
        else:
            await message.reply("yOu NeEd To Be CoNnEcTeD, GaRy!")


async def move_user(member: discord.Member, guild: discord.Guild):
    if member.voice is not None:
        ids_of_channels = [
            channel_one,
            channel_two,
            channel_three,
            channel_four,
        ] # user environment/ config variable for array

        rand = random.randint(0, 3)
        channel = guild.get_channel(
            ids_of_channels[rand]
        )  # randomize the channel being moved to
        await member.move_to(channel=channel, reason=None)  # moves member
        await connect_and_play(member)  # send to func



intents = discord.Intents.default()
intents.message_content = True
intents.voice_states = True

client = spongeBot(intents=intents)
client.run(token=token)
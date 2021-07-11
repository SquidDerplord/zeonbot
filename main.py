from replit import db
import os
import requests
import json
import random
import math
import time
import re
import typing
from datetime import datetime
import pytz
import asyncio
import tznameconv
import ffmpeg
import youtube_dl

import discord
from discord.ext import commands
from keep_alive import keep_alive     #Creates a webserver that allows pings from UptimeRobot to prevent zeonbot from stoping

print("Starting...")
TOKEN = os.getenv('TOKEN')
zeonid = int(os.getenv('OWNERID'))
botid = 806908019291717702
bot = commands.Bot(command_prefix=["z.", "zeon."])
print("Logging in..")

botadminid = [300552090613317632,202734950699499522,284271809183088643]
@bot.event
async def on_ready():
    await bot.change_presence(activity=discord.Game('z.help'))
    global zeonuser
    global logchannel
    logchannel = bot.get_channel(817301856963002408)
    zeonuser = await bot.fetch_user(zeonid)

    print('Logged in as')
    print(f'Bot Name: {bot.user}')
    print(f'Bot ID: {bot.user.id}')
    print('===================')
    await logchannel.send('Bot started')


#bot commands----------------------------------------------

#checks bt latency
@bot.command()
async def ping(ctx):
    """Pings the bot"""
    output = f'Pong! {round(bot.latency * 1000)}ms'
    await ctx.send(output)


#lists database items with prefix provided
@bot.command(hidden=True)
async def dblist(ctx, prefix: typing.Optional[str]=None):
    """shows db info based on prefix"""
    await ctx.send(prefix)
    if prefix is None:
      output = "Please insert a prefix"
    else:
      output = db.prefix(prefix)
    await ctx.send(output)
#--------------------------------------------------------


#basic commands--------------------------------------------

#repeats text
@bot.command(aliases=['say', 'repeat'])
async def echo(ctx, *, text):
    """Have the bot repeat what you say."""
    output = text
    await ctx.send(output)


#Reverses text
@bot.command()
async def reverse(ctx, *, text):
    """Reverses the text.txet eht sesreveR"""
    output = text[::-1]
    await ctx.send(output)


#Rates out of 10
@bot.command()
async def rate(ctx, *text):
    """Rates a thing out of 10."""
    if not text:
        text = ctx.author.name
    else:
        text = " ".join(text)
    output = f'I rate **{text}** a `{random.randint(0,100)/10}` out of 10.'
    await ctx.send(output)


#Random number between num provided
@bot.command()
async def rng(ctx, num1, num2):
    """Have the bot pick a random number of your choice."""
    num1 = int(num1)
    num2 = int(num2)
    mn = min(num1,num2)
    mx = max(num1,num2)
    """if num1 < num2:
        min = num1
        max = num2
    elif num2 < num1:
        min = num2
        max = num1
    elif num1 == num2:
        min = num1
        max = num2
    else:
        pass"""
    output = f'Number generated is: `{random.randint(mn,mx)}`'
    await ctx.send(output)


#Flips a fair 50/50 coin
@bot.command(aliases=['coin', 'flip'])
async def coinflip(ctx):
    """Flips a fair 50/50 coin"""
    chance = random.random(0,1)
    if chance <= 0.49:
        output = 'The coin landed on `HEADS`!'
    elif chance >= 0.51:
        output = 'The coin landed on `TAILS`!'
    else:
        output = 'Unbelievable!! The coin landed on its `SIDE`!'
    await ctx.send(output)


#Sends profile picture of user
@bot.command(aliases=['pfp'])
async def avatar(ctx, *,  avamember : discord.Member=None):
    """Sends profile picture of user"""
    author = ctx.message.author
    if avamember is None:
      userAvatarUrl = author.avatar_url
      await ctx.send(userAvatarUrl)
    else:
      userAvatarUrl = avamember.avatar_url
      await ctx.send(userAvatarUrl)
    

#time related--------------------------------------------------

#Shows current time in MST
@bot.command(aliases=['time'])
async def ntime(ctx):
    """Shows current time in MYT"""
    output = "<t:" + str(int(time.time())) + ">"
    await ctx.send(output)

#Day(s) before or from now
@bot.command(aliases=[])
async def dadd(ctx, text: typing.Optional[str]="0"):
    """Day(s) before or from now"""
    try:
      text = int(text)
    except:
      text = 0
      await ctx.send("expected int(defaulting to 0)")
    if int(text) > 0:
      msg = str(text) + " day(s) from now is:"
    elif int(text) < 0:
      msg = str(str(text).replace("-", "")) + " day(s) ago from now was:"
    else:
      msg = "Today is:"
    unix = int(time.time()) + int(int(text)*86400)
    output = "<t:" + str(unix) + ">"
    await ctx.send(msg)
    await ctx.send(output)

#Shows author time and target time
@bot.command(hidden=True)
async def tz(ctx, text: typing.Optional[str]="my"):
    """Shows your local time and target time"""
    hastz = True
    author = ctx.message.author
    key = "tz_id" + str(author.id)
    try:
      db[key]
    except:
      hastz = False
      pass
    if hastz == False:
      output = "Seems like you don't have a timezone set."
    else:  
      key = "tz_id" + str(author.id)
      authorzone = str(db[key])
      authorzonetime = datetime.now(pytz.timezone(authorzone))
      output = "Your time now is " + authorzonetime.strftime("%I:%M:%S")
    tzname = tznameconv.GetTimeZoneName(' ',text)
    targettime = datetime.now(pytz.timezone(tzname))
    output2 = "Target time(" + text + "/" + tzname + ") is " + targettime.strftime("%I:%M:%S")
    await ctx.send(output)
    await ctx.send(output2)

    #tz_MY = pytz.timezone('Asia/Kuala_Lumpur') 
    #datetime_MY = datetime.now(tz_MY)
    #await ctx.send(datetime_MY.strftime("%I:%M:%S"))

#converts time to author timezone
@bot.command()
async def tconv(ctx, text, *, input):
    """Converts time into your local time"""
    hastz = True
    #get author timezone name
    authortzname = db["tz_id" + str(ctx.author.id)]
    #if ping get pinged tz name, else use country get tz name
    if len(text)>2:
      text = text[3:]
      text = text[:-1]
      #gets target user tz from db
      try:
        targettzname = db["tz_id" + text]
      except:
        hastz = False
    else:
      targettzname = tznameconv.GetTimeZoneName(' ',text)
    if hastz == False:
      output = "User mentioned has no timezone set."
    else:
      #sets author n target timezone
      authortz = pytz.timezone(authortzname)
      targettz = pytz.timezone(targettzname)
      #utc day month & year
      if input =="now":
        targettime = targettz.localize(datetime.now())
      else:
        utctime = datetime.now()
        year = int(utctime.strftime("%Y"))
        month = int(utctime.strftime("%m"))
        day = int(utctime.strftime("%d"))
        #converts input time 12hr -> 24hr
        input = datetime.strptime(input, '%I:%M %p')
        #get input hr and min
        hour = int(input.strftime("%H"))
        min = int(input.strftime("%M"))
        #sets target time to input time
        targettime = targettz.localize(datetime(year, month, day, hour, min, 0))
      #converts time from target tz to author tz
      authortime = targettime.astimezone(authortz)
      #converts author time and target tiem into str
      targettime = str(targettime)
      authortime = str(authortime)
      output = "`" + targettime[:-6] + "`\nin " + targettzname + ", is \n`" + authortime[:-6] + "`\nfor you in " + authortzname +"."
    await ctx.send(output)
#---------------------------------------------------------------------


#Advanced? commands----------------------------------------------
@bot.command(aliases=['math'])
async def calc(ctx, text):
    """does math"""
    text = re.sub("`|```", "", text)
    text = text.replace("^", "**")
    text = text.replace("÷", "/")
    text = text.replace("x", "*")
    text = text.replace("math.sin", "sin")
    text = text.replace("math.cos", "cos")
    text = text.replace("math.tan", "tan")
    text = text.replace("sin", "math.sin")
    text = text.replace("cos", "math.cos")
    text = text.replace("tan", "math.tan")
    text = text.replace("math.sqrt", "sqrt")
    text = text.replace("sqrt", "math.sqrt")
    output = eval(text)
    await ctx.send(output)
#-------------------------------------------------------------


#meme commands-------------------------------------------------

#cockrate
@bot.command(hidden=True)
async def cockrate(ctx, *, member: discord.User=None):
    """Rates your cock"""
    if member is None:
      rated = "your"
    else:
      rated = "<@!"+ str(member.id) + "> 's"
    score = random.randint(1,10)
    if score == 10:
      output = "I rate " + str(rated) + " cock a ROCK SOLID " + str(score) + "/10." + "\nNice cock🍆 bro😉!"
    elif score < 6:
      output = "I rate " + str(rated) + " cock a flacid " + str(score) + "/10."
    elif score > 5:
      output = "I rate " + str(rated) + " cock a solid " + str(score) + "/10."
    await ctx.send(output)


#willy
@bot.command(hidden=True)
async def willy(ctx):
    """Test output"""
    output = "Willy"
    output2 = "Willlllly!"
    output3 = "TUN TUN TUN TUN TUNNN"
    await ctx.send(output)
    await asyncio.sleep(1.1)
    await ctx.send(output2)
    await asyncio.sleep(0.8)
    await ctx.send(output3+"\nhttps://cdn.discordapp.com/attachments/811835420232777788/863072087739334677/VID_27540412_072830_835.mp4")


#raud
@bot.command(hidden=True)
async def raud(ctx):
    """raud"""
    await ctx.send(file=discord.File('audio/Sussy Raud.mp3'))


#negus
@bot.command(hidden=True)
async def negus(ctx):
    """negus"""
    await ctx.send(file=discord.File('audio/negus.mp3'))


@bot.command(hidden=True)
async def negusvc(ctx):
    # grab the user who sent the command
    inVc = True
    try:
      voice_channel = ctx.author.voice.channel
    except:
      inVc = False
    if inVc != False:
      vc = await voice_channel.connect()
      await asyncio.sleep(1)
      vc.play(discord.FFmpegPCMAudio('audio/negus.mp3'), after=lambda e: print('done', e))
      # Sleep while audio is playing.
      while vc.is_playing():
        await asyncio.sleep(.1)
      await asyncio.sleep(1)
      await vc.disconnect()
    else:
      await ctx.send(str(ctx.author.name) + " is not in a channel.")
    # Delete command after the audio is done playing.
    await ctx.message.delete()


@bot.command(hidden=True)
async def willyvc(ctx):
    # grab the user who sent the command
    inVc = True
    try:
      voice_channel = ctx.author.voice.channel
    except:
      inVc = False
    if inVc != False:
      vc = await voice_channel.connect()
      await asyncio.sleep(1)
      vc.play(discord.FFmpegPCMAudio('audio/willy.mp3'), after=lambda e: print())
      # Sleep while audio is playing.
      while vc.is_playing():
        await asyncio.sleep(.1)
      await asyncio.sleep(1)
      await vc.disconnect()
    else:
      await ctx.send(str(ctx.author.name) + " is not in a channel.")
    # Delete command after the audio is done playing.
    await ctx.message.delete()


@bot.command(hidden=True)
async def oops(ctx):
    # grab the user who sent the command
    inVc = True
    try:
      voice_channel = ctx.author.voice.channel
    except:
      inVc = False
    if inVc != False:
      vc = await voice_channel.connect()
      await asyncio.sleep(1)
      vc.play(discord.FFmpegPCMAudio('audio/oops.mp3'), after=lambda e: print('done', e))
      # Sleep while audio is playing.
      while vc.is_playing():
        await asyncio.sleep(.1)
      await asyncio.sleep(1)
      await vc.disconnect()
    else:
      await ctx.send(str(ctx.author.name) + " is not in a channel.")
    # Delete command after the audio is done playing.
    await ctx.message.delete()


@bot.command(hidden=True)
async def rickroll(ctx):
    # grab the user who sent the command
    inVc = True
    try:
      voice_channel = ctx.author.voice.channel
    except:
      inVc = False
    if inVc != False:
      vc = await voice_channel.connect()
      await asyncio.sleep(1)
      vc.play(discord.FFmpegPCMAudio('audio/song.mp3'), after=lambda e: print('done', e))
      # Sleep while audio is playing.
      while vc.is_playing():
        await asyncio.sleep(.1)
      await asyncio.sleep(1)
      await vc.disconnect()
    else:
      await ctx.send(str(ctx.author.name) + " is not in a channel.")
    # Delete command after the audio is done playing.
    await ctx.message.delete()

#saddam
@bot.command(hidden=True)
async def saddam(ctx):
    """saddam"""
    output = "https://i.kym-cdn.com/photos/images/original/002/137/709/976.png"
    await ctx.send(output)
#----------------------------------------------------------------------------


#misc commands-------------------------------------

#waifu
@bot.command(aliases=['w'])
async def waifu(ctx, *text):
    """妻"""
    await ctx.send(":frame_photo:| Random waifu pic.")
    text = " ".join(text)
    if text.lower() != 'nsfw':
      response = requests.get('https://waifu.pics/api/sfw/waifu')
      url = json.loads(response.text)['url']
      await ctx.send(url)
    else:
      if ctx.author.id in botadminid:
        await ctx.send("https://images-ext-2.discordapp.net/external/fim3-auuWU5xUYsheqK4mcQvZw1VE-D8zYGMtRWMRrc/https/i.kym-cdn.com/photos/images/original/002/137/709/976.png")
      else:
        await ctx.send('This is not the bot for you')

#cat
@bot.command(hidden=True,aliases=['catto'])
async def cat(ctx):
    """Sends a random picture of asha's cat X3"""
    filename = 'catto/{0}'.format(random.choice(os.listdir('catto/')))
    await ctx.send(':frame_photo:| **Here\'s a cat picture :cat:**',
                   file=discord.File(filename))
#----------------------------------------------------


#WIP-------------------------------------------------
@bot.command(hidden=True)
async def choose(ctx):
    """WIP"""
    await ctx.send('random choice')


@bot.command(hidden=True)
async def remind(ctx):
    """WIP"""
    await ctx.send('wip')


@bot.command(hidden=True)
async def quiz(ctx):
    """WIP"""
    await ctx.send('work in progress')


@bot.command(hidden=True)
async def test(ctx):
    # grab the user who sent the command
    inVc = True
    try:
      voice_channel = ctx.author.voice.channel
    except:
      inVc = False
    if inVc != False:
      vc = await voice_channel.connect()
      vc.volume = 10 / 100
      vc.play(discord.FFmpegPCMAudio('https://www.youtube.com/watch?v=dQw4w9WgXcQ'), after=lambda e: print('done', e))
      # Sleep while audio is playing.
      while vc.is_playing():
        await asyncio.sleep(.1)
      await vc.disconnect()
    else:
      await ctx.send(str(ctx.author.name) + " is not in a channel.")
    # Delete command after the audio is done playing.
    await ctx.message.delete()

@bot.command()
async def play(ctx, url : str):
    song_there = os.path.isfile("song.mp3")
    try:
        if song_there:
            os.remove("song.mp3")
    except PermissionError:
        await ctx.send("Wait for the current playing music to end or use the 'stop' command")
        return

    #voiceChannel = discord.utils.get(ctx.guild.voice_channels, name='General')
    voice_channel = ctx.author.voice.channel
    await voice_channel.connect()
    voice = discord.utils.get(bot.voice_clients, guild=ctx.guild)

    ydl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
    }
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])
    for file in os.listdir("./"):
        if file.endswith(".mp3"):
            os.rename(file, "song.mp3")
    #state = bot.get_voice_state(ctx.message.server)
    #player = state.player
    voice.play(discord.FFmpegPCMAudio("song.mp3"))


@bot.command()
async def leave(ctx):
    voice = discord.utils.get(bot.voice_clients, guild=ctx.guild)
    if voice.is_connected():
        await voice.disconnect()
    else:
        await ctx.send("The bot is not connected to a voice channel.")


@bot.command()
async def pause(ctx):
    voice = discord.utils.get(bot.voice_clients, guild=ctx.guild)
    if voice.is_playing():
        voice.pause()
    else:
        await ctx.send("Currently no audio is playing.")


@bot.command()
async def resume(ctx):
    voice = discord.utils.get(bot.voice_clients, guild=ctx.guild)
    if voice.is_paused():
        voice.resume()
    else:
        await ctx.send("The audio is not paused.")


@bot.command()
async def stop(ctx):
    voice = discord.utils.get(bot.voice_clients, guild=ctx.guild)
    voice.stop()


@bot.command()
async def join(ctx):
    channel = ctx.author.voice.channel
    await channel.connect()
#----------------------------------------------------


#admin commands--------------------------------------------
@bot.command(hidden=True)
async def dm(ctx, userid: discord.User, *, text):
    if ctx.author.id in botadminid:
        try:
            await userid.send(text)
            print("DM sent to " + str(userid))
        except:
            print("DM failed sending to " + str(userid))

    
@bot.command(hidden=True)
async def tzset(ctx, tzvalue, member: discord.User=None):
    """tzset"""
    if ctx.author.id in botadminid:
      if member is None:
        member = ctx.message.author
      else:
        pass
      id = "tz_id" + str(member.id)
      value = str(tznameconv.GetTimeZoneName(' ',tzvalue))
      db[id] = value
      await ctx.send(id)
      stripout = id.strip("tz_id")
      await ctx.send(stripout)
      await ctx.send(value)
      print(db.prefix("tz_id"))
      print(db[id])
    else:
      await ctx.send("u no admin")
#------------------------------------------------------------

@bot.event
async def on_message(message):
    if isinstance(message.channel, discord.channel.DMChannel) and not message.author.bot and not message.author.id == zeonid:
        output = "**-->[DM]**`" + str(message.author) + "`: " + message.content
        print(output)
        #await zeonuser.send(output)
        await logchannel.send(output)
        if message.attachments:
          outputattach = ", ".join([i.url for i in message.attachments])
          #await zeonuser.send("Attachments: " + outputattach)
          await logchannel.send("Attachments: " + outputattach)

    await bot.process_commands(message)


keep_alive()
bot.run(TOKEN)


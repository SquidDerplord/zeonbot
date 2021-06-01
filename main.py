from replit import db
import os
import requests
import json
import random
import math
import datetime

import discord
from discord.ext import commands
from keep_alive import keep_alive     #Creates a webserver that allows pings from UptimeRobot to prevent zeonbot from stoping

TOKEN = os.getenv('TOKEN')
zeonid = int(os.getenv('OWNERID'))
botid = 806908019291717702
bot = commands.Bot(command_prefix=["z.", "zeon."])
print("Logging in..")


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


@bot.command()
async def ping(ctx):
    """Pings the bot"""
    output = f'Pong! {round(bot.latency * 1000)}ms'
    await ctx.send(output)


@bot.command()
async def rate(ctx, *text):
    """Rates a thing out of 10."""
    if not text:
        text = ctx.author.name
    else:
        text = " ".join(text)
    output = f'I rate **{text}** a `{random.randint(0,100)/10}` out of 10.'
    await ctx.send(output)


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


@bot.command()
async def reverse(ctx, *, text):
    """Reverses the text.txet eht sesreveR"""
    output = text[::-1]
    await ctx.send(output)


@bot.command(aliases=['say', 'repeat'])
async def echo(ctx, *, text):
    """Have the bot repeat what you say."""
    output = text
    await ctx.send(output)


@bot.command(aliases=['coin', 'flip'])
async def coinflip(ctx):
    """Flips a fair 50/50 coin"""
    chance = random.random()
    if chance <= 0.49:
        output = 'The coin landed on `HEADS`!'
    elif chance >= 0.51:
        output = 'The coin landed on `TAILS`!'
    else:
        output = 'Unbelievable!! The coin landed on its `SIDE`!'
    await ctx.send(output)

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


@bot.command(aliases=['w'])
async def waifu(ctx):
    """妻"""
    await ctx.send(":frame_photo:| Random waifu pic.")
    response = requests.get('https://waifu.pics/api/sfw/waifu')
    url = json.loads(response.url)["url"]
    await ctx.send(url)


@bot.command(hidden=True)
async def dm(ctx, userid: discord.User, *, text):
    if ctx.author.id == zeonid or ctx.author.id == 300552090613317632:
        try:
            await userid.send(text)
            print("DM sent to " + str(userid))
        except:
            print("DM failed sending to " + str(userid))


@bot.command(hidden=True)
async def test(ctx):
    """testing"""
    

@bot.command(hidden=True,aliases=['catto'])
async def cat(ctx):
    """Sends a random picture of asha's cat X3"""
    filename = 'catto/{0}'.format(random.choice(os.listdir('catto/')))
    await ctx.send(':frame_photo:| **Here\'s a cat picture :cat:**',
                   file=discord.File(filename))


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

  
import discord
from discord.ext import commands
from discord import TextChannel
from random import seed
from random import randint
from random import choice as randchoice
from datetime import datetime
from urllib.request import urlopen
from bs4 import BeautifulSoup
import re

dt = datetime.now()
seed(dt.second + dt.minute+dt.hour)

prefix = ","
bot = commands.Bot(command_prefix=commands.when_mentioned_or(prefix))
all_servers = bot.get_all_members()


@bot.event
async def on_ready():
    print("Tester Bot: Ready")


@bot.command()
async def test(ctx):
    await ctx.send("```test```")
    await ctx.send("smile! :smile:")
    await ctx.send("*italic*")
    await ctx.send("**bold**")
    await ctx.send("***bold italic***")


@bot.command()
async def channel(ctx, channel: TextChannel):
    await channel.edit(name="channel name update 2")


@bot.command()
async def random(ctx, arg1="", *args):
    if arg1:
        if arg1 in ("number", "num", "integer", "int"):
            num = randint(int(args[0]), int(args[1])) if args else randint(-1000, 1000)
            await ctx.send(str(num))
        else:
            # need to add an exception just in case arg1 is not recognized
            try:
                html = urlopen("https://en.wikipedia.org/wiki/"+arg1)
                bs = BeautifulSoup(html, "html.parser")
                images = bs.find_all("img", {"src": re.compile(".jpg")})
                ind = randint(0, len(images)-1)
                await ctx.send("https:" + images[ind]['src'])
            except:
                await ctx.send("{} is not accepted by Wikipedia!".format(arg1))

    else:
        await ctx.send("Command not recognized")


@bot.command()
async def say(ctx, *args):
    if args:
        await ctx.send(" ".join(args))
    else:
        await ctx.send("You didn't type anything tho")


@bot.command()
async def add(ctx, *args):
    num = sum(map(int, args))
    await ctx.send("{} = {}".format(" + ".join(args), num))


@bot.command()
async def slap(ctx, members: commands.Greedy[discord.Member], *, reason='no reason'):
    slapped = ", ".join(x.name for x in members)
    await ctx.send('{} just got slapped for {}'.format(slapped, reason))


@bot.command()
async def pingmepls(ctx):
    await ctx.send("nickname: {}".format(ctx.author.nick))
    await ctx.send("discord username: {}".format(ctx.author.name))
    await ctx.send("full discord username: {}".format(ctx.author))
    await ctx.send("mention: {}".format(ctx.author.mention))


@bot.command()
async def membercount(ctx):
    current_id = ctx.message.guild.id
    for server in all_servers:
        if server.guild.id == current_id:
            name = ctx.message.guild.name
            count = ctx.message.guild.member_count
            await ctx.send("**{}** currently has **{}** members".format(name, count))


@bot.command()
async def greeting(ctx):
    word = randchoice(("Hello!", "How's your day?", "Hi!", "How are you?", "Greetings!", "Hi, I have a cat!"))
    await ctx.send(word)


@bot.command()
async def cat(ctx):
    await ctx.send("https://genrandom.com/cats/")


bot.run("token")

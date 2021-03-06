# imports
import re
from datetime import datetime
from random import seed, randint, choice as randchoice
from urllib.request import urlopen
import json

import discord
from bs4 import BeautifulSoup
from discord import TextChannel
from discord.ext import commands

# initiations
dt = datetime.now()
seed(dt.second + dt.minute + dt.hour)

prefix = ","
intents = discord.Intents.all()
bot = commands.Bot(command_prefix=commands.when_mentioned_or(prefix), intents=intents, help_command=None)
client = discord.Client()
all_servers = bot.get_all_members()

color = discord.Color.from_rgb(255, 153, 153)

with open("BibleBooks.json", "r") as f:
    bible_books = json.load(f)


# events
@bot.event
async def on_ready():
    print("Tester Bot: Ready")


@bot.event
async def on_member_join(member):
    await member.send("Hello, {}! Welcome to the server!".format(member.mention))
    await bot.get_channel(806613504109838346).send("Say hi to {}!".format(member.mention))
    # currently sending to dev server jl channel


@bot.event
async def on_member_remove(member):
    await bot.get_channel(806613504109838346).send("{} left, may we live in grief...".format(member.mention))


# commands using bot
@bot.command()
async def help(ctx, area="commands"):
    embed_block = discord.Embed(title="Alpha Bot", description="Some of alpha-bots less useless commands", color=color)
    if area not in ("commands", "events"):
        area = "commands"
    with open("EventsAndCommands.json", "r") as f:
        data = json.load(f)
    for command in data[area]:
        embed_block.add_field(name="`" + str(command) + "`", value=str(data[area][command]["description"]),
                              inline=False)
    await ctx.channel.send(embed=embed_block)


@bot.command()
async def random(ctx, arg1="", *args):
    if arg1:
        if arg1 in ("number", "num", "integer", "int"):
            if args[1]<args[0]:
                args = (args[1], args[0])
            num = randint(int(args[0]), int(args[1])) if args else randint(-1000, 1000)
            await ctx.send(str(num))
        elif arg1 in ("choice", "yesno", "pick"):
            choice = randchoice(("Yes :white_check_mark:", "No :x:"))
            await ctx.send(choice)
        else:
            try:
                html = urlopen("https://en.wikipedia.org/wiki/" + arg1)
                bs = BeautifulSoup(html, "html.parser")
                images = bs.find_all("img", {"src": re.compile(".jpg")})
                ind = randint(0, len(images) - 1)
                await ctx.send("https:" + images[ind]['src'])
            except:
                await ctx.send("'{}' is not accepted by Wikipedia!".format(arg1))

    else:
        await ctx.send("Command not recognized")


@bot.command()
async def dice(ctx, sides=6):
    if sides < 0:
        await ctx.send(f"You cant have a {sides} sided die. Stop trying to enter the 4th dimension!")
        return
    elif sides == 0:
        nick = ctx.author.nick if ctx.author.nick else ctx.author.name
        await ctx.send(f"Use your brain {nick}, how is that even possible?")
        return
    num = randint(1, sides)
    await ctx.send(":game_die: " + str(num) + " :game_die:")


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
async def pingmepls(ctx):
    await ctx.send("nickname: {}".format(ctx.author.nick))
    await ctx.send("discord username: {}".format(ctx.author.name))
    await ctx.send("full discord username: {}".format(ctx.author))
    await ctx.send("mention: {}".format(ctx.author.mention))


@bot.command()
async def membercount(ctx):
    await ctx.send(
        "**{}** currently has **{}** members!".format(ctx.message.guild.name, ctx.message.guild.member_count))


@bot.command()
async def boop(ctx, victims: commands.Greedy[discord.Member], *, times="3"):
    times = times.split()
    if times[0] == "me":
        victims = [ctx.author]
        times = times[1:]
        if not len(times):
            times.append("3")
    try:
        int(times[0])
    except ValueError:
        await ctx.send("You can't ***BOOP*** '{}'. Be better.".format(*times))
        return
    msg = ""
    for victim in victims:
        msg += victim.mention + " "
    msg = "***BOOP*** " + msg * int(times[0])
    if len(msg) > 2000:
        await ctx.send("Message over 2000 characters")
    else:
        await ctx.send(msg)


@bot.command()
async def annoy(ctx, victims: commands.Greedy[discord.Member], *, times="3"):
    try:
        int(times)
    except ValueError:
        await ctx.send("'{}' is immune to being annoyed.".format(times))
        return
    if int(times) > 30:
        await ctx.send("I may be a robot, but at least I have more empathy than {}!".format(ctx.author.mention))
    else:
        victims = victims[0]
        await ctx.send("I am just a robot, blame {}.".format(ctx.author.mention))
        for i in range(1, int(times) + 1):
            await ctx.send("Currently annoying: {}, {}/{}".format(victims.mention, i, int(times)))
        await ctx.send("Sorry {}!".format(victims.nick))


@bot.command()
async def bible(ctx, *args):
    if args:
        query = "".join(args).replace(" ", "").split(":")
        chapter = ""
        while query[0] and query[0][-1].isdigit():
            chapter = query[0][-1] + chapter
            query[0] = query[0][:-1]

        url = f"https://www.biblegateway.com/passage/?search={query[0]}+{chapter}%3A+{query[1]}&version=NIV"
        html = urlopen(url)
        soup = BeautifulSoup(html, "html.parser")
        title = soup.find("meta", property="og:title")
        description = soup.find("meta", property="og:description")

        if not title or not description:
            await ctx.send("That verse does not exist :cry:")
            return

        embed_block = discord.Embed(title=" ", description=" ", color=color)
        embed_block.add_field(name=title["content"][23:-28] + " :book:", value=description["content"], inline=False)
        embed_block.set_footer(text=url)
        await ctx.channel.send(embed=embed_block)

    else:
        await ctx.send("Please enter a query: `<book>` `<chapter>`: `<verse start>` - `<verse end>`")
        
        
emoji_prefixes = ("person", "woman", "man")
emoji_types = (
    "bowing", "tipping_hand", "gesturing_no", "gesturing_ok", "raising_hand", "facepalming", "shrugging", "pouting",
    "frowning", "getting_haircut", "getting_massage", "in_steamy_room")
emoji_suffixes = ("", "_tone1", "_tone2", "_tone3", "_tone4", "_tone5")


@bot.command()
async def face(ctx, num="1"):
    try:
        if int(num) > 10:
            await ctx.send("Too many faces, do you have a fetish?")
            return
        elif int(num) <= 0:
            await ctx.send(f"I can't send {num} faces.")
            return

        message = ""
        for i in range(int(num)):
            pre_ = randchoice(emoji_prefixes)
            type_ = randchoice(emoji_types)
            suf_ = randchoice(emoji_suffixes)
            message += f":{pre_}_{type_}{suf_}:"
        await ctx.send(message)
    except ValueError:
        await ctx.send("Thats not a whole number ..")


# commands using client
# nothing here because bot > client

with open("BotToken.txt", "r") as token:
    bot.run(token.read().strip())

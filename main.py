import nextcord as discord
import os
from dotenv import load_dotenv
from nextcord.ext import commands

load_dotenv()

DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")

intents = discord.Intents.all()

bot = commands.Bot(command_prefix = "$", intents = intents)


@bot.command(
    name = "ping",
    help = "Pongs back at ya. That's all.",
    brief = "pong"
)
async def finally_work_pls(ctx):
    await ctx.channel.send(f"pong :ping_pong:\nMy latency is **{round(bot.latency*1000)} ms**")



@bot.command()
async def GetCarListing(ctx):
    def check_author(m):
        if m.author == ctx.author and m.channel == ctx.channel:
            return True
        return False
    def check_if_num(m):
        if m.author == ctx.author and m.channel == ctx.channel:
            try:
                float(m.content)
                return True
            except:
                return False
        return False
    
    def check_zip(m):
        if m.author == ctx.author and m.channel == ctx.channel and len(m.content.trim()) == 5:
            try:
                int(m.content)
                return True
            except:
                return False
        return False
    await ctx.send("What is your name?")
    name = await bot.wait_for("message", check=check_author)
    await ctx.send("What is your favorite color?")
    color = await bot.wait_for("message", check=check_author)
    await ctx.send("Enter a number")
    number = await bot.wait_for("message", check=check_if_num)
    await ctx.send("Enter your zip code")
    zip_code = await bot.wait_for("message", check=check_zip)
    await ctx.send(f"Hi {name.content}, who likes {color.content}. You enetered {float(number.content)}. Zip is {zip_code}")

bot.run(DISCORD_TOKEN)
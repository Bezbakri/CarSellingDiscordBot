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
    await ctx.send("What is your name?")
    name = await bot.wait_for("message", check=check_author)
    await ctx.send("What is your favorite color?")
    color = await bot.wait_for("message", check=check_author)
    await ctx.send(f"Hi {name.content}, who likes {color.content}")

bot.run(DISCORD_TOKEN)
import nextcord as discord
import os
from dotenv import load_dotenv
from nextcord.ext import commands
import csv

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
        if m.author == ctx.author and m.channel == ctx.channel and len(m.content.strip()) == 5:
            try:
                int(m.content)
                return True
            except:
                return False
        return False
    
    # Build a dictionary to map US zip codes to latitude and longitude
    zip_dict = {}
    with open('us_zip_codes.csv', 'r', newline = '') as f:
        zips = csv.reader(f)
        for row in zips:
            zip_dict[row[0]] = (row[1], row[2])
    
    # Get user's zip code
    await ctx.send("Enter your zip code")
    zip_code = await bot.wait_for("message", check=check_zip)
    zip_code = zip_code.content
    # Convert this to latitude and longitude
    try:
        lat1, lon1 = zip_dict[zip_code]
    except:
       await ctx.send("Run the command again. ZIp doesn't exist.")
    # This formula calculates distance as-the-crow-flies between two positions of a latitude and longitude
    #mi_dist = math.acos(math.sin(math.radians(lat1))*math.sin(math.radians(lat2))+math.cos(math.radians(lat1))*math.cos(math.radians(lat2))*math.cos(math.radians(lon2-lon1)))*6371*0.62137119
    
    await ctx.send(f"Your zip code is {zip_code}, so your latitude is {lat1} and your longitude is {lon1}.")

bot.run(DISCORD_TOKEN)

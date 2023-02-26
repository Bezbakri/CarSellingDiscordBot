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
    def check_mile_radius(m):
        if m.author == ctx.author and m.channel == ctx.channel:
            try:
                rad = float(m.content)
                if rad > 0:
                    return True
                return False
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
    await ctx.send("Enter your zip code:")
    zip_code = await bot.wait_for("message", check=check_zip)
    zip_code = zip_code.content
    # Convert this to latitude and longitude
    try:
        lat1, lon1 = zip_dict[zip_code]
    except:
       await ctx.send("This ZIP code doesn't exist. Try the command again.")
    
    await ctx.send("Enter a mile radius within which to search:")
    mile_radius = await bot.wait_for("message", check=check_mile_radius)
    mile_radius = float(mile_radius.content)
    
    # ADD QUESTION FOR VARIABLE NAMED PRICE_LIMIT HERE
    
    filtered_once = []
    valid_possible_cars = 0
    with open('vehicles.csv', 'r', newline = '') as f:
        cars = csv.reader(f)
        for car in cars:
            # First filter by price...
            price = car[4]
            if price > user_price_limit:
                continue
            
            # ...then by distance.
            lat2 = car[23]
            lon2 = car[24]
            
            # If no geolocation given, skip
            if lat2 == '' or lon2 == '':
                continue
            
            # This formula calculates distance in miles as-the-crow-flies between two positions given lat/long
            dist_from_car = math.acos(math.sin(math.radians(lat1))*math.sin(math.radians(lat2))
                                      +math.cos(math.radians(lat1))*math.cos(math.radians(lat2))
                                      *math.cos(math.radians(lon2-lon1)))*6371*0.62137119
            if mi_dist > mile_radius:
                continue
                
            # Else, car is a valid proposition, note it down
            valid_possible_cars += 1
            filtered_once += car
        
    await ctx.send(f"Your zip code is {zip_code}, so your latitude is {lat1} and your longitude is {lon1}. Valid cars found: {valid_possible_cars}")

bot.run(DISCORD_TOKEN)

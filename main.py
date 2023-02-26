import nextcord as discord
import os
from dotenv import load_dotenv
from nextcord.ext import commands
import csv
import math

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
    
    def check_price(m):
        if m.author == ctx.author and m.channel == ctx.channel:
            try:
                int(m.content)
                return True
            except:
                return False
        return False
    
    def check_bodystyle(m):
        if m.author == ctx.author and m.channel == ctx.channel:
            return m.content.lower() in ["coupe", "convertible", "sedan", "hatchback", "wagon", "pickup", "truck", "SUV", "mini-van", "offroad", "bus", "van"]
        return False
    
    async def end_routine(list_of_cars):
        await ctx.send("The list seems to be narrow enough. We found some cars you might like!")
    
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
        lat1, lon1 = float(lat1), float(lon1)
    except:
       await ctx.send("This ZIP code doesn't exist. Try the command again.")
    
    await ctx.send("Enter a mile radius within which to search:")
    mile_radius = await bot.wait_for("message", check=check_mile_radius)
    mile_radius = float(mile_radius.content)
    
    await ctx.send("What is your price limit?")
    price_limit = await bot.wait_for("message", check=check_price)
    user_price_limit = int(price_limit.content)
    
    filtered_once = []
    valid_possible_cars = 0
    with open('vehicles.csv', 'r', newline = '') as f:
        cars = csv.reader(f)
        for car in cars:
            # First filter by price...
            price = car[4]
            try:
                price = int(price)
            except:
                continue
            
            if price > user_price_limit:
                continue
            
            # ...then by distance.
            lat2 = car[23]
            lon2 = car[24]
            # If no geolocation given, skip
            try:
                lat2 = float(lat2)
                lon2 = float(lon2)
            except:
                continue
            
            # This formula calculates distance in miles as-the-crow-flies between two positions given lat/long
            dist_from_car = math.acos(math.sin(math.radians(lat1))*math.sin(math.radians(lat2))
                                      +math.cos(math.radians(lat1))*math.cos(math.radians(lat2))
                                      *math.cos(math.radians(lon2-lon1)))*6371*0.62137119
            if dist_from_car > mile_radius:
                continue
                
            # Else, car is a valid proposition, note it down
            valid_possible_cars += 1
            filtered_once += car
    
    if len(filtered_once) <= 10:
        end_routine(filtered_once)
    
    await ctx.send(f"Found {valid_possible_cars} in your area.")
    
    # Filter by bodystyle.
    await ctx.send("What bodystyle are you looking for? Options are: coupe, convertible, sedan, hatchback, wagon, pickup, truck, SUV, mini-van, offroad, bus, van.")
    bodystyle = await bot.wait_for("message", check=check_bodystyle)
    user_bodystyle = bodystyle.content.lower()
    
    filtered_by_bodystyle = []
    for car in filtered_once:
        if car[17] == user_bodystyle:
            filtered_by_bodystyle += car
    
    if len(filtered_by_bodystyle) <= 10:
        end_routine(filtered_by_bodystyle)
    
    # more filters?

bot.run(DISCORD_TOKEN)

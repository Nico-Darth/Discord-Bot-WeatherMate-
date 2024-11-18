import discord
import requests
from discord.ext import commands, tasks
from itertools import cycle

# Define bot token and OpenWeather API key
BOT_TOKEN = ""
OPENWEATHER_API_KEY = ""

# Set up the bot
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='/', intents=intents)

# Status messages to cycle through
status_messages = cycle([
    "Providing weather updates!", 
    "Developed by Niels Coert"
])

# Background task to update the bot's status
@tasks.loop(seconds=15)
async def update_status():
    await bot.change_presence(activity=discord.Game(next(status_messages)))

# Function to fetch weather data from OpenWeather
def get_weather(city):
    base_url = "http://api.openweathermap.org/data/2.5/weather?"
    complete_url = f"{base_url}q={city}&appid={OPENWEATHER_API_KEY}&units=metric"
    response = requests.get(complete_url)

    if response.status_code == 200:
        data = response.json()
        main_data = data['main']
        weather_data = data['weather'][0]
        temperature = main_data['temp']
        humidity = main_data['humidity']
        weather_description = weather_data['description']
        icon = weather_data['icon']
        return temperature, humidity, weather_description, icon
    else:
        return None

# Command to fetch weather info when a private message is received
@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    if message.content.startswith('/weather'):
        city = message.content[len('/weather '):].strip()

        if city:
            weather_info = get_weather(city)
            if weather_info:
                temperature, humidity, weather_description, icon = weather_info

                # Create an embedded message
                embed = discord.Embed(title=f"Weather in {city.capitalize()}", color=discord.Color.blue())
                embed.add_field(name="Temperature", value=f"{temperature}°C", inline=False)
                embed.add_field(name="Humidity", value=f"{humidity}%", inline=False)
                embed.add_field(name="Description", value=f"{weather_description.capitalize()} {emoji_for_weather(weather_description)}", inline=False)
                embed.set_thumbnail(url=f"http://openweathermap.org/img/wn/{icon}.png")
                embed.set_footer(
                    text="Data provided by OpenWeather", 
                    icon_url="http://openweathermap.org/themes/openweathermap/assets/img/logo_white_cropped.png"
                )
                await message.author.send(embed=embed)
            else:
                error_embed = discord.Embed(
                    title="Error",
                    description="Sorry, I couldn't retrieve the weather information. Please try again.",
                    color=discord.Color.red()
                )
                await message.author.send(embed=error_embed)
        else:
            error_embed = discord.Embed(
                title="Error",
                description="Please provide a city name. For example, `/weather London`.",
                color=discord.Color.red()
            )
            await message.author.send(embed=error_embed)
    elif message.content.startswith('/'):
        # Send error message for invalid commands
        error_embed = discord.Embed(
            title="Invalid Command",
            description="Sorry, I didn't recognize that command. Type `/info` to learn how to use this bot.",
            color=discord.Color.red()
        )
        await message.channel.send(embed=error_embed)

    await bot.process_commands(message)

# Function to add weather emojis based on the description
def emoji_for_weather(description):
    description = description.lower()
    if "clear" in description:
        return "☀️"
    elif "cloud" in description:
        return "☁️"
    elif "rain" in description:
        return "🌧️"
    elif "snow" in description:
        return "❄️"
    elif "storm" in description:
        return "⛈️"
    elif "fog" in description:
        return "🌫️"
    else:
        return "🌈"  # Default emoji for other weather

# Command to show info message
@bot.command()
async def info(ctx):
    info_embed = discord.Embed(
        title="Bot Information",
        description="Welcome to the Weather Bot! Here's how you can interact with me:",
        color=discord.Color.red()
    )
    info_embed.add_field(
        name="/weather <city>",
        value="Use this command to get the current weather for a specific city.\nFor example: `/weather London`",
        inline=False
    )
    info_embed.add_field(
        name="How the weather is shown:",
        value="The bot will reply with temperature, humidity, and a brief weather description along with an emoji and an icon.",
        inline=False
    )
    info_embed.add_field(
        name="Credits",
        value="This bot was developed by **Niels Coert** and hosted on Discord by **niels__69**. Thanks to OpenWeather for the weather data!",
        inline=False
    )
    info_embed.set_footer(text="Type '/weather <city>' to get started.")

    await ctx.send(embed=info_embed)

# Event to start the background task when the bot is ready
@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")
    update_status.start()  # Start the status update loop

# Run the bot
bot.run(BOT_TOKEN)

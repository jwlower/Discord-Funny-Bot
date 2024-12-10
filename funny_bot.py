# bot.py
import os
import discord
from dotenv import load_dotenv

# Set up intents
intents = discord.Intents.default()
intents.message_content = True  # Enable reading message content

# Load environment variables
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

# Create the client with the specified intents
client = discord.Client(intents=intents)

# List of greetings to look for
greetings = ["hello", "hi", "hey", "greetings", "sup"]

@client.event
async def on_ready():
    print(f'{client.user} has connected to Discord!')

@client.event
async def on_message(message):
    # Ignore messages from the bot itself
    if message.author == client.user:
        return

    # Check if the message contains a greeting
    if any(greet in message.content.lower() for greet in greetings) and ("!funnybot" in message.content.lower()):
        print("working")
        await message.channel.send("GREETING_LIST")

# Run the bot
client.run(TOKEN)

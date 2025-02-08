# bot.py
import os
import discord
import json
import random
from dotenv import load_dotenv
import re

# Set up intents
intents = discord.Intents.default()
intents.message_content = True  # Enable reading message content

# Load environment variables
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN_INSPIRATION_BOT')

# Create the client with the specified intents
client = discord.Client(intents=intents)

# List of bot activation phrases
bot_call = ["!starwarsname", "!swname", "!starwars_name"]

# Load Star Wars names JSON
try:
    with open("starwars_names.json", "r") as file:
        starwars_names = json.load(file)
except FileNotFoundError:
    starwars_names = {}

def generate_starwars_name(category="jedi"):
    """Generate a random Star Wars name from a given category."""
    if category not in starwars_names:
        return "Unknown category. Try: Jedi, Sith, Scoundrel, Alien, Droid."

    standard = starwars_names[category].get("standard", [])
    extension = starwars_names[category].get("extension", [])

    if not standard or not extension:
        return "Not enough name components available."

    return random.choice(standard) + random.choice(extension)

@client.event
async def on_ready():
    print(f'{client.user} has connected to Discord!')

@client.event
async def on_message(message):
    # Ignore messages from the bot itself
    if message.author == client.user:
        return

    content_lower = message.content.lower()

    # Check if the message contains a bot call
    if any(call in content_lower for call in bot_call):
        # Extract category if provided (e.g., "!starwarsname sith")
        parts = message.content.split()
        category = parts[1].lower() if len(parts) > 1 else "jedi"

        starwars_name = generate_starwars_name(category)
        await message.channel.send(f"Your {category.capitalize()} name: {starwars_name}")

# Run the bot
client.run(TOKEN)

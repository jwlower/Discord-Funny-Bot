# bot.py
import os
import discord
from dotenv import load_dotenv
import re
import random

# Set up intents
intents = discord.Intents.default()
intents.message_content = True  # Enable reading message content

# Load environment variables
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN_INSPIRATION_BOT')

# Create the client with the specified intents
client = discord.Client(intents=intents)

# List of greetings to look for
bot_call = ["!inspirationbot", "!inspiration_bot", "!insp", "!inspiration", "!inspbot", "!inspb"]

additions = []

@client.event
async def on_ready():
    print(f'{client.user} has connected to Discord!')

@client.event
async def on_message(message):
    # Ignore messages from the bot itself
    if message.author == client.user:
        return

    # Read random addition from the file
    try:
        with open("inspirations.txt", "r") as file:
            additions = file.readlines()
            
        # Pick a random addition
        if additions:
            addition = random.choice(additions).strip()
        else:
            addition = "inspired beyond words."  # Default if the file is empty
    except FileNotFoundError:
        addition = "inspired beyond words."  # Default if the file doesn't exist
    
    if "getinsp" in message.content.lower():
        guild = message.guild
        
        # Get all channel names and filter those containing "inspiration" (case-insensitive)
        matching_channels = [
            channel for channel in guild.channels
            if re.search(r'\binspiration\b', re.sub(r'[^a-zA-Z0-9\s]', '', channel.name), re.IGNORECASE)
        ]

        post_channel = matching_channels[0]
        
        if matching_channels:
            channel_names = ", ".join([channel.name for channel in matching_channels])
            await message.channel.send(f"Found channels containing 'inspiration': {channel_names}")
        else:
            await message.channel.send("No channels containing 'inspiration' were found.")

    # Check if the message contains a greeting
    if any(greet in message.content.lower() for greet in bot_call):
        if message.reference:
            # Fetch the replied-to message
            replied_message = await message.channel.fetch_message(message.reference.message_id)
            # Check if the replied message's author is the bot
            if replied_message.author != client.user:
                guild = message.guild
        
                # Get all channel names and filter those containing "inspiration" (case-insensitive)
                matching_channels = [
                    channel for channel in guild.channels
                    if re.search(r'\binspiration-bot\b', re.sub(r'[^a-zA-Z0-9\s]', '', channel.name), re.IGNORECASE)
                ]
                replied_content = replied_message.content
                if len(matching_channels) > 0:
                    # Pick first channel
                    post_channel = matching_channels[0]
                    await post_channel.send(f'"{replied_content}"\n\n-- {replied_message.author.name} {addition}')
                else:
                    
                    await message.channel.send(f'"{replied_content}"\n\n-- {replied_message.author.name} {addition}')
        
        
        else:
            await message.channel.send("You have called Inspiration Bot.")

    

# Run the bot
client.run(TOKEN)

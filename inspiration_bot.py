# bot.py
import os
import discord
from dotenv import load_dotenv

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

@client.event
async def on_ready():
    print(f'{client.user} has connected to Discord!')

@client.event
async def on_message(message):
    # Ignore messages from the bot itself
    if message.author == client.user:
        return

    # Check if the message contains a greeting
    if any(greet in message.content.lower() for greet in bot_call):
        if message.reference:
            # Fetch the replied-to message
            replied_message = await message.channel.fetch_message(message.reference.message_id)
            # Check if the replied message's author is the bot
            if replied_message.author != client.user:
                replied_content = replied_message.content
                await message.channel.send(f"You have called Inspiration Bot with a reply to this message\n\n{replied_content}")
        else:
            await message.channel.send("You have called Inspiration Bot.")

    

# Run the bot
client.run(TOKEN)

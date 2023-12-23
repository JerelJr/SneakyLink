# TODO: replace Client with Bot
import discord
from discord.ext import commands
from dotenv import load_dotenv
import os
import re

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

intents = discord.Intents(messages=True, message_content=True)
bot = commands.Bot('', intents=intents)
ALT_URL = "https://piped.video/watch?v="


@bot.event
async def on_ready():
    print(f'{bot.user} has connected to Discord.')


@bot.event
async def on_message(msg: discord.Message):
    if msg.author == bot.user:
        return
    yt_link_re = r'(?:https?:\/\/)?(?:www\.)?(?:youtube\.com\/(?:watch\?v=|embed\/|shorts\/)|youtu\.be\/)([\w-]{11})'
    matches = re.findall(yt_link_re, msg.content)
    if matches:
        msg_content = [f"@{msg.author} Here's an alternative to your YouTube link(s) that protect your privacy:\n"]
        for match in matches:
            msg_content.append(ALT_URL+match)

        send_msg = "\n"
        send_msg = send_msg.join(msg_content)
        await msg.channel.send(f"{send_msg}")


@bot.event
async def on_error(event, *args, **kwargs):
    with open('bot.log', 'a') as f:
        if event == 'on_message':
            f.write(f'[ERROR] Unhandled message: {args[0]}\n')
        else:
            raise

if TOKEN is not None:
    bot.run(str(TOKEN))

from time import time, ctime
from typing import List
import discord
from discord.ext import commands
import re


class SneakyLinkBot(discord.ext.commands.Bot):
    def __init__(self):
        intents = discord.Intents(messages=True, message_content=True)
        super().__init__('', intents=intents)
        self._REDD_ALT = "https://teddit.zaggy.nl/"
        self._TWITT_ALT = "https://nitter.net/"
        self._YT_ALT = "https://piped.video/watch?v="

        self._redd_link_re = r'(?:https?:\/\/)?(?:www\.)?(?:reddit)\.com\/([\w\/-]*)'
        self._twit_link_re = r'(?:https?:\/\/)?(?:www\.)?(?:twitter|x)\.com/([\w/-]*)'
        self._yt_link_re = (r'(?:https?:\/\/)?(?:www\.)?(?:youtube\.com\/(?:watch\?v=|embed\/|shorts\/)|youtu\.be\/)'
                            r'([\w-]{11})')

        self._alts = {
            "reddit": (self._redd_link_re, self._REDD_ALT),
            "twitter": (self._twit_link_re, self._TWITT_ALT),
            "youtube": (self._yt_link_re, self._YT_ALT)
        }

    async def on_ready(self):
        t = time()
        cur_time = ctime(t)
        with open('bot.log', 'a') as f:
            f.write(f'{cur_time} {self.user} has connected to Discord.')

    async def on_message(self, msg: discord.Message):
        if msg.author == self.user:
            return

        msg_content = []
        for domain in ["reddit", "twitter", "youtube"]:
            links: [] = self.match_links(domain, msg.content)
            if links:
                msg_content += [f"{domain.title()}:"]
                msg_content += links

        if msg_content:
            msg_content.insert(0,
                               f"<@{msg.author.id}> Here's an alternative to your link(s) that protect your privacy:\n")
            send_msg = "\n"
            send_msg = send_msg.join(msg_content)
            await msg.channel.send(f"{send_msg}")

    async def on_error(self, event, *args, **kwargs):
        with open('bot.log', 'a') as f:
            t = time()
            cur_time = ctime(t)
            if event == 'on_message':
                f.write(f'{cur_time} [ERROR] Unhandled message: {args[0]}\n')
            else:
                raise

    def match_links(self, domain: str, content: str) -> List[str]:
        (rgx, alt) = self._alts[domain]
        links = []

        matches = re.findall(rgx, content)

        for match in matches:
            links.append(alt + match)

        return links

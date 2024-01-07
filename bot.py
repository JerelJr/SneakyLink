from dotenv import load_dotenv
import os

import SneakyLink

if __name__ == "__main__":
    load_dotenv()
    TOKEN = os.getenv('DISCORD_TOKEN')

    bot = SneakyLink.SneakyLinkBot()

    if TOKEN is not None:
        bot.run(str(TOKEN))

from instabot import Bot
import time

# Create a Bot instance
bot = Bot()

# Login to your Instagram account
bot.login(username="megasameru", password="panchos")

bot.upload_photo("image.jpg", caption="My caption")

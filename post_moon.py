from moon_bot import MoonBot#, TESS_CONFIG
import cv2

bot = MoonBot()
bot.get_moon()

bot.make_ascii_tweet(9, 1)
print(bot.ascii)
bot.twitter_signin()
bot.set_moon_info_caption()
bot.post_moon_tweet()

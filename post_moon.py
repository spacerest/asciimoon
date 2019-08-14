from moon_bot import MoonBot#, TESS_CONFIG
import cv2

bot = MoonBot()
bot.get_moon()

bot.make_ascii_tweet(10, 1)
print(bot.ascii)
bot.twitter_signin()
bot.set_moon_info_caption()
bot.post_moon_tweet()
bot.update_profile_image()


#401408         km from earth
#96.72%               illuminated

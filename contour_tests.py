from moon_bot import MoonBot, TESS_CONFIG
import cv2
import pytesseract
from pytesseract import Output


bot = MoonBot()
bot.get_test_moon()


bot.draw_contours()
cv2.imwrite("contourmoon.jpg", bot.moon.image)
bot.get_image_tiles(bot.moon.image, 5) 
bot.map_tiles_to_chars(bot.tiles)







#bot.get_moon()
#bot.get_random_image(url=URL)
#cv2.imwrite("moon.png", bot.moon.image)

#bot.get_text()
#print(bot.text)


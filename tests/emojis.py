import unittest, os, datetime, cv2
from moon_bot import MoonBot
import numpy as np
import matplotlib.pyplot as plt


class TestAsciiMoon(unittest.TestCase):
	def test_can_make_accurate_gradient(self):
		bot = MoonBot(cache_dir="cached_moons/")

		#make a gradient image to test with
		x = np.ones((10, 10, 3))
		x[:, :, 0:3] = np.random.uniform(255, 255, (3,))
		y = np.ones((10, 10, 3))
		y[:,:,0:3] = np.random.uniform(0, 0, (3,))
		c = np.linspace(0, 1, 10)[:, None, None]
		gradient = x + (y - x) * c

		#make a moon but replace it with the gradient
		bot.get_moon(date="2020-02-20")
		bot.moon.image = gradient
		bot.set_modes(gradient_symbols="numbers")
		bot.make_ascii_tweet()
		assert bot.ascii_list[0] == "99" and bot.ascii_list[-1] == "00"# and int(bot.ascii_list[4][0]) + (bot.ascii_list[5][0]) == 100 

	def test_can_make_accurate_gradient_with_emoji_settings(self):
		bot = MoonBot(cache_dir="cached_moons/")

		#make a gradient image to test with
		x = np.ones((10, 10, 3))
		x[:, :, 0:3] = np.random.uniform(255, 255, (3,))
		y = np.ones((10, 10, 3))
		y[:,:,0:3] = np.random.uniform(0, 0, (3,))
		c = np.linspace(0, 1, 10)[:, None, None]
		gradient = x + (y - x) * c

		#make a moon but replace it with the gradient
		bot.get_moon(date="2020-02-20")
		bot.moon.image = gradient
		bot.set_modes(gradient_symbols="numbers-emojis")
		bot.make_ascii_tweet()
		assert bot.ascii_list[0] == " ⓽ " and bot.ascii_list[-1] == " ⓪ "# and int(bot.ascii_list[4][0]) + (bot.ascii_list[5][0]) == 100 

	def test_can_get_average_luminosity_of_white_image(self):
		#TODO do more testing on luminosity stuff, all it does now is make histogram
		bot = MoonBot(cache_dir="cached_moons/")

		img = np.full((500, 500, 3), 255, dtype = np.uint8) 

		#make a moon but replace it with the white img

		bot.get_moon(date="2020-02-20")
		bot.moon.image = img
		bot.make_histogram()
		bot.calculate_luminosity()

		assert bot.average_luminosity == 1

	# def test_can_get_average_luminosity_of_black_image(self):
	# 	bot = MoonBot(cache_dir="cached_moons/")

	# 	img = np.full((500, 500, 3), 0, dtype = np.uint8) 

	# 	#make a moon but replace it with the white img

	# 	bot.get_moon(date="2020-02-20")
	# 	bot.moon.image = img
	# 	bot.make_histogram()
	# 	print(bot.hist)
	# 	bot.calculate_luminosity()

	# 	assert bot.average_luminosity == 0

	def test_finds_least_frequent_luminosity_values(self):
		bot = MoonBot(cache_dir="cached_moons/")
		bot.get_moon(date="2020-02-20")
		bot.set_modes(gradient_symbols="inverted_moons", astrology=True)
		bot.make_ascii_tweet()
		print(bot.least_often_gradient_value1)
		print(bot.least_often_gradient_value2)
		assert bot.least_often_gradient_value1




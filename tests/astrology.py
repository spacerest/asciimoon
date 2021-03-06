import unittest, os, datetime, cv2
from moon_bot import MoonBot
import numpy as np
import matplotlib.pyplot as plt


class TestAsciiMoon(unittest.TestCase):
	def test_can_get_current_moon_sign(self):
		bot = MoonBot(cache_dir="cached_moons/")
		bot.get_moon(date="2020-02-02")
		bot.set_astrology_info()
		assert bot.moon_sign == "Taurus"

	def test_can_import_astrology_settings(self):
		bot = MoonBot(cache_dir="cached_moons/")
		bot.set_modes("moons2",astrology=True)
		bot.get_moon(date="2020-02-02")
		bot.make_ascii_tweet()
		assert bot.astrology_ascii_dict["element"] == "earth"

	def test_can_get_moon_aspects(self):
		bot = MoonBot(cache_dir="cached_moons/")
		bot.set_modes("moons2",astrology=True)
		bot.get_moon(date="2020-02-02")
		bot.make_ascii_tweet()
		print(bot.aspects)
		assert bot.aspects == []
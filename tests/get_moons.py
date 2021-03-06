import unittest, os, datetime
from moon_bot import MoonBot

class TestAsciiMoon(unittest.TestCase):
    def test_can_toggle_cache_moon_images(self):
    	m = MoonBot(cache_dir="cached_moons/")
    	assert m.cache_dir	

    def test_errors_if_no_cached_img_dir(self):
    	m = MoonBot(cache_dir="doesnt_exist/")
    	self.assertRaises(OSError, m.get_moon)

    def test_saves_moon_image_if_cache_toggled_on(self):
    	m = MoonBot(cache_dir="cached_moons/")
    	cached_img_fn = "cached_moons/2020-2-2-0.jpg"
    	# delete the file if it already exists
    	if os.path.isfile(cached_img_fn):
    		os.remove(cached_img_fn)
    	file_exists_before_check = os.path.isfile(cached_img_fn)
    	m.get_moon(date="2020-02-02")
    	assert not file_exists_before_check and os.path.isfile(cached_img_fn)

    def test_uses_cached_moon_image_if_cache_toggled_on(self):
    	m = MoonBot(cache_dir="cached_moons/")
    	cached_img_fn = "cached_moons/2020-2-2-0.jpg"
    	m.get_moon(date="2020-02-02")
    	time_before_second_load = datetime.datetime.now()
    	m.get_moon(date="2020-02-02")
    	time_after_second_load = datetime.datetime.now()
    	assert time_before_second_load - time_after_second_load \
    	< datetime.timedelta(milliseconds=50)

    def test_gets_moon_datetime_info_json_if_cache_toggled_on(self):
    	m = MoonBot(cache_dir="cached_moons/")
    	m.get_moon(date="2020-02-02")
    	m.set_moon_info_caption()
    	assert m.moon.moon_datetime_info is not None

    def test_saves_json_if_cache_toggled_on(self):
    	m = MoonBot(cache_dir="cached_moons/")
    	m.get_moon(date="2020-02-02")
    	json_file_exists = os.path.isfile("cached_moons/mooninfo_2020.json")
    	
    	assert json_file_exists

    def test_errors_if_json_file_empty(self):
    	m = MoonBot(cache_dir="cached_moons/")
    	with open("cached_moons/mooninfo_2021.json", 'w') as f:
    		f.write("")
    	self.assertRaises(ValueError, m.get_moon, date="2021-02-02")


if __name__ == '__main__':
    unittest.main()
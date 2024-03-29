from __keys import *
from random import randint, choice
from collections import Counter
from moon.dialamoon import Moon as MoonImage, CustomImage
import numpy as np
import cv2, mimetypes, random, os, json, tweepy, requests
from mastodon import Mastodon
from res import settings_dict
from res.astrology_dict import astrology_dict
from collections import Counter
from utilities import stretch
from flatlib.datetime import Datetime
from flatlib.protocols import behavior
from flatlib.geopos import GeoPos
from flatlib.chart import Chart
from flatlib import const
from flatlib.tools.chartdynamics import ChartDynamics
import matplotlib.pyplot as plt
from PIL import Image, ImageDraw,ImageFont, ImageFilter
import pdb

DIMS = (400, 400)
JSON_FN = "mooninfo_{year}.json"

class MoonBot():
	def __init__(self, cache_dir=None):
		#self.maxchar = 280 #twitter maxchar
		self.light_gradient = [str(x).zfill(2) for x in range(100)]
		self.cache_dir = cache_dir
		self.astrology = False

	def set_modes(self, gradient_symbols="moon2", astrology=False):
		self.gradient_symbols = gradient_symbols
		self.settings = settings_dict.settings[gradient_symbols]
		self.astrology = astrology
		self.charwidth = self.settings["ascii_dims"][0]
		self.charheight = self.settings["ascii_dims"][1]
		self.ascii_gradient = ['']*(self.charwidth * self.charheight)

	def decide_new_moon_border(self):
		#if True:#self.luminosity <= .1 and self.settings["settings_type"] == "random":
		if self.moon.moon_datetime_info["age"] < 3.0 or self.moon.moon_datetime_info["age"] > 25.0:
			self.add_border = True
			surrounding_pixels_offsets = {
						"char_to_left": -1, 
						"char_to_right": 1, 
						"char_above": -1 * self.charwidth,
						"char_below": self.charwidth,
						"char_up_right": (-1 * self.charwidth) + 1,
						"char_up_left": (-1 * self.charwidth) - 1,
						"char_down_right": self.charwidth + 1,
						"char_down_left": self.charwidth - 1
						}
			#make a shadow border
			for idx, value in enumerate(self.result_moon_gradients):
				#check whether there's a border character adjacent to this one
				border_char_adjacent = -1 in [self.result_moon_gradients[idx + offset] for offset in surrounding_pixels_offsets.values() if idx + offset >= 0 and idx + offset <= (self.charwidth * self.charheight) - 1]
				if border_char_adjacent:
					continue
				for desc, offset in surrounding_pixels_offsets.items():
					if idx + offset >= 0 and idx + offset <= (self.charwidth * self.charheight) - 1:#ignore negative offsets as they're at the end of the array and not nearby
						try:
							if int(self.result_moon_gradients[idx + offset]) == 0 and int(self.result_moon_gradients[idx]) > 0:

								self.result_moon_gradients[idx + offset] = -1

						except ValueError:
							pass
						except IndexError:
							pass
			#print(self.result_moon_gradients)

	def choose_random_shadow_symbol(self):
		return random.choice(self.settings["symbols"]["random_shadow_symbols"])
	
	def choose_random_light_symbol(self):
		return random.choice(self.settings["symbols"]["random_light_symbols"])
		
	def make_ascii_tweet(self):
		#pdb.set_trace()
		self.convert_image_to_ascii(self.charwidth, 1)
		#self.decide_new_moon_border()
		if self.astrology:
			self.set_astrology_info()
		self.set_symbols_list(self.luminosity)
		self.put_symbols_in_gradient()
		self.put_output_in_square()
		self.make_img_to_post()

	def put_symbols_in_gradient(self):
		self.ascii_list = []
		if self.astrology:
			#find which luminances have just one or two
			self.least_often_gradient_value1 = Counter(self.result_moon_gradients).most_common()[-1][0]
			self.least_often_gradient_value2 = Counter(self.result_moon_gradients).most_common()[-2][0]
		for value in self.result_moon_gradients:
			if value == self.least_often_gradient_value1:
				self.ascii_list.append(self.astrology_sign_random_emoji)
			elif value == self.least_often_gradient_value2:
				self.ascii_list.append(self.astrology_element_random_emoji)
			elif value == -2:
				self.border_char = "💡" #$todo
				self.ascii_list.append(self.border_char)
			elif value == -1:
				self.border_char = "🌚" #$todo
				self.ascii_list.append(self.border_char)
			else:
				self.ascii_list.append(self.ascii_gradient[int(value)])
	
	def make_img_to_post(self):
		#In-stream images are displayed at a 16:9 ratio of 600px by 335px 
		# and can be clicked and expanded up to 1200px by 675px.
		font_size = 80
		width = DIMS[0]
		height = DIMS[1]
		twitter_im_width = 800
		twitter_im_height = 450
		bg_color = (0, 0, 0)
		font_size=int(width/self.charwidth)
		unicode_text = self.ascii
		im = Image.open("moon.jpg")
		moon_waning = self.moon.moon_datetime_info["age"] > 14

		#im =  Image.new ( "RGB", (width,height), bg_color )

		unicode_font = ImageFont.truetype("res/unicode-emoji/symbola/Symbola.ttf", font_size)
		draw  =  ImageDraw.Draw ( im )
		for x in range(0, self.charwidth):
			for y in range(0, self.charheight):

				lum = int(255 - 255/(int(self.result_moon_gradients[(x * self.charwidth) + y]) + 1))
				if type(lum) == type(1.0):
					raise ValueError("float ", lum)
				if self.astrology == True:
					if self.moon_sign in ["Sagittarius", "Leo", "Aries"]:
						#red, yellow
						r = 255
						g = lum
						b = int(255 - (255 / (lum + 1) * (moon_waning * x * self.charwidth + y + 1)))
					elif self.moon_sign in ["Taurus", "Capricorn", "Virgo"]:
						#green, blue
						r = lum
						g = 255
						b = int(255 - (255 / (lum + 1) * (moon_waning * x * self.charwidth + y + 1)))
					elif self.moon_sign in ["Gemini", "Libra", "Aquarius"]:
						#blue, purple
						r = lum
						g = int(255 - (255 / (lum + 1) * (moon_waning * x * self.charwidth + y + 1)))
						b = 255
					elif self.moon_sign in ["Pisces", "Cancer", "Scorpio"]:
						#blue, green
						r = 255
						g = int(255 - (255 / (lum + 1) * (moon_waning * x * self.charwidth + y + 1)))
						b = lum
				else:
					#todo make an rgb that looks good
					r, g, b = (lum, lum, lum)

				if r > 255 or g > 255 or b > 255:
					raise ValueError(f"One of your RGB colors is higher than 255, your lum is: {lum}")
				font_color=(r, g, b)

				draw.text ( (x * int(width/self.charwidth) ,y * int(width/self.charheight)), self.ascii_list[(x * self.charwidth) + y], font=unicode_font, fill=font_color )

		#draw.text ( (0,0), self.moon_sign, font=unicode_font, fill=(255,255,0) )
				#self.ascii += str(self.ascii_list[(y * self.charwidth) + x])
		#im  =  Image.new ( "RGB", (width,height), bg_color )
		background_im =  Image.new ( "RGB", (twitter_im_width,twitter_im_height), bg_color )
		draw = ImageDraw.Draw(background_im)
		offset = ((twitter_im_width - width) // 2, (twitter_im_height - height) // 2)
		background_im.paste(im, offset)
		background_im.show()
		background_im.save("moon_emojis.png") #.jpg makes problems

	def calculate_luminosity(self):
		self.average_luminosity = 1

	def make_histogram(self):
		self.hist = plt.hist(self.moon.image.ravel(),256,[0,256])

	def put_output_in_square(self):
		self.ascii = ""
		for x in range(0, self.charwidth):
			for y in range(0, self.charheight):
				self.ascii += str(self.ascii_list[(y * self.charwidth) + x])
			self.ascii += "\n"

	def twitter_signin(self):
		auth = tweepy.OAuthHandler(TWITTER_CONSUMER_KEY, TWITTER_CONSUMER_SECRET)
		auth.set_access_token(TWITTER_ACCESS_TOKEN, TWITTER_ACCESS_TOKEN_SECRET)
		auth.set_access_token(TWITTER_ACCESS_TOKEN, TWITTER_ACCESS_TOKEN_SECRET)
		self.twitter_api = tweepy.API(auth, parser=tweepy.parsers.JSONParser())

	def mast_signin(self):
		self.mast_api = Mastodon(client_id=MAST_CLIENT_KEY, 
			client_secret=MAST_CLIENT_SECRET, 
			api_base_url='https://botsin.space', 
			access_token=MAST_ACCESS_TOKEN)

	def post_moon_toot(self):
		FPATH = ""
		data = {}
		try:
			image = FPATH + "moon_emojis.png"
			media = self.mast_api.media_post(image, description=self.alt_text)
			status = self.mast_api.status_post(self.moon_info_caption,media_ids=media,sensitive=False)
		except Exception as e:
			raise e
		
	#TODO use python mastodon api port or figure out why this isn't working
	def mast_update_profile_image(self):
		# with open('moon.jpg', 'rb') as f:
		#     image = f.read()

		account = self.mast_api.account_update_credentials(
		    avatar = "moon.jpg")

	def get_moon(self, **kwargs):
		try:
			self.moon = MoonImage()
			if not self.cache_dir:
				self.moon.set_moon_phase(**kwargs)
			else: #check if this moon time exists in cached img dir
				if not os.path.isdir(self.cache_dir):
					raise OSError((f"Can't find a directory called "
						"'{self.cache_dir}'. Please double "
						"check that you've created this directory."))
				self.moon.set_moon_datetime(**kwargs)
				date_filename = (f'{self.cache_dir}'
								f'{self.moon.datetime.year}-'
								f'{self.moon.datetime.month}-'
								f'{self.moon.datetime.day}-'
								f'{self.moon.datetime.hour}')
				
				if os.path.isfile(date_filename + '.jpg'):
					# TODO would be nice if `dialamoon.Moon` would do this in Moon.set_moon_phase()
					self.moon.image = cv2.imread(date_filename + '.jpg')
					self.moon.resize_image()
					self.set_up_cached_json()

				else:
					self.moon.set_moon_phase(**kwargs)
					self.moon.save_to_disk(date_filename)

			#self.moon.image = cv2.resize(self.moon.image, DIMS)
			self.moon.image = cv2.resize(self.moon.image, DIMS)

			#self.moon.image = cv2.resize(self.moon.image, (200,200))
			cv2.imwrite("moon.jpg", self.moon.image)
		except Exception as e:
			raise e

	def set_symbols_list(self, luminosity):		
		#TODO clean up so it isn't so rickety
		try:
			if self.settings["settings_type"] == "map":
				if self.moon.moon_datetime_info["age"] < 14:
						intervals = self.settings["intervals"]["young_moon"]
				else:
						intervals = self.settings["intervals"]["old_moon"]
				i = 0
				for n in sorted(intervals.keys()):
					rep = n - i
					self.ascii_gradient[i:n+1] = [intervals[n]] * rep
					i = n
			else:
				if self.moon.moon_datetime_info["age"] < 14:
	 
					self.ascii_gradient = stretch(self.settings["symbols"]["young_moon"], self.charwidth * self.charheight)
				else:
					self.ascii_gradient = stretch(self.settings["symbols"]["old_moon"], self.charwidth * self.charheight)

				if self.settings["settings_type"] == "random":
					self.ascii_gradient = self.set_random_chars()
		except TypeError as e:
			raise TypeError(f'Something might be wrong with your settings_dict {self.gradient_symbols} mode\n' + str(e))

	def set_astrology_info(self):
		d = Datetime(f'{self.moon.datetime.year}/{self.moon.datetime.month}/{self.moon.datetime.day}', f'{self.moon.datetime.hour}:00', '+00:00')
		pos = GeoPos('38n32', '8w54') #todo use a different location? this was in the docs
		self.chart = Chart(d, pos)
		self.moon_astrology_info = self.chart.get(const.MOON)
		self.moon_sign = self.moon_astrology_info.sign
		self.astrology_ascii_dict = astrology_dict["signs"][self.moon_sign]
		self.astrology_sign_random_emoji = choice(astrology_dict["signs"][self.moon_sign]["related"])
		self.astrology_element_random_emoji = choice(astrology_dict["elements"][self.astrology_ascii_dict["element"]])

		# get aspects of chart
		dyn = ChartDynamics(self.chart)
		self.aspects = dyn.validAspects(const.MOON, const.MAJOR_ASPECTS)

	def set_up_cached_json(self):
		#TODO do this in dialamoon.Moon some day
		json_path = self.cache_dir + JSON_FN.format(year=self.moon.datetime.year)
		if not os.path.isfile(json_path):
			self.moon.make_json_year_data_url()
			self.moon.set_json_year_data()
			with open(json_path, 'w') as outfile:
				json.dump(self.moon.moon_year_info, outfile)
		else: 
			with open(json_path, 'r') as outfile:
				s = outfile.read()
				if s == "":
					raise ValueError(f"The {json_path} file is empty. Please try again.")
				self.moon.moon_year_info = json.loads(s)
		self.moon.set_json_specific_data()
	
	def set_moon_info_caption(self):
		self.moon_info_caption = "...\n\n" + str(self.moon.moon_datetime_info["distance"]) + "km from earth".rjust(22, " ") + "\n" + str(self.moon.moon_datetime_info["phase"]) + "%" + "illuminated".rjust(26, " ") + "\n\n"

	def set_alt_text(self):
		self.alt_text = f"Image of the moon, {self.moon.moon_datetime_info['phase']}% illuminated, with emojis overlaid"

	def post_moon_tweet(self):
		media = self.twitter_api.media_upload("moon_emojis.png")

		#if .create_media_metadata makes a problem, it may be because tweepy.parser.JSONParser 
		#is receiving '' as payload (from resp.text) and json.loads() errors
		r = self.twitter_api.create_media_metadata(
			media_id=media["media_id_string"], 
			alt_text=self.alt_text)

		self.twitter_api.update_status(self.moon_info_caption, media_ids=[media["media_id_string"]])

	def update_profile_image(self):
		self.twitter_api.update_profile_image("./moon.jpg")

	# START pixelating grayscale image with characters/emojis
	### PYTHON TO ASCII ART - https://github.com/electronut/pp/blob/master/ascii/ascii.py#L2 modified to just take numpy images

	def convert_image_to_ascii(self, cols, scale):
		"""
		Given Image and dims (rows, cols) returns an m*n list of Images 
		"""
		# declare globals
		# open image and convert to grayscale
		im = self.rgb_to_gray(self.moon.image)
		# store dimensions
		W, H = im.shape[0], im.shape[1]
		# compute width of tile
		w = W/cols
		# compute tile height based on aspect ratio and scale
		h = w/scale
		# compute number of rows
		rows = int(H/h)

		#why not get the average luminosity of the whole image first
		self.luminosity = self.getAverageL(im) / 100
		
		# check if image size is too small
		if cols > W or rows > H:
			raise Exception("Image too small for specified cols!")
			exit(0)
	
		# ascii image is a list of character lists 
		aimg = []
		# generate list of dimensions
		for j in range(rows):
			y1 = int(j*h)
			y2 = int((j+1)*h)
			# correct last tile
			if j == rows-1:
				y2 = H
			# append an empty string
			aimg.append([])
			for i in range(cols):
				# crop image to tile
				x1 = int(i*w)
				x2 = int((i+1)*w)
				# correct last tile
				if i == cols-1:
					x2 = W
				# crop image to extract tile
				img = im[x1:x2, y1:y2]
				# get average luminosity
				avg = int(self.getAverageL(img))
				# look up value in light gradient
				gsval = self.light_gradient[int((avg*99)/255)]
				# append ascii char to string
				aimg[j].append(gsval)
		#transpose it as its currently rotated -90 deg
		#aimg = list(map(list, np.transpose(aimg)))

		# return light_gradients
		self.result_moon_gradients = [item for sublist in aimg for item in sublist]

	def rgb_to_gray(self, img):
		#make an array of zeros with the shape (1000, 1000, 3)
		# (1000 px by 1000 px each with 3 values - RGB)
		grayImage = np.zeros(img.shape)
		
		#take just the red, green and blue values from the 1000x1000 
		R = np.array(img[:, :, 0])
		G = np.array(img[:, :, 1])
		B = np.array(img[:, :, 2])

		# ITU-R 601-2 luma transform coefficients for converting rgb > greyscale
		R = (R *.299)
		G = (G *.587)
		B = (B *.114)

		Avg = (R+G+B)
		grayImage = img

		for i in range(3):
		   grayImage[:,:,i] = Avg
		return grayImage       

	def getAverageL(self, im):
		"""
		Given PIL Image, return average value of grayscale value
		"""
		# get shape
		w = im.shape[0]
		h = im.shape[1]
		# get average
		#cv2.imshow("test", im)
		#cv2.waitKey(0)
		#cv2.destroyAllWindows()
		return np.average(im)

#END pixelating grayscale image with characters/emojis#


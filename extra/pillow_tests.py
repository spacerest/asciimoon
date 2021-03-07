# A script to make an image with Symbola symbols in res/astrology_dict.
# Run this from asciimoon directory and take a look at the image to see if there's any
# symbols not printing how you would like

from PIL import Image, ImageDraw,ImageFont, ImageFilter
import astrology_dict_copy

font_size=36
width=1000
height=2000
back_ground_color=(255,255,255)
font_size=50
font_color=(0,0,0)

emojis_dict = astrology_dict_copy.astrology_dict

count = 0
line_length = 15
unicode_text = ""

for k in emojis_dict["signs"]:
	unicode_text += (k + ": ")
	for c in emojis_dict["signs"][k]["related"]:
		unicode_text += c
		count += 1
		if count == line_length:
			unicode_text += "\n"
			count = 0
	unicode_text += "\n\n"
	count = 0

for k in emojis_dict["elements"]:
	unicode_text += (k + ": ")
	for c in emojis_dict["elements"][k]:
		unicode_text += c
		count += 1
		if count == line_length:
			unicode_text += "\n"
			count = 0
	unicode_text += "\n\n"
	count = 0

im  =  Image.new ( "RGB", (width,height), back_ground_color )
draw  =  ImageDraw.Draw ( im )
unicode_font = ImageFont.truetype("res/unicode-emoji/Symbola.ttf", font_size)
draw.text ( (10,10), unicode_text, font=unicode_font, fill=font_color )
im.save("extra/sample_symbola.png")




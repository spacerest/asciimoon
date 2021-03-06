from PIL import Image, ImageDraw,ImageFont, ImageFilter

font_size=36
width=500
height=100
back_ground_color=(255,255,255)
font_size=36
font_color=(0,0,0)
unicode_text =u"\U0001f300"#"🌒🌔🌙"#u"\U0001f300"

im  =  Image.new ( "RGB", (width,height), back_ground_color )
draw  =  ImageDraw.Draw ( im )
unicode_font = ImageFont.truetype("Symbola.ttf", font_size)
draw.text ( (10,10), unicode_text, font=unicode_font, fill=font_color )
im.show()
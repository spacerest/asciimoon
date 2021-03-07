# asciibot

This is a script for a bot that posts an image of an emoji representation & some stats about today's moon phase to [twitter](https://twitter.com/the_moon_is) and [mastodon](https://botsin.space/@moon).

To see some nasa data on the current moon phase, please look at Ernie Wright's moon visualizations over at https://svs.gsfc.nasa.gov/

## updates:
- March 7, 2021 
  - Instead of posting strings of emojis, now posting images of emojis printed in Symbola font on an image of the moon
  - Added alt text for mastodon
  - Determine the random emojis and font color based on the lunar zodiac per `flatlib`


## sources:

- https://docs.opencv.org/3.3.1/d4/d73/tutorial_py_contours_begin.html
- https://pypi.org/project/pytesseract/
- https://github.com/flatangle/flatlib/
- https://github.com/spacerest/moon


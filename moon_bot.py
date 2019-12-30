import tweepy
import requests
from __keys import *
from random import randint
from moonmask.moon_image import MoonImage, CustomImage
import numpy as np
import cv2
import mimetypes

DIMS = (400, 400)

class MoonBot():
    def __init__(self):
        self.maxchar = 280 #twitter maxchar
        self.ascii_chars = ["🌑","㉄","㉄","🌕","🌕","🌕"]
        self.charwidth = 10
        self.charheight = 10

    def set_moon_chars(self):
        if self.moon.moon_info["age"] < 14:
            self.ascii_chars[1] = "🌒"
            self.ascii_chars[2] = "🌓"
        else:
            self.ascii_chars[1] = "🌘"
            self.ascii_chars[2] = "🌗"

    def make_ascii_tweet(self, cols, scale):
        self.set_moon_chars()
        self.convert_image_to_ascii(cols, scale)

    def twitter_signin(self):
        auth = tweepy.OAuthHandler(TWITTER_CONSUMER_KEY, TWITTER_CONSUMER_SECRET)
        auth.set_access_token(TWITTER_ACCESS_TOKEN, TWITTER_ACCESS_TOKEN_SECRET)
        auth.set_access_token(TWITTER_ACCESS_TOKEN, TWITTER_ACCESS_TOKEN_SECRET)
        self.api = tweepy.API(auth)

    def mast_set_headers(self):
        self.mast_host_instance = 'https://botsin.space'
        token = MAST_ACCESS_TOKEN
        self.mast_headers = {}
        self.mast_headers['Authorization'] = 'Bearer ' + token

    def post_moon_toot(self):
        data = {}
        data['status'] = self.moon_info_caption + self.ascii 
        data['visibility'] = 'public'

        response = requests.post(
            url=self.mast_host_instance + '/api/v1/statuses', data=data, headers=self.mast_headers)

        if response.status_code == 200:
            return True
        else:
            return False

    #TODO use python mastodon api port or figure out why this isn't working
    def mast_update_profile_image(self):
        files = {}
        avatar = open("./moon.jpg", 'rb')
        avatar_mime_type = mimetypes.guess_type("./moon.jpg")[0]
        avatar_file_name = "moon_" + avatar_mime_type
        files["avatar"] = (avatar_file_name, avatar, avatar_mime_type)
        response = requests.post(
            url=self.mast_host_instance + '/api/v1/accounts/update_credentials', files = files, headers = self.mast_headers, data = files)
        print(response.text)
        print(response.iter_content)
        print(response.url)
        print(response.reason)
        print(response.request)
        print(response.raw)
        print(response.headers)
        if response.status_code == 200:
            return True
        else:
            return False
        

    def get_moon(self, **kwargs):    
        self.moon = MoonImage(DIMS, "todaysmoon")
        self.moon.set_moon_image(**kwargs)
        cv2.imwrite("moon.jpg", self.moon.image)

    def get_test_moon(self):
        self.moon = CustomImage(DIMS, "testmoon", filename="moon.png")

    def get_random_image(self, **kwargs):
        self.moon = CustomImage(DIMS, "testmoon", **kwargs)

    def set_moon_info_caption(self):
        self.moon_info_caption = "...\n\n" + str(self.moon.moon_info["distance"]) + "km from earth".rjust(22, " ") + "\n" + str(self.moon.moon_info["phase"]) + "%" + "illuminated".rjust(26, " ") + "\n\n"

    def post_moon_tweet(self):
        self.api.update_status(self.moon_info_caption + self.ascii)

    def update_profile_image(self):
        self.api.update_profile_image("./moon.jpg")



#START pixelating grayscale image with characters/emojis#
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
        
        # check if image size is too small
        if cols > W or rows > H:
            print("Image too small for specified cols!")
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
                # get average luminance
                avg = int(self.getAverageL(img))
                # look up ascii char
                gsval = self.ascii_chars[int((avg*6)/255)]
                # append ascii char to string
                aimg[j].append(gsval)
        #transpose it as its currently rotated -90 deg
        aimg = list(map(list, np.transpose(aimg)))
        aimg_str = ""
        for x in aimg:
            for y in x:
                aimg_str += y
            aimg_str += "\n"
        
             
        # return txt image
        self.ascii = aimg_str
        return aimg
 
    def rgb_to_gray(self, img):
        grayImage = np.zeros(img.shape)
        R = np.array(img[:, :, 0])
        G = np.array(img[:, :, 1])
        B = np.array(img[:, :, 2])

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

    
## START trying to make art from text recognition tesseract #
#import pytesseract
#from pytesseract import Output
#
#TESS_CONFIG = ('-l eng --oem 1 --psm 10')# -c textord_min_linesize=15 -c preserve_interword_spaces=1')
#LINE_WIDTH = 6
#
###### thresholds for moon pics ###########
#THRESH_DARK = 25
#THRESH_MEDIUM1 = 120
#THRESH_MEDIUM2= 155
#THRESH_LIGHT = 205


#    def draw_contours(self):
#        im = cv2.imread('moon.png')
#        imgray = cv2.cvtColor(self.moon.image, cv2.COLOR_BGR2GRAY)
#
#        white_canvas = CustomImage(DIMS, "canvas", color=(255,255,255)).image
#        _, thresh_dark = cv2.threshold(imgray, THRESH_DARK, 255, 0)
#        contours_dark, _ = cv2.findContours(thresh_dark, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
#        
#        _, thresh_medium1 = cv2.threshold(imgray, THRESH_MEDIUM1, 255, 0)
#        contours_medium1, _ = cv2.findContours(thresh_medium1, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
#         
#        _, thresh_medium2 = cv2.threshold(imgray, THRESH_MEDIUM2, 255, 0)
#        contours_medium2, _ = cv2.findContours(thresh_medium2, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
#        
#        _, thresh_light= cv2.threshold(imgray, THRESH_LIGHT, 255, 0)
#        contours_light, _ = cv2.findContours(thresh_light, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
#
#        #thresh = cv2.threshold(self.moon.image, 127, 255, 0)
#
#	######colored contours##############################################
#        #cv2.drawContours(white_canvas, contours_light, -1, (255,0,0), 1)
#        #cv2.drawContours(white_canvas, contours_medium1, -1, (0,255,100), 1)
#        #cv2.drawContours(white_canvas, contours_medium2, -1, (255,0,255), 1)
#        #cv2.drawContours(white_canvas, contours_dark, -1, (0,150,255), 1)
#
#        cv2.drawContours(white_canvas, contours_light, -1, (0,0,0), LINE_WIDTH)
#        cv2.drawContours(white_canvas, contours_medium1, -1, (0,0,0), LINE_WIDTH)
#        #cv2.drawContours(white_canvas, contours_dark, -1, (0,0,0), LINE_WIDTH)
#        #cv2.imshow("test", white_canvas)
#        #cv2.waitKey()
#        #cv2.destroyAllWindows()
#        self.moon.image = white_canvas 
#
#    def get_image_tiles(self, im, num_tiles):
#        """Splits an image into num_tiles x num_tiles image array"""
#        tiles = []
#        im_dim = im.shape[0]
#        tile_dim = int(im_dim / num_tiles)
#        y1, y2 = 0, tile_dim 
#        for column in range(num_tiles):
#            tiles.append([])
#            x1, x2 = 0, tile_dim 
#            for row in range(num_tiles):
#                tiles[column].append(im[x1:x2, y1:y2])
#                x1 += tile_dim 
#                x2 += tile_dim
#                #cv2.imshow("test", tiles[column][row])
#                #cv2.waitKey()
#                #cv2.destroyAllWindows()
#            y1 += tile_dim
#            y2 += tile_dim
#        self.tiles = tiles
#   
#    def map_tiles_to_chars(self, tiles):
#        art = []
#        for column in range(len(tiles)):
#            art.append([])
#            for row in range(len(tiles)):
#                im = tiles[column][row] 
#                
#                d = pytesseract.image_to_data(im, config = TESS_CONFIG, output_type=Output.DICT)
#                print(d)
#                n_boxes = len(d['level'])
#
#                for i in range(n_boxes):
#                    (x, y, w, h, t) = (d['left'][i], d['top'][i], d['width'][i], d['height'][i], d["text"][i])
#                    cv2.rectangle(im, (x, y), (x + w, y + h), (0, 255, 0), 2)
#                    print(d["text"][i])
#                    cv2.imshow('img', im)
#                    cv2.waitKey()
#                    cv2.destroyAllWindows()
#
#
#                #char = char.rjust(7, ' ')
#                #print(char)
#                #art[column].append(char) 
#                #cv2.imshow("test", tiles[column][row])
#                #cv2.waitKey()
#                #cv2.destroyAllWindows()
#	#transpose it as its currently rotated -90 deg
#        #art = list(map(list, np.transpose(art)))
#        #for row in art:
#        #    s = "."
#        #    for col in row:
#        #        if col == "": col = " "
#        #        col = col 
#        #        col = col.center(4, " ")
#        #        s+=col 
#        #    print(s)
#        #print(art)
#   
#    def get_text(self):
#        self.text = pytesseract.image_to_string(self.moon.image, config = TESS_CONFIG)
#
#
# END trying to make art from text recognition tesseract #

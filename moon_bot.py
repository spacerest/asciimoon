from __keys import *
from random import randint
from moon.dialamoon import Moon as MoonImage, CustomImage
import numpy as np
import cv2, mimetypes, random, os, json, tweepy, requests
import settings_dict
from collections import Counter
from utilities import stretch

DIMS = (400, 400)
JSON_FN = "mooninfo_{year}.json"

class MoonBot():
    def __init__(self, cache_dir=None):
        self.maxchar = 280 #twitter maxchar
        self.light_gradient = [str(x).zfill(2) for x in range(100)]
        self.cache_dir = cache_dir

    def set_mode(self, mode):
        self.mode = mode
        self.settings = settings_dict.settings[mode]
        self.charwidth = self.settings["ascii_dims"][0]
        self.charheight = self.settings["ascii_dims"][1]
        self.ascii_gradient = ['']*(self.charwidth * self.charheight)

    def get_symbols_list(self, luminance):
        try:
            if self.moon.moon_datetime_info["age"] < 14:
 
                self.ascii_gradient = stretch(self.settings["symbols"]["young_moon"], self.charwidth * self.charheight)
            else:
                self.ascii_gradient = stretch(self.settings["symbols"]["old_moon"], self.charwidth * self.charheight)

            if self.settings["settings_type"] == "random":
                self.ascii_gradient = self.set_random_chars()
        except TypeError as e:
            raise TypeError(f'Something might be wrong with your settings_dict {self.mode} mode\n' + str(e))

    def set_random_chars(self):
        ##self.set_interval(5,100,self.settings["symbols"]["FULL_MOON"])
        #self.ascii_gradient[4] = "R"#self.choose_random_shadow_symbol()
        #self.ascii_gradient[6] = "R"#self.choose_random_shadow_symbol()
        #self.ascii_gradient[9] = "R"#self.choose_random_light_symbol()
        self.border_char = self.choose_random_shadow_symbol()
        return self.ascii_gradient

    def set_interval(self, start, end_inclusive, symbol):
        self.ascii_gradient[start:end_inclusive] = [symbol] * (end_inclusive-start)
    
    def decide_random_positions(self):
        #get a light gradient value that has minimum
        gradient_value_counts_dict = Counter(self.result_moon_gradients).most_common()
        #min1, min2, min3 = (gradient_value_count[-1], gradient_value_count[-2], gradient_value_count[-2])
        gradient_value_count = len(gradient_value_counts_dict)
        #print(gradient_value_count)
        #print(gradient_value_counts_dict)

    def decide_new_moon_border(self):
        if self.luminance <= .1 and self.settings["settings_type"] == "random":
            self.add_border = True
            surrounding_pixels_offsets = {
                        "char_to_left": -1, 
                        "char_to_right": 1, 
                        "char_above": -1 * self.charwidth,
                        "char_below": self.charwidth
                        }
            #make a shadow border
            for idx, value in enumerate(self.result_moon_gradients):
                for desc, offset in surrounding_pixels_offsets.items():
                    try:
                        if int(self.result_moon_gradients[idx + offset]) == 0 and int(self.result_moon_gradients[idx]) != 0:
                            # print("offset: " + str(offset))
                            # print(self.result_moon_gradients[idx + offset])
                            # print(self.result_moon_gradients[idx])
                            self.result_moon_gradients[idx] = -1

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
        self.decide_new_moon_border()
        self.get_symbols_list(self.luminance)
        self.put_symbols_in_gradient()
        self.put_output_in_square()
        self.decide_random_positions()

    def put_symbols_in_gradient(self):
        self.ascii_list = []
        for value in self.result_moon_gradients:
            if value == -1:
                self.ascii_list.append(self.border_char)
            else:
                self.ascii_list.append(self.ascii_gradient[int(value)])

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
        if response.status_code == 200:
            return True
        else:
            return False

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

            cv2.imwrite("moon.jpg", self.moon.image)
        except Exception as e:
            raise e

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

    def post_moon_tweet(self):
        self.api.update_status(self.ascii+self.moon_info_caption)

    def update_profile_image(self):
        self.api.update_profile_image("./moon.jpg")

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

        #why not get the average luminance of the whole image first
        self.luminance = self.getAverageL(im) / 100
        print("avg lum" + str(self.luminance))
        
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


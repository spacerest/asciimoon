#twitter display dimensions: 435 x 375
#http://freshtakeoncontent.com/twitter-image-sizes-dimensions/

import tweepy, time, sys, PIL, yaml
from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw
import glob, os, __keys
from random import randint

auth = tweepy.OAuthHandler(__keys.CONSUMER_KEY, __keys.CONSUMER_SECRET)
auth.set_access_token(__keys.ACCESS_TOKEN, __keys.ACCESS_TOKEN_SECRET)
auth.set_access_token(__keys.ACCESS_TOKEN, __keys.ACCESS_TOKEN_SECRET)
api = tweepy.API(auth)

def get_last_tweet(self):
    tweet = self.user_timeline(sn, count = 1)[0]
    return tweet

def find_new_caption(self,since_id):
    mentions_since = api.mentions_timeline(since_id)
    last_tweet = get_last_tweet(self)
    return mentions_since[randint(0,len(mentions_since)-1)]

def rebuild_caption(split_cap,maxchar):
    caption = ""
    line = ""
    r = range(len(split_cap))
    for word in split_cap:
        if len(line + word) + 1 >= maxchar:
            line += word + "\n"
            caption += line
	    line = ""
        else:
            line += word + " " 
    caption += line
    return caption 

def format_caption(caption, maxchar):
    if len(caption) < maxchar:
        return caption
    else:
        split_cap = caption.split(" ")   
        return rebuild_caption(split_cap, maxchar)        

def position_sn(caption_sn, maxchar):
    x = 435.0 - 435.0 / (maxchar / len(caption_sn) + 0.0)
    y = 349
    return (x,y)

def position_caption(caption, maxchar):
    if len(caption) < maxchar:
        return (15, 330)
    if len(caption) < maxchar * 2:
        return (15, 290)
    if len(caption) < maxchar * 3:
        return (15, 260)
    return (15, 230)

im = Image.open('./images/1.png')
w = im.width + 0.0
h = im.height + 0.0
num_posts = 11
sn = '_s_z_o_'
loop_thru = range(num_posts+1) 
loop_thru.remove(0)
p = (375+ 0.0)/435 

def run_bot():
    while True:
	np = open('nextpost.yml', "r")
	dataMap = yaml.safe_load(np)
	np.close()
	count = dataMap['c']
	image_num = dataMap['n']
		
	
	im = Image.open('./images/{}.png'.format(image_num))
    	box = (w/2 - (count*w/(num_posts*2)), h/2 - (count*w*p/(num_posts*2)), w/2 + (count*w/(num_posts*2)), h/2 + (count*w*p/(num_posts*2)))
    	im_to_post = im.crop(box)
    	im_to_post = im_to_post.resize((435,375))
    	draw = ImageDraw.Draw(im_to_post)
    	font = ImageFont.truetype("./fonts/zillah_modern_thin.ttf",27)
    	last_tweet = get_last_tweet(api)
    	mentions_since = api.mentions_timeline(last_tweet.id)
    	if len(mentions_since) == 0:
    	    caption_text = '_____________'
    	    caption_sn = '~@{}'.format(sn)
    	else:
    	    caption = find_new_caption(api, last_tweet.id)
    	    caption_text = caption.text
    	    caption_sn = " ~@" + caption.user.screen_name
    	#caption_text = "@ my bot tush sometime why don't you you fucking weirdo?"
    	#caption_sn = "~@youdontreallylovemedou"
    	draw.text(position_caption(caption_text, 30),format_caption(caption_text, 30),(255,255,255),font=font)
    	draw.text(position_sn(caption_sn, 30),format_caption(caption_sn, 30),(255,0,0),font=font)
    	im_to_post.save('./images/a.png')
	if count == num_posts + 1:
	    dataMap['n'] += 1
	    dataMap['c'] = 1
	else:
	    dataMap['c'] += 1
	np = open('nextpost.yml', "w")
	yaml.dump(dataMap, np)
	np.close()
    	api.update_with_media('./images/a.png',status="")
    	os.remove('./images/a.png')
    	time.sleep(60)#time.sleep(86446)

run_bot()
    



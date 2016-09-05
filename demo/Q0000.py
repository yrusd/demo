#coding=utf-8

from PIL import Image,ImageDraw,ImageFont
import random

msgNum = str(random.randint(1,99))

img = Image.open('background.png')
#img.show()
w,h = img.size
wDraw = 0.8 * w
hDraw = 0.08 * h

font=ImageFont.truetype('DroidSans.ttf', 18) 
draw = ImageDraw.Draw(img)
draw.text((wDraw,hDraw), msgNum, font=font, fill=(255,33,33))
#img.show()
# Save image
img.save('background_msg.png', 'png')
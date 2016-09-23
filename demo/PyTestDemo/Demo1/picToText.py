# coding: utf-8 -*-

from PIL import Image
import os
import sys

serarr = '''@#$%&?*aeoc=<{[(/l|!-_:;,."'^~` '''
count = len(serarr)

def toText(image_file):#�˺����������� gif �ļ�
   image_file = image_file.convert("L")#ת�Ҷ�
   asd = ''#�����ַ���
   for h in range(0,  image_file.size[1]):#h
      for w in range(0, image_file.size[0]):#w
         gray = image_file.getpixel((w,h))
         asd = asd + serarr[int(gray / (256 / (count)))]
      asd = asd + '\r\n'
   return asd
  
def toText2(image_file):
   asd = ''#�����ַ���
   for h in range(0,  image_file.size[1]):#h
      for w in range(0, image_file.size[0]):#w
         r,g,b = image_file.getpixel((w,h))
         gray = int(r * 0.299 + g * 0.587 + b * 0.114)
         asd = asd + serarr[int(gray / (256 / (count)))]
      asd = asd + '\r\n'
   return asd
  
  
image_file = Image.open(os.path.dirname(sys.argv[0]) + '\\' +"hehe.jpg") # ��ͼƬ
image_file = image_file.resize((int(image_file.size[0] * 0.275), int(image_file.size[1] * 0.125)))#����ͼƬ��С
print(u'Info:',image_file.size[0],' ',image_file.size[1],' ',count)
  
     
tmp = open(os.path.dirname(sys.argv[0]) + '\\' +'tmp.txt','w')
tmp.write(toText(image_file))
tmp.close()
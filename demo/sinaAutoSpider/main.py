#coding=utf-8

#from selenium import webdriver

#driver = webdriver.PhantomJS()
#driver.get('http://weibo.cn/u/1790107895?filter=1&page=1')
#print(driver.page_source)


#getHtml('http://m.weibo.cn/n/Reveur_Flolos?filter=1&page=1')


import re
import string
import sys
import os
import urllib
from bs4 import BeautifulSoup
import requests
from lxml import etree
from datetime import *
import time
import bs4

cookie = {"Cookie": "_T_WM=c449d927b8ea9f6d5355ab2cedf01a77; SCF=AkAhJl9oh7RcsgsbZoyMOx4dVbUDb9yAwskeisCt8f3K6mIQl6XYQQ5ZUnLxJoFeMCMu6MygiNytPE8zaHKHfyw.; SUB=_2A256zSOEDeTxGeRK7VIZ8ivJyDyIHXVWTk3MrDV6PUJbkdBeLVinkW0rb5XCttKXw35QFsKiMVWARD7lsg..; SUHB=05iLcEzvU3kRGm; SSOLoginState=1472811988; M_WEIBOCN_PARAMS=uicode%3D20000174"}

html = requests.get('http://weibo.cn/u/1790107895?filter=0&page=1', cookies = cookie).content.decode('utf-8')
re_nbsp = re.compile('&nbsp;')
html = re_nbsp.sub('',html)
blank_line = re.compile('\n+')#去掉多余的空行
html = blank_line.sub('',html)
re_time = re.compile('月|日| |:')
re_match = re.compile('(.*)(/attitude/|/repost/|/comment/|/fav/|赞|原文)(.*)')
#selector = etree.HTML(html)
#content = selector.xpath('//div[@class="c"]')
#for each in content:
#    text = each.xpath('string(.)')
#    print(text.replace(u'\xa0', u' '))
#print(html)
soup = BeautifulSoup(html,"lxml")
#i=1
#for tag in soup.title:
#    print(++i)
#    print(tag)
##print(soup.title)
##print(soup.find_all('div'))
#for tag in soup.find_all('title'):
#    print(tag)
j = 1
isTime = False
one = ''
isContinue = False
filename = time.strftime('%Y%m%d%H%M%S',time.localtime(time.time())) + '.txt'
fp = open(os.getcwd() + '\\' + filename,mode="a+",encoding="UTF-8") 
urlTail = False
for tag in soup.find_all('div', attrs={'class':'c','id':re.compile('\S')}):  
    for content in tag.descendants:          
        #print(j)
        #j+=1
        if(type(content) == bs4.element.Tag):
            #print("Tag")
            url = ''
            if(content.name == 'a'):
                url = urllib.parse.unquote(content.get("href"))
            if(content.name == 'img'):
                url = urllib.parse.unquote(content.get("src"))
            if url.startswith('/'):
                url = 'http://weibo.cn' + url
            if re.match(re_match,url):
                isContinue = True
                continue
            if url.startswith('http'):                
                if urlTail == False :
                    if(content.name == 'a'):
                        one += '<a href="' + url
                        urlTail = True
                    if(content.name == 'img'):
                        one += '<img src="' + url + '/>'
            if(content.name == 'span' and 'ct' in content.get("class")):
                isTime = True
            #print(content.replace(u'\xa0', u' '))
        elif(type(content) == bs4.element.NavigableString):
            info = str(content.string.replace(u'\xa0', u' ')).strip()
            if isContinue:
                isContinue = False
                continue
            if re.match(re_match,info):
                continue
            if urlTail:
                one+= '">' + info + '</a>'  
                urlTail = False
            else :
                one+=info
            if isTime:
                isTime = False
                fp.writelines(str(one) + '\n')
                one = ''
                print(re_time.sub('',info[0:12]))
            #if info.strip()=='':
            #    continue
        #print(content.replace(u'\xa0', u' '))
    #print(j)
    #j+=1
    ##print(type(tag.contents[0]))
    #print(type(tag))
    ##print(tag.contents[0].replace(u'\xa0', u' '))
    #print(tag.replace(u'\xa0', u' '))
    #print(tag.string.replace(u'\xa0', u' '))
    #print(tag.replace(u'\xa0', u' '))

#filename =time.strftime('%Y%m%d%H%M%S',time.localtime(time.time())) + '.txt'
#fp = open(os.getcwd() + '\\' + filename,mode="a+",encoding="UTF-8") 
#fp.writelines(str(html))

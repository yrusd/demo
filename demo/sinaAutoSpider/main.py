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

cookie = {"Cookie": "_T_WM=c449d927b8ea9f6d5355ab2cedf01a77; SCF=AkAhJl9oh7RcsgsbZoyMOx4dVbUDb9yAwskeisCt8f3K6mIQl6XYQQ5ZUnLxJoFeMCMu6MygiNytPE8zaHKHfyw.; SUB=_2A256zSOEDeTxGeRK7VIZ8ivJyDyIHXVWTk3MrDV6PUJbkdBeLVinkW0rb5XCttKXw35QFsKiMVWARD7lsg..; SUHB=05iLcEzvU3kRGm; SSOLoginState=1472811988; M_WEIBOCN_PARAMS=uicode%3D20000174"}

html = requests.get('http://weibo.cn/u/1790107895?filter=0&page=1', cookies = cookie).content.decode('UTF-8')

print(html)
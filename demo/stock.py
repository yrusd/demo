# -*- coding: utf-8 -*-
import hashlib
import web
import lxml
import time
import os
import urllib2
import json
from lxml import etree
import pylibmc
import urllib
import string
import itertools

class Stock:
    def GET(self):
        data = web.input()
        code = data.code
        url =  'http://hq.sinajs.cn/list=' + code
        req_header = {'User-Agent':'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
             'Accept':'text/html;q=0.9,*/*;q=0.8',
             'Accept-Charset':'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
             'Accept-Encoding':'gzip',
             'Connection':'close',
             'Referer':'www.niurenqushi.com' #ע????????Ȼ????ץȡ?Ļ???????????????ץȡ??վ??host
             }
        req = urllib2.Request(url, None)
        response = urllib2.urlopen(req)
        returnstr = response.read()
        
        return returnstr
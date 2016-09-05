#coding=utf-8
import urllib.request  
import urllib.parse  
import re  
import urllib.request,urllib.parse,http.cookiejar  
import time  
import os
import json

def getHtml(url):  
  
      
    cj=http.cookiejar.CookieJar()  
    opener=urllib.request.build_opener(urllib.request.HTTPCookieProcessor(cj))  
    opener.addheaders=[('User-Agent','Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2272.101 Safari/537.36'),('Cookie','4564564564564564565646540'),('apikey','d537c2a89195597876e920678da7d066')]  
  
    urllib.request.install_opener(opener)  
      
    page = urllib.request.urlopen(url)  
    html = page.read().decode('UTF-8')
    return html  

def GetContext(context,param):
    result=''    
    for s in str(param).split('/'):
        result=result+s+':'+str(context[s])+'\n'
    return result

c=input('code:\n')
code=''
for s in c.split(','):
    code=code+'sz'+s+',' if s.startswith('00') else code+'sh'+s+','
while True:
    html = getHtml('http://apis.baidu.com/apistore/stockservice/stock?stockid='+code[:-1]+'&list=1')
    html=json.dumps(json.loads(html),ensure_ascii=False)
    html=json.loads(html)
    i=0
    stock=''
    for s in c.split(','):
        stockinfo=html['retData']['stockinfo'][i]
    #name/code/date/time/OpenningPrice/closingPrice/currentPrice/hPrice/lPrice
        stockinfo=GetContext(stockinfo,'name/code/date/time/currentPrice/hPrice/lPrice/OpenningPrice/closingPrice')
        stock=stock+str(stockinfo)+'\n'
        i=i+1
    shanghai=html['retData']['market']['shanghai']
    #name/curdot/curprice/rate
    shanghai=GetContext(shanghai,'name/curdot/curprice/rate')
    shenzhen=html['retData']['market']['shenzhen']
    #name/curdot/curprice/rate
    shenzhen=GetContext(shenzhen,'name/curdot/curprice/rate')
    print(str(shanghai)+str(shenzhen)+str(stock))
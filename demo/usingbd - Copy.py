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
    opener.addheaders=[('User-Agent','Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2272.101 Safari/537.36')]  
  
    urllib.request.install_opener(opener)  
      
    page = urllib.request.urlopen(url)  
    html = page.read().decode('GBK')
    return html  

def GetContext(context,param):
    result=''    
    for s in str(param).split('/'):
        result=result+s+':'+str(context[s])+'\n'
    return result

c=input('code:\n')
code=''
for s in c.split(','):
    code=code+'sh'+s+',' if s.startswith('60') else code+'sz'+s+','
while True:
    html = getHtml('http://hq.sinajs.cn/list='+code+'s_sh000001,s_sz399001')
    eachCode=code[:-1].split(',')
    eachInfo=html.split(';')
    stock=''
    for i in range(len(eachCode)):
        info=eachInfo[i].split('"')[1].split(',');
        #name/code/date/time/currentPrice/hPrice/lPrice/OpenningPrice/closingPrice
        stock=stock+info[0]+eachCode[i]+info[30]+info[31]+info[3]+info[4]+info[5]+info[1]+info[2]+','
    sh=eachInfo[len(eachInfo)-3].split('"')[1]
    sz=eachInfo[len(eachInfo)-2].split('"')[1]
    print(sh+'\n'+sz+'\n'+stock)

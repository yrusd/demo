#coding=utf-8
import urllib.request  
import urllib.parse  
import re  
import urllib.request,urllib.parse,http.cookiejar  
import time  
import os

def getHtml(url):  
  
      
    cj=http.cookiejar.CookieJar()  
    opener=urllib.request.build_opener(urllib.request.HTTPCookieProcessor(cj))  
    opener.addheaders=[('User-Agent','Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2272.101 Safari/537.36'),('Cookie','4564564564564564565646540')]  
  
    urllib.request.install_opener(opener)  
      
    page = urllib.request.urlopen(url)  
    html = page.read().decode('UTF-8')
    return html  
#print ( html)  

ISOTIMEFORMAT='%Y-%m-%d %X'
c=input('code:\n')
top=999#input('toplimit:\n')
lower=0#input('lowerlimit:\n')
flag=True
topflag=False
lowerflag=False
code=c.split('-')[0]
while flag:
    html = getHtml("https://www.baidu.com/s?ie=UTF-8&wd="+str(code))
    html=html[html.index('<li class="c-tabs-nav-li c-tabs-nav-selected" data-click="{\'fm\':\'beha\'}" data-resourceid="6896">东方财富网</li>'):]
    html=html[:html.index('<div class="op-stockdynamic-moretab-bottom c-gap-top"')]
    nowprice=html[html.index('<span class="op-stockdynamic-moretab-cur-num c-gap-right-small">'):html.index('</span>')]
    re_br=re.compile('<br\s*?/?>')#处理换行
    re_h=re.compile('</?\w+[^>]*>')#HTML标签
    s=html.replace('东方财富网','').replace('同花顺','')
    s=re_br.sub('',s)#将br转换为换行
    s=re_h.sub('',s) #去掉HTML 标签
    nowprice=re_h.sub('',nowprice)
    blank_line=re.compile('\n+')
    s=blank_line.sub('\n',s).replace('\t','').replace(' ','').replace('分时','').replace('5日','').replace('1月','').replace('1年','')
    nowGGpercent=float(s[s.index('(')+1:s.index(')')].replace('+','').replace('%',''))
    nowSZpercent=s[s.index('上证:'):]
    nowSZpercent=float(nowSZpercent[nowSZpercent.index('(')+1:nowSZpercent.index(')')].replace('+','').replace('%',''))
    nowSZpercent=nowSZpercent*2 if nowSZpercent>0 else nowSZpercent/2
    nowSZpercent=nowSZpercent if nowSZpercent<10 else 10
    if nowGGpercent>=nowSZpercent :
        flag=False
        topflag=True
    if nowGGpercent<nowSZpercent:
        flag=False
        lowerflag=True
    last=''
    i=0
    for tt in s.splitlines():
        if(tt!=''):        
            tt=tt+'\n'
        last=last+tt
    now=time.strftime( ISOTIMEFORMAT, time.localtime() )
    print(c+" "+now+"\n"+last)
    
    #time.sleep(1)
file=''
if topflag:
    file="start "+os.getcwd()+"/五月天-伤心的人别听慢歌.mp3"
if lowerflag:
    file="start "+os.getcwd()+"/五月天-步步.mp3"
os.system(file)

  

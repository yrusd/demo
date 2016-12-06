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

class WeixinInterface:

    def __init__(self):
        self.app_root = os.path.dirname(__file__)
        self.templates_root = os.path.join(self.app_root, 'templates')
        self.render = web.template.render(self.templates_root)

    def GET(self):
        #获取输入参数
        data = web.input()
        signature = data.signature
        timestamp = data.timestamp
        nonce = data.nonce
        echostr = data.echostr
        #自己的token
        token = "monsieur" #这里改写你在微信公众平台里输入的token
        #字典序排序
        list = [token,timestamp,nonce]
        list.sort()
        sha1 = hashlib.sha1()
        map(sha1.update,list)
        hashcode = sha1.hexdigest()
        #sha1加密算法

        #如果是来自微信的请求，则回复echostr
        if hashcode == signature:
            return echostr
        
    def xiaohuangji(ask):
        ask = ask.encode('UTF-8')
        enask = urllib2.quote(ask)
        baseurl = r'http://www.simsimi.com/func/req?msg='
        url = baseurl + enask + '&lc=ch&ft=0.0'
        resp = urllib2.urlopen(url)
        reson = json.loads(resp.read())
        return reson
    
    def xhj(self,ask):
        req = urllib2.Request(r"http://www.niurenqushi.com/app/simsimi/")  
        data = {'txt':ask}
        data = urllib.urlencode(data)  
    	#enable cookie
        opener = urllib2.build_opener(urllib2.HTTPCookieProcessor())  
        response = opener.open(req, data)  
        return response.read()
        
    def POST(self):
        
        str_xml = web.data()
        xml = etree.fromstring(str_xml)        
        msgType = xml.find("MsgType").text
        fromUser = xml.find("FromUserName").text
        toUser = xml.find("ToUserName").text
        replytext = "<xml><ToUserName><![CDATA[%s]]></ToUserName><FromUserName><![CDATA[%s]]></FromUserName><CreateTime>%s</CreateTime><MsgType><![CDATA[%s]]></MsgType><Content><![CDATA[%s]]></Content><FuncFlag>0</FuncFlag></xml>"
        
        autoReturn = True
        #return replytext % (fromUser, toUser, str(int(time.time())), msgType,
        #msgType)

        if msgType == "event":
            mscontent = xml.find("Event").text
            if mscontent == "subscribe":                
                return replytext % (fromUser, toUser, str(int(time.time())), 'text', u'大佬，目前已支持阴阳师悬赏封印线索搜索，单个式神击杀搜索，多个式神击杀搜索（如同时要击杀樱花妖和雪女，搜索“樱花妖，雪女”即可）。')
            if mscontent == "unsubscribe":
                return replytext % (fromUser, toUser, str(int(time.time())), 'text', u'我现在功能还很简单，知道满足不了您的需求，但是我会慢慢改进，欢迎您以后再来')

        content = xml.find("Content").text
        
        ssrDic = dict()
        ssrDic.setdefault(u'赤舌','15-1|2|3|4|5|6-6')
        ssrDic.setdefault(u'盗墓小鬼','2-5-2')
        ssrDic.setdefault(u'灯笼鬼','9-1-3')
        ssrDic.setdefault(u'寄生魂','11-1-3')
        ssrDic.setdefault(u'天邪鬼青','10-1|2-4')
        ssrDic.setdefault(u'天邪鬼黄','5-4|5-4')
        ssrDic.setdefault(u'天邪鬼赤','4-3-3')
        ssrDic.setdefault(u'天邪鬼绿','6-3|4-6')
        ssrDic.setdefault(u'提灯小僧','1-2-2')
        ssrDic.setdefault(u'唐纸伞妖','4-1|6-4')
        ssrDic.setdefault(u'涂壁','14-2|3|6-18')
        ssrDic.setdefault(u'帚神','6-1|2-6')
        ssrDic.setdefault(u'跳跳犬','7-4|5-6')
        ssrDic.setdefault(u'黑豹','5-1-1')
        ssrDic.setdefault(u'兵俑','3-3|4-2')
        ssrDic.setdefault(u'丑时之女','10-1|2-2')
        ssrDic.setdefault(u'独眼小僧','11-2-3')
        ssrDic.setdefault(u'饿鬼','11-6-3')
        ssrDic.setdefault(u'管狐','5-5-2')
        ssrDic.setdefault(u'河童','7-3|7-2')
        ssrDic.setdefault(u'蝴蝶镜','6-5|6-1')
        ssrDic.setdefault(u'九命猫','15-2|4|5-6')
        ssrDic.setdefault(u'觉','10-3|4|5|6-4')
        ssrDic.setdefault(u'椒图','y3')
        ssrDic.setdefault(u'鲤鱼精','7-1-3')
        ssrDic.setdefault(u'狸猫','10-3-3')
        ssrDic.setdefault(u'青蛙瓷器','4-boss-1')
        ssrDic.setdefault(u'食发鬼','10-boss-1')
        ssrDic.setdefault(u'首无','13-5-6')
        ssrDic.setdefault(u'山童','16-1|4|5-6')
        ssrDic.setdefault(u'山兔','9-4-4')
        ssrDic.setdefault(u'三尾狐','6-5|6-2')
        ssrDic.setdefault(u'铁鼠','9-3|6-4')
        ssrDic.setdefault(u'童男','12-4|5-2')
        ssrDic.setdefault(u'童女','3-6-3')
        ssrDic.setdefault(u'巫蛊师','6-boss-1')
        ssrDic.setdefault(u'武士之灵','11-1|2-2')
        ssrDic.setdefault(u'鸦天狗','12-2|4|5-6')
        ssrDic.setdefault(u'雨女','4-boss-1')
        ssrDic.setdefault(u'莹草','y2')
        ssrDic.setdefault(u'座敷','10-5|6-4')
        ssrDic.setdefault(u'凤凰火','3-boss-1')
        ssrDic.setdefault(u'鬼使白','16-boss-1')
        ssrDic.setdefault(u'鬼使黑','16-boss-1')
        ssrDic.setdefault(u'鬼女红叶','11-boss-2')
        ssrDic.setdefault(u'骨女','10-boss-1')
        ssrDic.setdefault(u'海坊主','12-1|2-2')
        ssrDic.setdefault(u'傀儡师','10-1|2|4|6-4')
        ssrDic.setdefault(u'镰鼬','y5')
        ssrDic.setdefault(u'孟婆','9-boss-1')
        ssrDic.setdefault(u'判官','16-boss-1')
        ssrDic.setdefault(u'犬神','10-5|6-2')
        ssrDic.setdefault(u'食梦貘','14-boss-4')
        ssrDic.setdefault(u'桃花妖','8-boss-1')
        ssrDic.setdefault(u'跳跳哥哥','12-boss-1')
        ssrDic.setdefault(u'雪女','8-2|6-2')
        ssrDic.setdefault(u'吸血姬','y2')
        ssrDic.setdefault(u'妖狐','y2')
        ssrDic.setdefault(u'樱花妖','8-2|6|boss-3')
        ssrDic.setdefault(u'大天狗','15-5-1')
        ssrDic.setdefault(u'荒川之主','17-boss-1')
        ssrDic.setdefault(u'酒吞童子','10-boss-2')
        ssrDic.setdefault(u'阎魔','y6')
        
        ssrXSDic = dict()
        ssrXSDic.setdefault(u'书生',u'妖狐:第7章、御魂2')
        ssrXSDic.setdefault(u'二筒',u'青蛙瓷器:第4章、御魂3')
        ssrXSDic.setdefault(u'云',u'阎魔:御魂6')
        ssrXSDic.setdefault(u'人偶',u'傀儡师:第10章、御魂5')
        ssrXSDic.setdefault(u'伞',u'雨女:第4章、御魂6')
        ssrXSDic.setdefault(u'冥界',u'阎魔:御魂6')
        ssrXSDic.setdefault(u'冥界',u'鬼使白:第16章、御魂4')
        ssrXSDic.setdefault(u'出千',u'青蛙瓷器:第4章、御魂3')
        ssrXSDic.setdefault(u'剑',u'兵俑:第3/10章、御魂2\r\n镰鼬:御魂5')
        ssrXSDic.setdefault(u'剑雀',u'犬神:第10章、御魂4')
        ssrXSDic.setdefault(u'单眼',u'山童:第8/16章、御魂1\r\n天邪鬼黄:第3、5、12章\r\n独眼小僧:第11章、御魂1/5')
        ssrXSDic.setdefault(u'和尚',u'独眼小僧:第11章、御魂1/5')
        ssrXSDic.setdefault(u'可爱',u'蝴蝶精:第6/8章、御魂3/8')
        ssrXSDic.setdefault(u'咒锥',u'丑时之女:第10章、御魂5/7')
        ssrXSDic.setdefault(u'噩梦',u'食梦貘:第14章、御魂4/9')
        ssrXSDic.setdefault(u'坚甲',u'兵俑:第3/10章、御魂2')
        ssrXSDic.setdefault(u'大翅膀',u'大天狗:第15/18章、御魂4/10')
        ssrXSDic.setdefault(u'夺命',u'鬼使白:第16章、御魂4')
        ssrXSDic.setdefault(u'妖艳',u'三尾狐:第6/18章、御魂1')
        ssrXSDic.setdefault(u'守护',u'犬神:第10章、御魂4')
        ssrXSDic.setdefault(u'小妖精',u'蝴蝶精:第6/8章、御魂3/8')
        ssrXSDic.setdefault(u'尾巴',u'椒图:妖气封印、御魂3/8/9/10\r\n鲤鱼精:第7章、御魂2/3/9')
        ssrXSDic.setdefault(u'屋',u'犬神:第10章、御魂4')
        ssrXSDic.setdefault(u'幸运',u'座敷童子:第2章、御魂3/6')
        ssrXSDic.setdefault(u'幼女',u'童女:第3/11/12章、御魂2/4')
        ssrXSDic.setdefault(u'怪力',u'山童:第8/16章、御魂1')
        ssrXSDic.setdefault(u'扇',u'大天狗:第15/18章、御魂4/10')
        ssrXSDic.setdefault(u'扇子',u'椒图:妖气封印、御魂3/8/9/10')
        ssrXSDic.setdefault(u'手鼓',u'蝴蝶精:第6/8章、御魂3/8')
        ssrXSDic.setdefault(u'拍屁股',u'天邪鬼赤:第4/5/6/7/13/14/15章、御魂1')
        ssrXSDic.setdefault(u'操纵',u'傀儡师:第10章、御魂5')
        ssrXSDic.setdefault(u'杖',u'海坊主:第12章、妖气封印、御魂3')
        ssrXSDic.setdefault(u'棺材',u'跳跳哥哥:第10/12章、御魂5/10、妖气封印')
        ssrXSDic.setdefault(u'樱花树',u'三尾狐:第6/18章、御魂1')
        ssrXSDic.setdefault(u'水池',u'鲤鱼精:第7章、御魂2/3/9\r\n河童:第7章、御魂2')
        ssrXSDic.setdefault(u'水泡',u'鲤鱼精:第7章、御魂2/3/9')
        ssrXSDic.setdefault(u'水球',u'河童:第7章、御魂2')
        ssrXSDic.setdefault(u'汤碗',u'孟婆:第9章、御魂5/6')
        ssrXSDic.setdefault(u'河流',u'河童:第7章、御魂2')
        ssrXSDic.setdefault(u'治疗',u'萤草:御魂2/9/10')
        ssrXSDic.setdefault(u'泪珠',u'雨女:第4章、御魂6')
        ssrXSDic.setdefault(u'海',u'海坊主:第12章、妖气封印、御魂3')
        ssrXSDic.setdefault(u'渔夫',u'海坊主:第12章、妖气封印、御魂3')
        ssrXSDic.setdefault(u'牙牙',u'孟婆:第9章、御魂5/6')
        ssrXSDic.setdefault(u'献祭',u'童男:第12章、御魂4')
        ssrXSDic.setdefault(u'琴',u'孟婆:第9章、御魂5/6')
        ssrXSDic.setdefault(u'瓷',u'青蛙瓷器:第4章、御魂3')
        ssrXSDic.setdefault(u'白',u'鬼使白:第16章、御魂4')
        ssrXSDic.setdefault(u'短刀',u'鬼使黑:妖气封印、第16章、御魂4')
        ssrXSDic.setdefault(u'石',u'凃壁:第4/14章、御魂1')
        ssrXSDic.setdefault(u'石墙',u'凃壁:第4/14章、御魂1')
        ssrXSDic.setdefault(u'石化',u'兵俑:第3/10章、御魂2')
        ssrXSDic.setdefault(u'兵甲',u'兵俑:第3/10章、御魂2')
        ssrXSDic.setdefault(u'石菩萨',u'独眼小僧:第11章、御魂1/5')
        ssrXSDic.setdefault(u'石锤',u'山童:第8/16章、御魂1')
        ssrXSDic.setdefault(u'稻草人',u'丑时之女:第10章、御魂5/7')
        ssrXSDic.setdefault(u'笛子',u'大天狗:第15/18章、御魂4/10')
        ssrXSDic.setdefault(u'红尾',u'三尾狐:第6/18章、御魂1')
        ssrXSDic.setdefault(u'红色',u'三尾狐:第6/18章、御魂1')
        ssrXSDic.setdefault(u'红鬼',u'天邪鬼赤:第4/5/6/7/13/14/15章、御魂1')
        ssrXSDic.setdefault(u'纸扇',u'妖狐:第7章、御魂2')
        ssrXSDic.setdefault(u'羽毛',u'大天狗:第15/18章、御魂4/10')
        ssrXSDic.setdefault(u'羽衣',u'童女:第3/11/12章、御魂2/4')
        ssrXSDic.setdefault(u'翅膀',u'童女:第3/11/12章、御魂2/4\r\n童男:第12章、御魂4\r\n鸦天狗:第3/9/12/17/18章、御魂6')
        ssrXSDic.setdefault(u'胡须',u'海坊主:第12章、妖气封印、御魂3')
        ssrXSDic.setdefault(u'舞',u'桃花妖:第8章、御魂3')
        ssrXSDic.setdefault(u'花',u'桃花妖:第8章、御魂3')
        ssrXSDic.setdefault(u'荷叶',u'河童:第7章、御魂2')
        ssrXSDic.setdefault(u'蒲公英',u'萤草:御魂2/9/10')
        ssrXSDic.setdefault(u'蜡烛',u'跳跳哥哥:第10/12章、御魂5/10、妖气封印')
        ssrXSDic.setdefault(u'蝙蝠',u'吸血姬:御魂2层')
        ssrXSDic.setdefault(u'血',u'吸血姬:御魂2层')
        ssrXSDic.setdefault(u'角',u'座敷童子:第2章、御魂3/6')
        ssrXSDic.setdefault(u'贝壳',u'椒图:妖气封印、御魂3/8/9/10')
        ssrXSDic.setdefault(u'财富',u'座敷童子:第2章、御魂3/6')
        ssrXSDic.setdefault(u'金刚经',u'独眼小僧:第11章、御魂1/5')
        ssrXSDic.setdefault(u'钉耙',u'镰鼬:御魂5')
        ssrXSDic.setdefault(u'铃铛',u'食梦貘:第14章、御魂4/9')
        ssrXSDic.setdefault(u'锤子',u'镰鼬:御魂5')
        ssrXSDic.setdefault(u'锤',u'镰鼬:御魂5')
        ssrXSDic.setdefault(u'雉刀',u'鸦天狗:第3/9/12/17/18章、御魂6')
        ssrXSDic.setdefault(u'雨',u'雨女:第4章、御魂6')
        ssrXSDic.setdefault(u'雨衣',u'童男:第12章、御魂4')
        ssrXSDic.setdefault(u'青皮肤',u'天邪鬼青:第2/5/6/10/11章')
        ssrXSDic.setdefault(u'青苔',u'凃壁:第4/14章、御魂1')
        ssrXSDic.setdefault(u'面具',u'妖狐:第7章、御魂2\r\n鸦天狗:第3/9/12/17/18章、御魂6')
        ssrXSDic.setdefault(u'风',u'大天狗:第15/18章、御魂4/10')
        ssrXSDic.setdefault(u'风筝',u'天邪鬼青:第2/5/6/10/11章')
        ssrXSDic.setdefault(u'鬼火',u'座敷童子:第2章、御魂3/6')
        ssrXSDic.setdefault(u'鬼面',u'阎魔:御魂6')
        ssrXSDic.setdefault(u'黑镰',u'鬼使黑:妖气封印、第16章、御魂4')
        ssrXSDic.setdefault(u'鼓',u'天邪鬼黄:第3、5、12章')
        
        newSsrDic = dict()


        newSsrDic.setdefault(u'三尾狐',[u'御魂一层一回合-1',u'第三章式神挑战',u'第六章蝴蝶精-1'])
        newSsrDic.setdefault(u'丑时之女',[u'御魂七层一回合-1',u'御魂五层一回合-1',u'第十章丑时之女-1',u'第十章式神挑战'])
        newSsrDic.setdefault(u'黑豹',[u'第五章涂壁1-1'])
        newSsrDic.setdefault(u'两面佛',[u'御魂九层三回合-2'])
        newSsrDic.setdefault(u'九命猫',[u'第一章式神挑战',u'第一章首领-3',u'第十五章提灯小僧12-2',u'第十五章提灯小僧3-2',u'第十五章首领-3'])
        newSsrDic.setdefault(u'二口女',[u'妖气封印',u'御魂十层一回合-1'])
        newSsrDic.setdefault(u'傀儡师',[u'御魂五层二回合-1',u'第十章丑时之女-1',u'第十章傀儡师1-1',u'第十章傀儡师2-1'])
        newSsrDic.setdefault(u'八歧大蛇',[u'御魂一层三回合-1',u'御魂七层三回合-1',u'御魂三层三回合-1',u'御魂二层三回合-1',u'御魂五层三回合-1',u'御魂六层三回合-1',u'御魂四层三回合-1'])
        newSsrDic.setdefault(u'兵俑',[u'御魂二层二回合-1',u'第三章兵俑1-1',u'第三章兵俑2-1',u'第十三章式神挑战',u'第十章首领-1'])
        newSsrDic.setdefault(u'凤凰火',[u'御魂七层一回合-1',u'第三章首领-1'])
        newSsrDic.setdefault(u'判官',[u'御魂八层一回合-1',u'第十六章首领-1'])
        newSsrDic.setdefault(u'吸血姬',[u'御魂二层二回合-1'])
        newSsrDic.setdefault(u'唐纸伞妖',[u'第八章唐纸伞妖1-1',u'第八章唐纸伞妖2-1',u'第八章式神挑战',u'第十三章唐纸伞妖12-1',u'第十三章唐纸伞妖3-1',u'第四章唐纸伞妖1-1',u'第四章唐纸伞妖2（困难模式）-1',u'第四章唐纸伞妖2（简单模式）-1',u'第四章天邪鬼赤1-1',u'第四章天邪鬼赤2-2',u'第四章帚神2（困难模式）-3',u'第四章帚神2（简单模式）-2'])
        newSsrDic.setdefault(u'大天狗',[u'御魂十层三回合-2',u'御魂四层二回合-1',u'第十五章提灯小僧3-1'])
        newSsrDic.setdefault(u'天邪鬼绿',[u'第一章天邪鬼绿1（困难模式）-1',u'第一章天邪鬼绿1（普通模式）-1',u'第一章天邪鬼绿2-1',u'第一章式神挑战',u'第一章提灯小僧1-2',u'第二章首领-2',u'第五章管狐2-3',u'第八章天邪鬼绿-1',u'第六章天邪鬼青-3',u'第六章首领-3',u'第十三章唐纸伞妖12-2',u'第十三章唐纸伞妖3-2',u'第十五章天邪鬼绿123-1'])
        newSsrDic.setdefault(u'天邪鬼赤',[u'御魂一层三回合-2',u'第七章式神挑战',u'第七章首领-2',u'第五章帚神1-1',u'第五章帚神2-1',u'第五章涂壁1-2',u'第五章涂壁2-3',u'第六章蝴蝶精-2',u'第十一章独眼小僧1-2',u'第十一章独眼小僧2-2',u'第十三章唐纸伞妖12-1',u'第十三章唐纸伞妖3-1',u'第十三章饿鬼12-3',u'第十三章饿鬼3-3',u'第十五章天邪鬼绿123-2',u'第十四章帚神123-3',u'第十四章首领-3',u'第四章唐纸伞妖1-3',u'第四章唐纸伞妖2（简单模式）-1',u'第四章天邪鬼赤1-1',u'第四章天邪鬼赤2-1'])
        newSsrDic.setdefault(u'天邪鬼青',[u'御魂一层一回合-1',u'第九章式神挑战',u'第二章首领-1',u'第五章首领-2',u'第八章天邪鬼绿-1',u'第八章首领-1',u'第六章天邪鬼青-1',u'第十一章首领-2',u'第十章丑时之女-2'])
        newSsrDic.setdefault(u'天邪鬼黄',[u'御魂一层一回合-1',u'第三章天邪鬼黄1-1',u'第三章天邪鬼黄2-1',u'第三章式神挑战',u'第三章赤舌2-1',u'第五章帚神2-2',u'第五章管狐1-2',u'第八章天邪鬼绿-2',u'第十二章童男1-1'])
        newSsrDic.setdefault(u'妖狐',[u'御魂二层一回合-1',u'第七章首领-1'])
        newSsrDic.setdefault(u'妖琴师',[u'御魂七层二回合-1'])
        newSsrDic.setdefault(u'孟婆',[u'御魂五层三回合-2',u'御魂六层一回合-1',u'第九章首领-1'])
        newSsrDic.setdefault(u'寄生魂',[u'第七章首领-1',u'第三章首领-3',u'第二章寄生魂1-1',u'第二章寄生魂2-1',u'第二章帚神-1',u'第二章盗墓小鬼1-2',u'第五章管狐1-1',u'第五章管狐2-1',u'第十一章式神挑战',u'第十一章武士之灵1-3',u'第十二章首领-1',u'第十六章赤舌13-3',u'第十六章赤舌2-3'])
        newSsrDic.setdefault(u'山兔',[u'御魂七层二回合-1',u'第九章山兔1-4',u'第九章山兔2-3',u'第九章式神挑战',u'第十七章首领-1',u'第十三章首领-1',u'第十六章饿鬼123-1'])
        newSsrDic.setdefault(u'山童',[u'御魂一层二回合-1',u'第八章唐纸伞妖2-1',u'第十六章式神挑战',u'第十六章饿鬼123-2'])
        newSsrDic.setdefault(u'巫蛊师',[u'御魂六层二回合-1',u'第六章式神挑战',u'第六章首领-1'])
        newSsrDic.setdefault(u'帚神',[u'第七章鲤鱼精1-1',u'第七章鲤鱼精2-3',u'第三章天邪鬼黄1-2',u'第九章铁鼠1-3',u'第九章铁鼠2-2',u'第二章帚神-1',u'第五章帚神1-1',u'第五章帚神2-1',u'第五章式神挑战',u'第八章唐纸伞妖1-3',u'第八章唐纸伞妖2-2',u'第八章樱花妖1-1',u'第八章首领-1',u'第六章灯笼鬼-3',u'第十二章海坊主1-1',u'第十四章帚神123-1',u'第四章帚神1-1',u'第四章帚神2（困难模式）-1',u'第四章帚神2（简单模式）-1',u'第四章首领-2'])
        newSsrDic.setdefault(u'座敷童子',[u'御魂三层三回合-2',u'御魂六层一回合-1',u'第七章首领-2',u'第二章式神挑战',u'第二章首领-1',u'第十章傀儡师2-2',u'第十章觉2-2'])
        newSsrDic.setdefault(u'提灯小僧',[u'第一章天邪鬼绿2-2',u'第一章提灯小僧1-1',u'第一章提灯小僧2-1',u'第七章提灯小僧12-1',u'第七章提灯小僧3-1',u'第三章兵俑1-1',u'第三章兵俑2-1',u'第三章赤舌1-1',u'第九章提灯小僧1-1',u'第九章提灯小僧2-1',u'第二章式神挑战',u'第八章首领-2',u'第十二章童女1-2',u'第十五章提灯小僧12-1',u'第十五章提灯小僧3-1'])
        newSsrDic.setdefault(u'暗凤凰',[u'第十七章狸猫3-1'])
        newSsrDic.setdefault(u'桃花妖',[u'御魂三层一回合-1',u'第八章式神挑战',u'第八章首领-1'])
        newSsrDic.setdefault(u'椒图',[u'妖气封印',u'御魂三层二回合-1',u'御魂九层一回合-1',u'御魂八层二回合-1',u'御魂十层二回合-1'])
        newSsrDic.setdefault(u'樱花妖',[u'第八章樱花妖1-1',u'第八章樱花妖2-1',u'第八章首领-1'])
        newSsrDic.setdefault(u'武士之灵',[u'第十一章武士之灵1-1',u'第十一章武士之灵2-1',u'第十二章首领-2',u'第十章式神挑战'])
        newSsrDic.setdefault(u'河童',[u'御魂二层一回合-1',u'第七章式神挑战',u'第七章河童1-1',u'第七章河童2-1'])
        newSsrDic.setdefault(u'海坊主',[u'妖气封印',u'御魂三层二回合-1',u'第十二章海坊主1-1',u'第十二章海坊主2-1'])
        newSsrDic.setdefault(u'涂壁',[u'御魂一层二回合-1',u'第七章河童1-2',u'第七章首领-1',u'第三章天邪鬼黄1-1',u'第五章帚神1-2',u'第五章涂壁1-1',u'第五章涂壁2-1',u'第八章樱花妖1-2',u'第八章樱花妖2-3',u'第六章蝴蝶精-1',u'第十一章独眼小僧1-1',u'第十一章饿鬼1-1',u'第十三章式神挑战',u'第十二章海坊主1-2',u'第十二章海坊主2-1',u'第十四章涂壁12-6',u'第十四章涂壁3-6',u'第四章唐纸伞妖2（困难模式）-3',u'第四章唐纸伞妖2（简单模式）-2',u'第四章天邪鬼赤1-2',u'第四章帚神1-2',u'第四章帚神2（简单模式）-1'])
        newSsrDic.setdefault(u'清姬',[u'御魂九层二回合-1'])
        newSsrDic.setdefault(u'灯笼鬼',[u'第一章天邪鬼绿1（普通模式）-2',u'第一章提灯小僧2-2',u'第七章河童2-1',u'第三章兵俑2-2',u'第三章赤舌1-2',u'第九章提灯小僧1-3',u'第九章提灯小僧2-1',u'第九章首领-1',u'第二章寄生魂1-2',u'第二章盗墓小鬼2-2',u'第五章首领-1',u'第六章式神挑战',u'第六章灯笼鬼-1',u'第十七章首领-1',u'第十三章首领-1'])
        newSsrDic.setdefault(u'犬神',[u'御魂四层一回合-1',u'第十章傀儡师2-1',u'第十章觉2-1'])
        newSsrDic.setdefault(u'独眼小僧',[u'御魂一层二回合-1',u'御魂五层二回合-1',u'第十一章武士之灵2-3',u'第十一章独眼小僧1-2',u'第十一章独眼小僧2-2',u'第十八章式神挑战'])
        newSsrDic.setdefault(u'狸猫',[u'御魂九层二回合-1',u'第十七章狸猫12-1',u'第十七章狸猫3-1',u'第十四章式神挑战',u'第十章傀儡师1-2',u'第十章觉1-3'])
        newSsrDic.setdefault(u'白狼',[u'御魂八层二回合-1'])
        newSsrDic.setdefault(u'盗墓小鬼',[u'第二章寄生魂2-2',u'第二章帚神-1',u'第二章盗墓小鬼1-1',u'第二章盗墓小鬼2-1',u'第十二章童女1-1',u'第十二章童女2-1',u'第十四章式神挑战'])
        newSsrDic.setdefault(u'童女',[u'御魂二层三回合-2',u'御魂四层一回合-1',u'第三章兵俑1-2',u'第三章天邪鬼黄2-3',u'第三章赤舌2-2',u'第十一章首领-1',u'第十二章式神挑战',u'第十二章童女1-1',u'第十二章童女2-3',u'第十二章童男2-1'])
        newSsrDic.setdefault(u'童男',[u'御魂四层一回合-1',u'第十二章式神挑战',u'第十二章童男1-1',u'第十二章童男2-1'])
        newSsrDic.setdefault(u'管狐',[u'御魂八层一回合-1',u'第七章提灯小僧12-1',u'第七章提灯小僧3-1',u'第七章首领-1',u'第五章管狐1-2',u'第五章管狐2-1',u'第十一章独眼小僧2-1',u'第十一章饿鬼1-2',u'第十一章饿鬼2-1',u'第四章式神挑战'])
        newSsrDic.setdefault(u'茨木童子',[u'御魂八层三回合-2'])
        newSsrDic.setdefault(u'荒川之主',[u'御魂七层三回合-2',u'第十七章首领-1'])
        newSsrDic.setdefault(u'莹草',[u'御魂九层一回合-1',u'御魂十层一回合-1',u'第十七章式神挑战',u'御魂二层二回合-1'])
        newSsrDic.setdefault(u'蝴蝶精',[u'御魂三层一回合-1',u'御魂八层二回合-1',u'第八章首领-2',u'第六章式神挑战',u'第六章蝴蝶精-1'])
        newSsrDic.setdefault(u'觉',[u'御魂十层一回合-1',u'第十一章首领-2',u'第十八章式神挑战',u'第十章傀儡师1-1',u'第十章傀儡师2-1',u'第十章觉1-1',u'第十章觉2-1'])
        newSsrDic.setdefault(u'觉醒火小怪',[u'第十七章狸猫12-3'])
        newSsrDic.setdefault(u'觉醒火小怪',[u'第十七章狸猫3-3'])
        newSsrDic.setdefault(u'觉醒风小怪',[u'第十七章鸦天狗123-3'])
        newSsrDic.setdefault(u'赤舌',[u'第三章赤舌1-1',u'第三章赤舌2-1',u'第十五章天邪鬼绿123-1',u'第十五章提灯小僧12-1',u'第十五章提灯小僧3-1',u'第十六章式神挑战',u'第十六章赤舌13-1',u'第十六章赤舌2-1',u'第十六章赤舌2-1',u'第十章觉2-1'])
        newSsrDic.setdefault(u'跳跳哥哥',[u'妖气封印',u'御魂五层二回合-1',u'第十二章首领-2',u'第十章首领-1'])
        newSsrDic.setdefault(u'跳跳妹妹',[u'第十二章首领-1',u'第十五章式神挑战',u'第十五章首领-1'])
        newSsrDic.setdefault(u'跳跳弟弟',[u'第十五章式神挑战'])
        newSsrDic.setdefault(u'跳跳犬',[u'第一章天邪鬼绿1（困难模式）-2',u'第七章提灯小僧12-3',u'第七章提灯小僧3-1',u'第七章河童2-2'])
        newSsrDic.setdefault(u'酒吞童子',[u'御魂七层二回合-1',u'御魂十层二回合-1',u'第十章首领-1',u'第十章首领-1'])
        newSsrDic.setdefault(u'铁鼠',[u'第三章式神挑战',u'第九章山兔2-1',u'第九章提灯小僧2-2',u'第九章铁鼠1-1',u'第九章铁鼠2-2',u'金币副本'])
        newSsrDic.setdefault(u'镰鼬',[u'御魂五层一回合-1',u'第十八章式神挑战'])
        newSsrDic.setdefault(u'阎魔',[u'御魂六层二回合-1'])
        newSsrDic.setdefault(u'雨女',[u'御魂六层一回合-1',u'第四章式神挑战',u'第四章首领-1'])
        newSsrDic.setdefault(u'雪女',[u'第八章樱花妖1-1',u'第八章樱花妖2-1',u'第十二章童女1-1',u'第十二章童女2-1',u'第十二章首领-1',u'第十二章首领-1'])
        newSsrDic.setdefault(u'青蛙瓷器',[u'御魂三层一回合-1',u'第四章式神挑战',u'第四章首领-1'])
        newSsrDic.setdefault(u'青行灯',[u'御魂十层二回合-1'])
        newSsrDic.setdefault(u'食发鬼',[u'御魂七层一回合-1',u'第五章式神挑战',u'第五章首领-1',u'第十章首领-2'])
        newSsrDic.setdefault(u'食梦貘',[u'御魂九层二回合-1',u'御魂四层三回合-2',u'第十四章涂壁3-1',u'第十四章首领-1',u'第十四章首领-4'])
        newSsrDic.setdefault(u'饿鬼',[u'御魂八层一回合-1',u'第九章首领-3',u'第十一章式神挑战',u'第十一章饿鬼1-1',u'第十一章饿鬼2-3',u'第十三章饿鬼12-1',u'第十三章饿鬼3-1',u'第十六章饿鬼123-1'])
        newSsrDic.setdefault(u'首无',[u'第十三章唐纸伞妖3-1',u'第十三章饿鬼3-1',u'第十三章首领-1'])
        newSsrDic.setdefault(u'骨女',[u'妖气封印',u'御魂五层一回合-1',u'御魂六层三回合-2',u'第十一章首领-1',u'第十七章首领-1',u'第十三章首领-1',u'第十章首领-2'])
        newSsrDic.setdefault(u'鬼使白',[u'御魂四层二回合-1',u'第十六章首领-1'])
        newSsrDic.setdefault(u'鬼使黑',[u'妖气封印',u'御魂四层二回合-1',u'第十六章首领-1'])
        newSsrDic.setdefault(u'鬼女红叶',[u'第十一章首领-1',u'第十一章首领-1'])
        newSsrDic.setdefault(u'鲤鱼精',[u'御魂三层二回合-1',u'御魂九层一回合-1',u'御魂二层一回合-1',u'第七章式神挑战',u'第七章提灯小僧3-2',u'第七章河童1-1',u'第七章鲤鱼精1-3',u'第七章鲤鱼精2-1'])
        newSsrDic.setdefault(u'鸦天狗',[u'御魂六层二回合-1',u'第三章赤舌1-1',u'第三章赤舌2-1',u'第九章山兔1-1',u'第九章山兔2-1',u'第九章首领-2',u'第十七章式神挑战',u'第十七章鸦天狗123-1',u'第十二章海坊主2-2',u'第十二章童男1-2',u'第十二章童男2-2'])
        
        
        if ',' in content or u'，' in content and 'yys' not in content:
            autoReturn = False
            tmpPrint = content.replace(u'，',',')
            tmpList = tmpPrint.split(',')
            list2 = []

            for tmpSs in tmpList:
                if tmpSs not in newSsrDic.keys():
                    autoReturn = True
                    break
            if not autoReturn:
                for i in range(1,len(tmpList) + 1)[::-1]:
                    iter = itertools.combinations(tmpList,i)
                    list2.append(list(iter))
                tmpStr1 = ''
                tmpStr2 = ''
                for tmp1 in list2:
                    tmpStr2 = ''
                    for tmp2 in tmp1:
                        if tmpStr2 != '':
                            tmpStr2 = tmpStr2 + '|'
                        tmpStr2 = tmpStr2 + ','.join(tmp2)
                    if tmpStr1 != '':
                        tmpStr1 = tmpStr1 + '|'
                    tmpStr1 = tmpStr1 + tmpStr2

                allResult = ''
                for tmpGroup in tmpStr1.split('|'):
                    #content=tmpGroup

                    if ',' in tmpGroup:
                        hasSame = False
                        sameResult = ''
                        sameResultList = []
                        hasInit = False
                        for tmpSs in tmpGroup.split(','):
                            if not len(sameResultList) and not hasInit:
                                hasInit = True
                                sameResultList = newSsrDic[tmpSs]
                            else:
                                sameResultList = [val.split('-')[0] for val in sameResultList if val.split('-')[0] in ''.join(newSsrDic[tmpSs])]

                        if len(sameResultList):
                            hasSame = True
                            sameResult = ','.join(sameResultList)


                        if hasSame:                                          
                            if allResult != '':
                                allResult = allResult + '\r\n'
                            allResult = allResult + tmpGroup + ":\r\n" + sameResult
                    else:
                        tmpList = newSsrDic[tmpGroup]
                        tmpMaxCount = 0
                        tmpNoCount = ''
                        tmpReturn = ''
                        for tmp in tmpList:
                            if '-' in tmp:
                                tmpCurrent = int(tmp.split('-')[1])
                                if tmpCurrent > tmpMaxCount:
                                    tmpReturn = tmp.replace('-',u'，可击杀')
                                    tmpMaxCount = tmpCurrent
                                elif tmpCurrent == tmpMaxCount:
                                    tmpReturn = tmpReturn + ';' + tmp.replace('-',u'，可击杀')
                            else:
                                if tmpNoCount == '':
                                    tmpNoCount = tmp
                                else:
                                    tmpNoCount = tmpNoCount + ';' + tmp
                        if tmpNoCount != '':
                            tmpNoCount = tmpNoCount + '\r\n'
                        if allResult != '':
                            allResult = allResult + '\r\n'
                        allResult = allResult + tmpGroup + ":\r\n" + tmpNoCount + tmpReturn
                content = allResult

        elif 'old' in content:
            content = content.replace('old','')
            if content in ssrDic.keys():
                content = ssrDic[content]
                if '-' in content:
                    tmpStr = content.replace('|',u'、').split('-')
                    content = u'第' + tmpStr[0] + u'章' + u' 怪：' + tmpStr[1] + u'，总计可击杀:' + tmpStr[2] + u'个'
                elif 'y' in content:
                    content = content.replace('y',u'御魂') + u'层'
                else:
                    content = content
                autoReturn = False
            else:
                autoReturn = True
        elif 'yys' in content and content != 'yys':
            autoReturn = False
            content = content.replace('yys','')
            
            tmpSs = content.split(u'，')
            tmpZj = ''
            tmpXg = ''
            tmpFy = '' 
            content = ''
            tmpCon = ''
            for tmp in tmpSs:
                if tmp in ssrDic.keys():
                    if tmpZj == '':                        
                        tmpFy = tmp
                        if '-' in ssrDic[tmp]:
                            tmpZj = ssrDic[tmp].split('-')[0]
                            tmpXg = ssrDic[tmp].split('-')[1]
                            tmpStr = ssrDic[tmp].replace('|',u'、').split('-')
                            tmpCon = tmp + u': 第' + tmpStr[0] + u'章' + u' 怪：' + tmpStr[1] + u'，总计可击杀:' + tmpStr[2] + u'个'
                        elif 'y' in ssrDic[tmp]:
                            tmpZj = ssrDic[tmp].replace('y',u'御魂') + u'层'
                            tmpXg = ''
                            tmpCon = tmp + ':' + ssrDic[tmp].replace('y',u'御魂') + u'层'
                        else:
                            tmpZj = ssrDic[tmp]
                            tmpXg = ''
                            tmpCon = tmp + ':' + ssrDic[tmp]
                    elif '-' in ssrDic[tmp] and tmpZj == ssrDic[tmp].split('-')[0]:
                        tmpXgList = [val for val in tmpXg.split('|') if val in ssrDic[tmp].split('-')[1].split('|')]
                        tmpXg = '|'.join(tmpXgList)
                        tmpFy = tmpFy + u'、' + tmp
                    else:
                        if '-' in ssrDic[tmp]:
                            tmpStr = ssrDic[tmp].replace('|',u'、').split('-')
                            content = content + '\r\n' + tmp + u': 第' + tmpStr[0] + u'章' + u' 怪：' + tmpStr[1] + u'，总计可击杀:' + tmpStr[2] + u'个'
                        elif 'y' in ssrDic[tmp]:
                            content = content + '\r\n' + tmp + ':' + ssrDic[tmp].replace('y',u'御魂') + u'层'
                        else:
                            content = content + '\r\n' + tmp + ':' + ssrDic[tmp]
                else:
                    autoReturn = True
            if not autoReturn:
                if u'、' in tmpFy:
                    content = tmpFy + ':' + u'第' + tmpZj + u'章' + u' 怪：' + tmpXg.replace('|',u'、')
                else:
                    content = tmpCon + content
        elif content in newSsrDic.keys():
            autoReturn = False
            content = content.replace('new','')
            if content in newSsrDic.keys():
                tmpList = newSsrDic[content]
                tmpMaxCount = 0
                tmpNoCount = ''
                tmpReturn = ''
                for tmp in tmpList:
                    if '-' in tmp:
                        tmpCurrent = int(tmp.split('-')[1])
                        if tmpCurrent > tmpMaxCount:
                            tmpReturn = tmp.replace('-',u'，可击杀')
                            tmpMaxCount = tmpCurrent
                        elif tmpCurrent == tmpMaxCount:
                            tmpReturn = tmpReturn + ';' + tmp.replace('-',u'，可击杀')
                    else:
                        if tmpNoCount == '':
                            tmpNoCount = tmp
                        else:
                            tmpNoCount = tmpNoCount + ';' + tmp
                if tmpNoCount != '':
                    tmpNoCount = tmpNoCount + '\r\n'
                content = content + ":\r\n" + tmpNoCount + tmpReturn
        elif content in ssrXSDic.keys():
            autoReturn = False
            tmpXsReturn = ssrXSDic[content]
            if tmpXsReturn.split(':')[0] in newSsrDic.keys() and '\r\n' not in tmpXsReturn:
                content = tmpXsReturn.split(':')[0]
                tmpList = newSsrDic[content]
                tmpMaxCount = 0
                tmpNoCount = ''
                tmpReturn = ''
                for tmp in tmpList:
                    if '-' in tmp:
                        tmpCurrent = int(tmp.split('-')[1])
                        if tmpCurrent > tmpMaxCount:
                            tmpReturn = tmp.replace('-',u'，可击杀')
                            tmpMaxCount = tmpCurrent
                        elif tmpCurrent == tmpMaxCount:
                            tmpReturn = tmpReturn + ';' + tmp.replace('-',u'，可击杀')
                    else:
                        if tmpNoCount == '':
                            tmpNoCount = tmp
                        else:
                            tmpNoCount = tmpNoCount + ';' + tmp
                if tmpNoCount != '':
                    tmpNoCount = tmpNoCount + '\r\n'
                content = content + ":\r\n" + tmpNoCount + tmpReturn
                        #content=len(tmpList)
            else:
                content = tmpXsReturn
        
        if autoReturn:
            tmpXS = content.replace(u'探索','').replace(u'是什么','').replace(u'线索','').replace(u'，',',').replace(u'、',',').replace('/',',').replace(' ',',').replace(u' ',',')
            tmpXsList = tmpXS.split(',')
            XsReturn = ''
            for tmpXs in tmpXsList:
                tmpXsReturn = ''
                if tmpXs in ssrXSDic.keys():
                    autoReturn = False
                    tmpXsReturn = ssrXSDic[tmpXs]
                    if XsReturn == '':
                        XsReturn = tmpXsReturn
                if '\r\n' not in tmpXsReturn:
                    if tmpXsReturn.split(':')[0] in newSsrDic.keys():
                        content = tmpXsReturn.split(':')[0]
                        tmpList = newSsrDic[content]
                        tmpMaxCount = 0
                        tmpNoCount = ''
                        tmpReturn = ''
                        for tmp in tmpList:
                            if '-' in tmp:
                                tmpCurrent = int(tmp.split('-')[1])
                                if tmpCurrent > tmpMaxCount:
                                    tmpReturn = tmp.replace('-',u'，可击杀')
                                    tmpMaxCount = tmpCurrent
                                elif tmpCurrent == tmpMaxCount:
                                    tmpReturn = tmpReturn + ';' + tmp.replace('-',u'，可击杀')
                            else:
                                if tmpNoCount == '':
                                    tmpNoCount = tmp
                                else:
                                    tmpNoCount = tmpNoCount + ';' + tmp
                        if tmpNoCount != '':
                            tmpNoCount = tmpNoCount + '\r\n'
                        content = content + ":\r\n" + tmpNoCount + tmpReturn
                        #content=len(tmpList)
                    else:
                        content = tmpXsReturn
                    break
                else:
                    tmpXsReturnLen = len(tmpXsReturn.split('\r\n'))
                    XsReturnLen = len(XsReturn.split('\r\n'))      
                    if tmpXsReturnLen < XsReturnLen:
                        XsReturn = tmpXsReturn
                         

        if autoReturn:
            url = 'http://www.xiaodoubi.com/xiaoiapi.php?msg=' + urllib.quote(content.encode('utf8'), safe='/')
            req_header = {'User-Agent':'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
             'Accept':'text/html;q=0.9,*/*;q=0.8',
             'Accept-Charset':'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
             'Accept-Encoding':'gzip',
             'Connection':'close',
             'Referer':'www.niurenqushi.com' #注意如果依然不能抓取的话，这里可以设置抓取网站的host
             }
        #values = {'':content}
        #data = urllib.urlencode(values)
        #enable cookie
            req = urllib2.Request(url, None)
            response = urllib2.urlopen(req)
            returnstr = response.read()
            if 'Content' in returnstr:
                content = returnstr.split("Content>")[1].split("</")[0]
            else:
            	content = returnstr
        #returnxml = etree.fromstring(returnstr)
        #content=returnxml.find("Content").text
        
        return replytext % (fromUser, toUser, str(int(time.time())), msgType, content)   
        
        
        #return replytext%(fromUser, toUser, str(int(time.time())), msgType,
        #content)
        mc = pylibmc.Client() #初始化一个memcache实例用来保存用户的操作
        #下面创建一个欢迎消息，通过判断Event类型
        if msgType == "event":
            mscontent = xml.find("Event").text
            if mscontent == "subscribe":                
                return replytext % (fromUser, toUser, str(int(time.time())), msgType, u'欢迎关注本微信')
            if mscontent == "unsubscribe":
                return replytext % (fromUser, toUser, str(int(time.time())), msgType, u'我现在功能还很简单，知道满足不了您的需求，但是我会慢慢改进，欢迎您以后再来')
        if msgType == 'text':
            if content.lower() == 'bye':
                mc.delete(fromUser + '_xhj')
                return replytext % (fromUser, toUser, str(int(time.time())), msgType,  u'您已经跳出了和小黄鸡的交谈中，输入help来显示操作指令')
            if content.lower() == 'xhj':
                mc.set(fromUser + '_xhj','xhj')
                return replytext % (fromUser, toUser, str(int(time.time())), msgType, u'您已经进入与小黄鸡的交谈中，请尽情的蹂躏它吧！输入bye跳出与小黄鸡的交谈')
                
                
            mcxhj = mc.get(fromUser + '_xhj')
            if mcxhj == 'xhj':
                #return replytext % (fromUser, toUser, str(int(time.time())),
                #msgType, u"小黄鸡脑袋出问题了，请换个问题吧~")
                url = 'http://www.xiaodoubi.com/xiaoiapi.php?msg=' + content
                req_header = {'User-Agent':'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
             'Accept':'text/html;q=0.9,*/*;q=0.8',
             'Accept-Charset':'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
             'Accept-Encoding':'gzip',
             'Connection':'close',
             'Referer':'www.niurenqushi.com' #注意如果依然不能抓取的话，这里可以设置抓取网站的host
             }
                values = {'txt':content}
                data = urllib.urlencode(values)
                #enable cookie
                req = urllib2.Request(url, None)
                response = urllib2.urlopen(req)
                returnstr = "<" + response.read() + ">"
                returnxml = etree.fromstring(returnstr)
                content = returnxml.find("Content").text
                return replytext % (fromUser, toUser, str(int(time.time())), msgType, content)   

            if content.lower() == 'help':
                return replytext % (fromUser, toUser, str(int(time.time())), msgType,u'输入xhj进入调戏小黄鸡模式')
            if type(content).__name__ == "unicode":
                content = content.encode('UTF-8')

        #return replytext%(fromUser, toUser, str(int(time.time())), msgType, content)        
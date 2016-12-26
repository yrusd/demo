#coding=utf-8

#version

from PyQt4.QtGui import *
from PyQt4.QtCore import *
import urllib.request  
import urllib.parse  
import re  
import urllib.request
import urllib.parse
import http.cookiejar  
import time  
import os
import json
import sys
import win32con
import ctypes 
from ctypes import wintypes

ISOTIMEFORMAT = '%Y-%m-%d %X'
JUSTTIME = '%X'


global shenzhen,shanghai,stock,code,initcode,initInfo,initCheckBox,wantWarning,hasMessage,isRunning,isMainHide,isRefresh
shenzhen = ''
shanghai = ''
stock = ''
code = ''
initcode = ''
initInfo = ''
initCheckBox = ''
wantWarning = True
hasMessage = False
isRunning = False  
isMainHide = True
isRefresh = False

class WorkThread(QThread):
    trigger = pyqtSignal()
    def __int__(self):
        super(WorkThread,self).__init__()

    def getHtml(self,url): 
      
        cj = http.cookiejar.CookieJar()  
        opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(cj))  
        opener.addheaders = [('User-Agent','Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2272.101 Safari/537.36'),('Cookie','4564564564564564565646540'),('apikey','d537c2a89195597876e920678da7d066')]  
  
        urllib.request.install_opener(opener)  
      
        page = urllib.request.urlopen(url)  
        html = page.read().decode('GBK')
        return html  

    def GetContext(self,context,param):
        result = ''    
        for s in str(param).split('/'):
            result = result + '' + str(context[s]) + ','
        return result

    def run(self):
        global shenzhen,shanghai,stock,code,isRefresh
        while 1:         
            #html = self.getHtml('http://hq.sinajs.cn/list=' + code +
            #'s_sh000001,s_sz399001')
            html = self.getHtml('http://1.nofat1.applinzi.com/stock?code=' + code + 's_sh000001,s_sz399001')
            eachCode = code[:-1].split(',')
            eachInfo = html.split(';')
            print(eachInfo)
            stock = ''
            for i in range(len(eachCode)):
                info = eachInfo[i].split('"')[1].split(',')
                #name/code/date/time/currentPrice/hPrice/lPrice/OpenningPrice/closingPrice
                stock = stock + info[0] + ',' + eachCode[i] + ',' + info[30] + ',' + info[31] + ',' + info[3] + ',' + info[4] + ',' + info[5] + ',' + info[1] + ',' + info[2] + ','
            stock = stock[:-1]
            shanghai = eachInfo[len(eachInfo) - 3].split('"')[1]
            shenzhen = eachInfo[len(eachInfo) - 2].split('"')[1] 
            time.sleep(100) 
            isRefresh = True
        self.trigger.emit() 

class hotKeyThread(QThread):
    def __int__(self):
        super(hotKeyThread,self).__init__()

    def run(self):
        byref = ctypes.byref
        user32 = ctypes.windll.user32  
        HOTKEYS = {  
                       1 : (win32con.VK_F1, win32con.MOD_CONTROL),
                       2 : (win32con.VK_F2, win32con.MOD_CONTROL),
                       3 : (win32con.VK_F3, win32con.MOD_CONTROL),
                       4 : (win32con.VK_F4, win32con.MOD_CONTROL)
                       }
        HOTKEY_ACTIONS = {  
                1 : dialog.restoreAction.trigger,
                2:dialog.startAction.trigger,
                #2 : work,
                3 : dialog.warningAction.trigger,
                4 : dialog.quitAction.trigger#dialog.quit
                }   
        for id, (vk, modifiers) in HOTKEYS.items():  
            if not user32.RegisterHotKey(None, id, modifiers, vk):
                print("Unable to register id", id)
        msg = wintypes.MSG()  
        while user32.GetMessageA(byref(msg), None, 0, 0) != 0:  
            if msg.message == win32con.WM_HOTKEY:  
                action_to_take = HOTKEY_ACTIONS.get(msg.wParam)  
                if action_to_take:  
                    action_to_take()

def countTime():
    global shenzhen,shanghai,stock,code,initCode,initInfo,wantWarning,hasMessage,isRefresh
    dialog.indexLabel.setText(str(shanghai + '\n' + shenzhen))
    stockArr = stock.split(',')
    total = len(stock.split(','))
    num = 0
    rowcount = 0
    while rowcount < len(code.split(',')):
        for j in range(9):
            if num < total:
                cnt = stockArr[num]
                newItem = QTableWidgetItem(cnt)
                dialog.table.setItem(rowcount,j,newItem)
                num = num + 1        
        if  dialog.table.item(rowcount,4) and dialog.table.item(rowcount,8):
            if float(dialog.table.item(rowcount,4).text()) > float(dialog.table.item(rowcount,8).text()):
                cnt = stockArr[4 + rowcount * 9]
                newItem = QTableWidgetItem(cnt)
                newItem.setTextColor(QColor(255,0,0))
                dialog.table.setItem(rowcount,4,newItem)
            elif float(dialog.table.item(rowcount,4).text()) < float(dialog.table.item(rowcount,8).text()):
                cnt = stockArr[4 + rowcount * 9]
                newItem = QTableWidgetItem(cnt)
                newItem.setTextColor(QColor(0,255,0))
                dialog.table.setItem(rowcount,4,newItem)
            elif float(dialog.table.item(rowcount,4).text()) == float(dialog.table.item(rowcount,8).text()):
                cnt = stockArr[4 + rowcount * 9]
                newItem = QTableWidgetItem(cnt)
                newItem.setTextColor(QColor(0,0,0))
                dialog.table.setItem(rowcount,4,newItem)
        if dialog.table.item(rowcount,4) and dialog.table.item(rowcount,8) and dialog.table.item(rowcount,8).text() != "0":
            rate = float(dialog.table.item(rowcount,4).text()) / float(dialog.table.item(rowcount,8).text()) - 1
            rate = round(rate * 100,2)            
            if rate > 0:
                newItem = QTableWidgetItem(str(rate))
                newItem.setTextColor(QColor(255,0,0))
                dialog.table.setItem(rowcount,9,newItem)
            elif rate < 0:
                newItem = QTableWidgetItem(str(rate))
                newItem.setTextColor(QColor(0,255,0))
                dialog.table.setItem(rowcount,9,newItem)
            elif rate == 0:
                newItem = QTableWidgetItem(str(rate))
                newItem.setTextColor(QColor(0,0,0))
                dialog.table.setItem(rowcount,9,newItem)
        rowcount = rowcount + 1
    initCount = 0
    initStock = initInfo.split('|')
    trayTip = ''
    message = ''
    msgCount = 1
    if initcode != '':
        while initCount < len(initcode.rstrip(',').split(',')):
            cnt = initStock[initCount].split(',')[3]
            newItem = QTableWidgetItem(cnt)
            dialog.table.setItem(initCount,10,newItem)
            cnt = initStock[initCount].split(',')[1]
            newItem = QTableWidgetItem(cnt)
            dialog.table.setItem(initCount,11,newItem)
            cnt = initStock[initCount].split(',')[2]
            newItem = QTableWidgetItem(cnt)
            dialog.table.setItem(initCount,12,newItem)

            #set cost markVal
            if dialog.table.item(initCount,12) and dialog.table.item(initCount,12).text() != '':
                if dialog.table.item(initCount,4) and dialog.table.item(initCount,4).text() != '':
                    cnt = round(float(dialog.table.item(initCount,4).text()) * float(dialog.table.item(initCount,12).text()),2)
                    newItem = QTableWidgetItem(str(cnt))
                    dialog.table.setItem(initCount,14,newItem)
                if dialog.table.item(initCount,11) and dialog.table.item(initCount,11).text() != '':
                    cnt = round(float(dialog.table.item(initCount,11).text()) * float(dialog.table.item(initCount,12).text()),2)
                    newItem = QTableWidgetItem(str(cnt))
                    dialog.table.setItem(initCount,13,newItem)       
                    
            #set fuYing
            if dialog.table.item(initCount,14) and dialog.table.item(initCount,14).text() != '':
                if dialog.table.item(initCount,13) and dialog.table.item(initCount,13).text() != '':
                    cnt = round(float(dialog.table.item(initCount,14).text()) - float(dialog.table.item(initCount,13).text()),2)
                    if cnt > 0:
                        newItem = QTableWidgetItem(str(cnt))
                        newItem.setTextColor(QColor(255,0,0))
                        dialog.table.setItem(initCount,15,newItem)
                    elif cnt < 0:
                        newItem = QTableWidgetItem(str(cnt))
                        newItem.setTextColor(QColor(0,255,0))
                        dialog.table.setItem(initCount,15,newItem)
                    elif cnt == 0:
                        newItem = QTableWidgetItem(str(cnt))
                        newItem.setTextColor(QColor(0,0,0))
                        dialog.table.setItem(initCount,15,newItem)

            #message
            if dialog.table.item(initCount,1) and dialog.table.item(initCount,4) and dialog.table.item(initCount,4).text() != '' and wantWarning :#and hasMessage==False:
                curPri = dialog.table.item(initCount,4).text()
                warning = str(dialog.table.item(initCount,8).text() + '-' + dialog.table.item(initCount,8).text()).split('-')   if dialog.table.item(initCount,10) or dialog.table.item(initCount,10).text() == ''  else dialog.table.item(initCount,10).text().split('-')
                if len(warning) == 2:
                    if warning[0] != '' and float(curPri) >= float(warning[0]):
                        hasMessage = True
                        message = message + str(dialog.table.item(initCount,1).text() + '↑' + curPri + '↑' + warning[0] + '↑' + dialog.table.item(initCount,9).text() + '↑') + '\n'
                        msgCount+=1
                    if warning[1] != '' and float(curPri) < float(warning[1]):
                        hasMessage = True
                        message = message + str(dialog.table.item(initCount,1).text() + '↓' + curPri + '↓' + warning[1] + '↓' + dialog.table.item(initCount,9).text() + '↓') + '\n'
                        msgCount+=1
                else:
                    if warning[0] != '' and float(curPri) >= float(warning[0]):
                        hasMessage = True
                        message = message + str(dialog.table.item(initCount,1).text() + '↑' + curPri + '↑' + warning[0] + '↑' + dialog.table.item(initCount,9).text() + '↑') + '\n'
                        msgCount+=1
            if dialog.table.item(initCount,4) and dialog.table.item(initCount,4).text():
                trayTip = trayTip + dialog.table.item(initCount,4).text() + '\n'
            initCount = initCount + 1
    if message != '' and isRefresh:
        tmpSZ = shanghai.split(',')
        messageBox(time.strftime(JUSTTIME, time.localtime()) + ' ' + tmpSZ[1] + ',' + tmpSZ[3] + '\n' + message,msgCount).show()
        isRefresh = False
    dialog.trayIcon.setToolTip(trayTip)
    dialog.timeLabel.setText(time.strftime(ISOTIMEFORMAT, time.localtime()))
    dialog.table.repaint()    

def work():
    global shenzhen,shanghai,stock,code,initcode,isRunning
    c = initcode + dialog.lineEdit.text()
    c = c.rstrip(',')
    dialog.table.clearContents()
    code = ''
    for s in c.split(','):
        code = code + 'sh' + s + ',' if s.startswith('60') else code + 'sz' + s + ','
    workThread.start()    
    isRunning = not isRunning
    workThread.isRunning = isRunning  
    timer.start(1000) if isRunning else timer.stop()      
    dialog.startAction.setIcon(QIcon("images/start.png") if not isRunning else QIcon("images/pause.png"))
    dialog.startAction.setText('start' if not isRunning else 'pause')
    dialog.execButton.setText('start' if not isRunning else 'pause')
    #workThread.trigger.connect(timeStop)
def timeStop():
    workThread.run()

class labelBtn(QLabel):
    """
    自定义图片按钮类
    """
    def __init__(self,ID):
        super(QLabel, self).__init__()
        self.setMouseTracking(True)
        self.ID = ID
   
    def mouseReleaseEvent(self,event):  #注:
        #鼠标点击事件
        self.parent().parent().btnHandle(self.ID)
   
    def enterEvent(self,event):
        #鼠标进入时间
        self.parent().parent().btnEnter(self.ID)
   
    def leaveEvent(self,event):
        #鼠标离开事件
        self.parent().parent().btnLeave(self.ID)

class mainWidget(QMainWindow):
    def __init__(self,parent=None):
        QMainWindow.__init__(self,parent)
        self.initCofig()
        global initcode,initInfo,initCheckBox


        #if os.path.exists(os.getcwd() + '\\config\\initCode.ini'):
        #    initcode = str(open(os.getcwd() +
        #    '\\config\\initCode.ini',mode="r",encoding="UTF-8").read())
        #if os.path.exists(os.getcwd() + '\\config\\initInfo.ini'):
        #    initInfo = str(open(os.getcwd() +
        #    '\\config\\initInfo.ini',mode="r",encoding="UTF-8").read())

        self.timeLabel = QLabel()
        self.pe = QPalette()
        self.pe.setColor(QPalette.WindowText,QColor(255,255,255))
        self.timeLabel.setPalette(self.pe)
        self.timeLabel.setText(time.strftime(ISOTIMEFORMAT, time.localtime()))
        self.descriptLabel = QLabel('input code ,split with comma like \',\'')
        self.descriptLabel.setPalette(self.pe)
        self.lineEdit = QLineEdit()
        self.execButton = QPushButton('start') 
        self.initButton = QPushButton('init')
        self.connect(self.initButton,SIGNAL("clicked()"),self.FontModalessDialog)
        
        self.nameCheckBox = QCheckBox('name')
        self.nameCheckBox.setPalette(self.pe)
        self.nameCheckBox.setChecked(True)
        self.nameCheckBox.connect(self.nameCheckBox,SIGNAL('clicked()'),self.setHideOrShow)
        self.codeCheckBox = QCheckBox('code')
        self.codeCheckBox.setPalette(self.pe)
        self.codeCheckBox.setChecked(True)
        self.codeCheckBox.connect(self.codeCheckBox,SIGNAL('clicked()'),self.setHideOrShow)
        self.dateCheckBox = QCheckBox('date')
        self.dateCheckBox.setPalette(self.pe)
        self.dateCheckBox.setChecked(True)
        self.dateCheckBox.connect(self.dateCheckBox,SIGNAL('clicked()'),self.setHideOrShow)
        self.timeCheckBox = QCheckBox('time')
        self.timeCheckBox.setPalette(self.pe)
        self.timeCheckBox.setChecked(True)
        self.timeCheckBox.connect(self.timeCheckBox,SIGNAL('clicked()'),self.setHideOrShow)
        self.currentPriceCheckBox = QCheckBox('currentPrice')
        self.currentPriceCheckBox.setPalette(self.pe)
        self.currentPriceCheckBox.setChecked(True)
        self.currentPriceCheckBox.connect(self.currentPriceCheckBox,SIGNAL('clicked()'),self.setHideOrShow)
        self.hPriceCheckBox = QCheckBox('hPrice')
        self.hPriceCheckBox.setPalette(self.pe)
        self.hPriceCheckBox.setChecked(True)
        self.hPriceCheckBox.connect(self.hPriceCheckBox,SIGNAL('clicked()'),self.setHideOrShow)
        self.lPriceCheckBox = QCheckBox('lPrice')
        self.lPriceCheckBox.setPalette(self.pe)
        self.lPriceCheckBox.setChecked(True)
        self.lPriceCheckBox.connect(self.lPriceCheckBox,SIGNAL('clicked()'),self.setHideOrShow)
        self.OpenningPriceCheckBox = QCheckBox('OpenningPrice')
        self.OpenningPriceCheckBox.setPalette(self.pe)
        self.OpenningPriceCheckBox.setChecked(True)
        self.OpenningPriceCheckBox.connect(self.OpenningPriceCheckBox,SIGNAL('clicked()'),self.setHideOrShow)
        self.closingPriceCheckBox = QCheckBox('closingPrice')
        self.closingPriceCheckBox.setPalette(self.pe)    
        self.closingPriceCheckBox.setChecked(True)
        self.closingPriceCheckBox.connect(self.closingPriceCheckBox,SIGNAL('clicked()'),self.setHideOrShow) 
        self.RateCheckBox = QCheckBox('Rate')
        self.RateCheckBox.setPalette(self.pe)    
        self.RateCheckBox.setChecked(True)
        self.RateCheckBox.connect(self.RateCheckBox,SIGNAL('clicked()'),self.setHideOrShow)  
        self.Warning = QCheckBox('Warning')
        self.Warning.setPalette(self.pe)    
        self.Warning.setChecked(True)
        self.Warning.connect(self.Warning,SIGNAL('clicked()'),self.setHideOrShow)  
        self.bidPri = QCheckBox('bidPri')
        self.bidPri.setPalette(self.pe)    
        self.bidPri.setChecked(True)
        self.bidPri.connect(self.bidPri,SIGNAL('clicked()'),self.setHideOrShow) 
        self.Volume = QCheckBox('Volume')
        self.Volume.setPalette(self.pe)    
        self.Volume.setChecked(True)
        self.Volume.connect(self.Volume,SIGNAL('clicked()'),self.setHideOrShow) 
        self.Cost = QCheckBox('Cost')
        self.Cost.setPalette(self.pe)    
        self.Cost.setChecked(True)
        self.Cost.connect(self.Cost,SIGNAL('clicked()'),self.setHideOrShow) 
        self.markVal = QCheckBox('markVal')
        self.markVal.setPalette(self.pe)    
        self.markVal.setChecked(True)
        self.markVal.connect(self.markVal,SIGNAL('clicked()'),self.setHideOrShow)    
        self.fuYing = QCheckBox('fuYing') 
        self.fuYing.setPalette(self.pe)    
        self.fuYing.setChecked(True)
        self.fuYing.connect(self.fuYing,SIGNAL('clicked()'),self.setHideOrShow)     
        
        checkBoxConfig = initCheckBox.split(',')
        if(len(checkBoxConfig) == 17):
            self.nameCheckBox.setChecked(checkBoxConfig[0] == 'True')
            self.codeCheckBox.setChecked(checkBoxConfig[1] == 'True')
            self.dateCheckBox.setChecked(checkBoxConfig[2] == 'True')
            self.timeCheckBox.setChecked(checkBoxConfig[3] == 'True')
            self.currentPriceCheckBox.setChecked(checkBoxConfig[4] == 'True')
            self.hPriceCheckBox.setChecked(checkBoxConfig[5] == 'True')
            self.lPriceCheckBox.setChecked(checkBoxConfig[6] == 'True')
            self.OpenningPriceCheckBox.setChecked(checkBoxConfig[7] == 'True')
            self.closingPriceCheckBox.setChecked(checkBoxConfig[8] == 'True')
            self.RateCheckBox.setChecked(checkBoxConfig[9] == 'True')
            self.Warning.setChecked(checkBoxConfig[10] == 'True')
            self.bidPri.setChecked(checkBoxConfig[11] == 'True')
            self.Volume.setChecked(checkBoxConfig[12] == 'True')
            self.Cost.setChecked(checkBoxConfig[13] == 'True')
            self.markVal.setChecked(checkBoxConfig[14] == 'True')
            self.fuYing.setChecked(checkBoxConfig[15] == 'True')

        self.indexLabel = QLabel()
        self.indexLabel.setPalette(self.pe)
        self.table = QTableWidget(10,16)
        self.table.setHorizontalHeaderLabels(['name','code','date','time','currentPrice','hPrice','lPrice','OpenningPrice','closingPrice','Rate','Warning','bidPri','Volume','Cost','markVal','fuYing'])        
        self.table.verticalHeader().setVisible(False)
        self.table.setEditTriggers(QTableWidget.NoEditTriggers)
        self.table.setAlternatingRowColors(True)           
        
        self.btn_min = labelBtn(1)               #定义最小化按钮 ID:1
        self.btn_min.setParent(self)
        self.btn_min.setGeometry(884,0,16,16)
        self.btn_min.setToolTip(u"minimize") 
     
        self.btn_close = labelBtn(2)              #定义关闭按钮 ID:2
        self.btn_close.setParent(self)
        self.btn_close.setGeometry(911,0,16,16)
        self.btn_close.setToolTip(u"close")   
        
        self.btn_min.setPixmap(QPixmap(os.getcwd() + '/images/min2.png'))
        self.btn_close.setPixmap(QPixmap(os.getcwd() + '/images/close2.png'))   

        #self.btn_min.setIcon(QIcon(os.getcwd() + '/images/min2.png'))
        #self.btn_min.setIconSize(QSize(12,12))
        #self.btn_close.setIcon(QIcon(os.getcwd() + '/images/close2.png'))
        #self.btn_close.setIconSize(QSize(12,12))
        
        self.topLayout = QHBoxLayout()
        self.topLayout.addWidget(self.timeLabel,1)     
        self.topLayout.addWidget(self.btn_min)
        self.topLayout.addWidget(self.btn_close)

        self.horLayout = QHBoxLayout()
        self.horLayout.addWidget(self.descriptLabel)
        self.horLayout.addWidget(self.lineEdit)
        self.horLayout.addWidget(self.execButton)
        self.horLayout.addWidget(self.initButton)

        self.midLayout = QHBoxLayout()
        self.midLayout.addWidget(self.nameCheckBox)
        self.midLayout.addWidget(self.codeCheckBox)
        self.midLayout.addWidget(self.dateCheckBox)
        self.midLayout.addWidget(self.timeCheckBox)
        self.midLayout.addWidget(self.currentPriceCheckBox)
        self.midLayout.addWidget(self.hPriceCheckBox)
        self.midLayout.addWidget(self.lPriceCheckBox)
        self.midLayout.addWidget(self.OpenningPriceCheckBox)
        self.midLayout.addWidget(self.closingPriceCheckBox)
        self.midLayout.addWidget(self.RateCheckBox)
        self.midLayout.addWidget(self.Warning)
        self.midLayout.addWidget(self.bidPri)
        self.midLayout.addWidget(self.Volume)
        self.midLayout.addWidget(self.Cost)
        self.midLayout.addWidget(self.markVal)
        self.midLayout.addWidget(self.fuYing)

        self.varLayout = QVBoxLayout()
        self.varLayout.addWidget(self.indexLabel)
        self.varLayout.addWidget(self.table)

        self.layout = QVBoxLayout()
        #self.layout.addWidget(self.timeLabel)
        self.layout.addLayout(self.topLayout)
        self.layout.addLayout(self.horLayout)
        self.layout.addLayout(self.midLayout)
        self.layout.addLayout(self.varLayout)

        self.widget = QWidget()
        self.widget.setLayout(self.layout)
        self.setCentralWidget(self.widget)
        self.setWindowTitle('stock v1.2')
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
        #self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint |
        #Qt.Tool | Qt.Popup)

        self.icon = QIcon()
        self.icon.addPixmap(QPixmap(os.getcwd() + '/images/icon.png'), QIcon.Normal, QIcon.Off)
        self.setWindowIcon(self.icon)
        self.trayIcon = QSystemTrayIcon(self)
        self.trayIcon.setIcon(self.icon)
        self.trayIcon.show()
        self.trayIcon.activated.connect(self.trayClick)
        self.trayMenu()  

        self.setAutoFillBackground(True)
        self.palette = QPalette()
        self.palette.setBrush(QPalette.Background,QBrush(QPixmap(os.getcwd() + '/images/background.png')))
        self.setPalette(self.palette)   
        
        self.setHideOrShow() 

    def initCofig(self):
        global initcode,initInfo,initCheckBox

        if os.path.exists(os.getcwd() + '\\config\\initCode.ini'):
            initcode = str(open(os.getcwd() + '\\config\\initCode.ini',mode="r",encoding="UTF-8").read())
        if os.path.exists(os.getcwd() + '\\config\\initInfo.ini'):
            initInfo = str(open(os.getcwd() + '\\config\\initInfo.ini',mode="r",encoding="UTF-8").read())
        if os.path.exists(os.getcwd() + '\\config\\initCheckBox.ini'):
            initCheckBox = str(open(os.getcwd() + '\\config\\initCheckBox.ini',mode="r",encoding="UTF-8").read())

    def  setHideOrShow(self):
        global wantWarning
        if (self.nameCheckBox.isChecked()):
            self.table.showColumn(0)  
        else :
            self.table.hideColumn(0)  
        if (self.codeCheckBox.isChecked()):
            self.table.showColumn(1)  
        else :
            self.table.hideColumn(1)
        if (self.dateCheckBox.isChecked()):
            self.table.showColumn(2)  
        else :
            self.table.hideColumn(2)
        if (self.timeCheckBox.isChecked()):
            self.table.showColumn(3)  
        else :
            self.table.hideColumn(3)
        if (self.currentPriceCheckBox.isChecked()):
            self.table.showColumn(4)  
        else :
            self.table.hideColumn(4)
        if (self.hPriceCheckBox.isChecked()):
            self.table.showColumn(5)  
        else :
            self.table.hideColumn(5)
        if (self.lPriceCheckBox.isChecked()):
            self.table.showColumn(6)  
        else :
            self.table.hideColumn(6)
        if (self.OpenningPriceCheckBox.isChecked()):
            self.table.showColumn(7)  
        else :
            self.table.hideColumn(7)
        if (self.closingPriceCheckBox.isChecked()):
            self.table.showColumn(8)  
        else :
            self.table.hideColumn(8)
        if (self.RateCheckBox.isChecked()):
            self.table.showColumn(9)  
        else :
            self.table.hideColumn(9)
        if (self.Warning.isChecked()):
            self.table.showColumn(10)  
            wantWarning = True
            self.warn(2)
        else :
            self.table.hideColumn(10)
            wantWarning = False
            self.warn(2)
        if (self.bidPri.isChecked()):
            self.table.showColumn(11)  
        else :
            self.table.hideColumn(11)
        if (self.Volume.isChecked()):
            self.table.showColumn(12)  
        else :
            self.table.hideColumn(12)
        if (self.Cost.isChecked()):
            self.table.showColumn(13)  
        else :
            self.table.hideColumn(13)
        if (self.markVal.isChecked()):
            self.table.showColumn(14)  
        else :
            self.table.hideColumn(14)
        if (self.fuYing.isChecked()):
            self.table.showColumn(15)  
        else :
            self.table.hideColumn(15)

    def setInitCheckBox(self):
        global initCheckBox
        initCheckBox = ''
        initCheckBox = initCheckBox + str('True' if self.nameCheckBox.isChecked() else 'False') + ','
        initCheckBox = initCheckBox + str('True' if self.codeCheckBox.isChecked() else 'False') + ','
        initCheckBox = initCheckBox + str('True' if self.dateCheckBox.isChecked() else 'False') + ','
        initCheckBox = initCheckBox + str('True' if self.timeCheckBox.isChecked() else 'False') + ','
        initCheckBox = initCheckBox + str('True' if self.currentPriceCheckBox.isChecked() else 'False') + ','
        initCheckBox = initCheckBox + str('True' if self.hPriceCheckBox.isChecked() else 'False') + ','
        initCheckBox = initCheckBox + str('True' if self.lPriceCheckBox.isChecked() else 'False') + ','
        initCheckBox = initCheckBox + str('True' if self.OpenningPriceCheckBox.isChecked() else 'False') + ','
        initCheckBox = initCheckBox + str('True' if self.closingPriceCheckBox.isChecked() else 'False') + ','
        initCheckBox = initCheckBox + str('True' if self.RateCheckBox.isChecked() else 'False') + ','
        initCheckBox = initCheckBox + str('True' if self.Warning.isChecked() else 'False') + ','
        initCheckBox = initCheckBox + str('True' if self.bidPri.isChecked() else 'False') + ','
        initCheckBox = initCheckBox + str('True' if self.Volume.isChecked() else 'False') + ','
        initCheckBox = initCheckBox + str('True' if self.Cost.isChecked() else 'False') + ','
        initCheckBox = initCheckBox + str('True' if self.markVal.isChecked() else 'False') + ','
        initCheckBox = initCheckBox + str('True' if self.fuYing.isChecked() else 'False') + ','

        file_object = open(os.getcwd() + '\\config\\initCheckBox.ini',mode="w",encoding="UTF-8")
        file_object.writelines(initCheckBox)
        file_object.flush() 
        file_object.close()

    def FontModalessDialog(self):
        dialog = initDialog(self)
        dialog.setModal(False)
        if dialog.show():
            pass

    def trayClick(self,reason):
       #双击托盘
       if reason == QSystemTrayIcon.DoubleClick:
           self.mainHideOrShow()
       else:
           pass

    def trayMenu(self):
       #右击托盘弹出的菜单
       img_main = QIcon("images/main.png")
       img_warning = QIcon("images/false.png")
       img_start = QIcon("images/start.png")
       img_exit = QIcon("images/exit.png")
       
       self.trayIcon.setToolTip(u"stock v1.2")

       self.restoreAction = QAction(img_main,u"open main", self)
       self.restoreAction.setShortcut('CTRL+F1')
       self.restoreAction.triggered.connect(self.mainHideOrShow)
       self.startAction = QAction(img_start,'start',self)
       self.startAction.setShortcut('CTRL+F2')
       self.startAction.triggered.connect(work)       
       self.warningAction = QAction(img_warning,'warning',self)
       self.warningAction.setShortcut('CTRL+F3')
       self.warningAction.triggered.connect(self.warn)
       self.quitAction = QAction(img_exit,u"exit", self)
       self.quitAction.setShortcut('CTRL+F4')
       self.quitAction.triggered.connect(self.quit)
       
       self.trayIconMenu = QMenu(self)
       self.trayIconMenu.addAction(self.restoreAction)       
       self.trayIconMenu.addSeparator()
       self.trayIconMenu.addAction(self.startAction)
       self.trayIconMenu.addSeparator()
       self.trayIconMenu.addAction(self.warningAction)
       self.trayIconMenu.addSeparator()
       self.trayIconMenu.addAction(self.quitAction)
       self.trayIcon.setContextMenu(self.trayIconMenu)

    def mainHideOrShow(self):
        global isMainHide
        isMainHide = not isMainHide
        self.restoreAction.setText('open main' if isMainHide else 'hide main')
        if isMainHide:
            self.hide()
        else:
            self.showNormal()

    def quit(self):
        self.setInitCheckBox()
        self.trayIcon.hide()
        sys.exit()

    def warn(self,ID):
        global wantWarning
        #ID 1:托盘点击 2：复选框点击
        if ID != 2:
            wantWarning = False if wantWarning else True 
            self.Warning.setChecked(wantWarning)
            if (self.Warning.isChecked()):
                self.table.showColumn(10)  
            else :
                self.table.hideColumn(10)   
              
        img_warning = QIcon("images/false.png") if wantWarning else QIcon("images/true.png")
        self.warningAction.setIcon(img_warning)  

        #支持窗口拖动,重写两个方法
    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.m_drag = True
            self.m_DragPosition = event.globalPos() - self.pos()
            event.accept()            
 
    def mouseMoveEvent(self, QMouseEvent):
        if QMouseEvent.buttons() and Qt.LeftButton:
            self.move(QMouseEvent.globalPos() - self.m_DragPosition)
            QMouseEvent.accept()
 
    def mouseReleaseEvent(self, QMouseEvent):
        self.m_drag = False  

    def btnHandle(self,ID):
        #最小化
        if ID == 1:
            #self.hide()
            self.mainHideOrShow()
            #self.showMinimized()
        elif ID == 2:
           #关闭
            self.quit()
                      
    def btnEnter(self,ID):
       #鼠标进入
       if ID == 1:
           self.btn_min.setPixmap(QPixmap(os.getcwd() + '/images/min.png'))
       elif ID == 2:
           self.btn_close.setPixmap(QPixmap(os.getcwd() + '/images/close.png'))
 
    def btnLeave(self,ID):
       #鼠标离开
       '''false.png这张图片是不存在的，目的是要在鼠标
        离开后还原背景，因为默认按钮我已经PS在背景上了'''
       self.btn_min.setPixmap(QPixmap(os.getcwd() + '/images/min2.png'))
       self.btn_close.setPixmap(QPixmap(os.getcwd() + '/images/close2.png'))

class initDialog(QDialog):
    def __init__(self,parent=None):
        super(initDialog,self).__init__(parent)
        
        global initInfo

        self.initTable = QTableWidget(4,4)
        self.initTable.setHorizontalHeaderLabels(['code','bidPri','Volume','Warning'])
        self.initTable.verticalHeader().setVisible(False)
        self.initTable.setAlternatingRowColors(True)

        if initInfo != '':
            eachInfo = initInfo.split('|')
            rowcount = 0
            while rowcount < len(initInfo.split('|')):
                if eachInfo[rowcount] != '':
                    info = eachInfo[rowcount].split(',')
                    for j in range(len(info)):            
                        cnt = info[j]
                        newItem = QTableWidgetItem(cnt)
                        self.initTable.setItem(rowcount,j,newItem)
                rowcount = rowcount + 1

        self.submitButton = QPushButton('Submit')
        self.quitButton = QPushButton('Quit')
        self.connect(self.submitButton,SIGNAL("clicked()"),self.submit)
        self.connect(self.quitButton,SIGNAL("clicked()"),self,SLOT("close()"))

        self.horLayout = QHBoxLayout()
        self.horLayout.addWidget(self.submitButton)
        self.horLayout.addWidget(self.quitButton)

        self.varLayout = QVBoxLayout()
        self.varLayout.addWidget(self.initTable)        
        self.varLayout.addLayout(self.horLayout)

        self.setLayout(self.varLayout)
        self.setWindowTitle('stock v1.2 init ')

        self.icon = QIcon()
        self.icon.addPixmap(QPixmap(os.getcwd() + '/images/icon.png'), QIcon.Normal, QIcon.Off)
        self.setWindowIcon(self.icon)
        #self.trayIcon = QSystemTrayIcon(self)
        #self.trayIcon.setIcon(self.icon)

        self.setAutoFillBackground(True)
        self.palette = QPalette()
        self.palette.setBrush(QPalette.Background,QBrush(QPixmap(os.getcwd() + '/images/background.png')))
        self.setPalette(self.palette)  
        self.setFixedSize(400, 240)
        #self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
        #self.setWindowFlags(Qt.FramelessWindowHint)
        self.setWindowFlags(Qt.Tool | Qt.Popup)

    def submit(self):
        global initcode,initInfo
        initcode = ''
        initInfo = ''
        for i in range(self.initTable.rowCount()):
            if self.initTable.item(i,0) and self.initTable.item(i,0).text() != '' :
                initcode = initcode + self.initTable.item(i,0).text() + ','
                for j in range(self.initTable.columnCount()):
                    if self.initTable.item(i,j):
                        initInfo = initInfo + self.initTable.item(i,j).text() + ','
                    else:
                        initInfo = initInfo + ','
                initInfo = initInfo[:-1] + '|'

        if os.path.exists(os.getcwd() + '\\config') == False:
            os.makedirs(os.getcwd() + '\\config')
        file_object = open(os.getcwd() + '\\config\\initCode.ini',mode="w",encoding="UTF-8")
        file_object.writelines(initcode)
        file_object.flush() 
        file_object.close()
        file_object = open(os.getcwd() + '\\config\\initInfo.ini',mode="w",encoding="UTF-8")
        file_object.writelines(initInfo)
        file_object.flush() 
        file_object.close()

        self.accept()

class messageBox(QDialog):
    def __init__(self,message,i):
        super(messageBox,self).__init__()
        self.desktop = QDesktopWidget() 

        self.messageLabel = QLabel()
        self.pe = QPalette()
        self.pe.setColor(QPalette.WindowText,QColor(255,255,255))        
        self.messageLabel.setPalette(self.pe)
        self.messageLabel.setText(message)
        self.messageLabel.setFont(QFont("Roman times",10,QFont.Bold))

        self.varLayout = QVBoxLayout()
        self.varLayout.addWidget(self.messageLabel)

        self.setLayout(self.varLayout)

        self.resize(250,20 * (i + 1))
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint | Qt.Tool | Qt.Popup)
        self.move((self.desktop.availableGeometry().width() - self.width()),self.desktop.availableGeometry().height()) #初始化位置到右下角
        self.setWindowOpacity(0.3)

        self.setAutoFillBackground(True)
        self.palette = QPalette()
        self.palette.setBrush(QPalette.Background,QBrush(QPixmap(os.getcwd() + '/images/background.png')))
        self.setPalette(self.palette)  

        self.showAnimation()  

        #弹出动画
    def showAnimation(self):
        #显示弹出框动画
        self.animation = QPropertyAnimation(self,"pos")
        self.animation.setDuration(1000)
        self.animation.setStartValue(QPoint(self.x(),self.y()))
        self.animation.setEndValue(QPoint((self.desktop.availableGeometry().width() - self.width()),(self.desktop.availableGeometry().height() - self.height())))
        self.animation.start()

        #设置弹出框1秒弹出，然后渐隐
        self.remainTimer = QTimer()
        self.connect(self.remainTimer,SIGNAL("timeout()"),self,SLOT("closeAnimation()"))
        self.remainTimer.start(3000)  #定时器10秒
    #关闭动画
    @pyqtSlot()
    def closeAnimation(self):
        global hasMessage
        #清除Timer和信号槽
        self.remainTimer.stop()
        self.disconnect(self.remainTimer,SIGNAL("timeout()"),self,SLOT("closeAnimation()"))
        self.remainTimer.deleteLater()
        self.remainTimer = None
        #弹出框渐隐
        self.animation = QPropertyAnimation(self,"windowOpacity")
        self.animation.setDuration(3000)
        self.animation.setStartValue(0.3)
        self.animation.setEndValue(0)
        self.animation.start()
        #动画完成后清理
        hasMessage = False
        self.connect(self.animation,SIGNAL("finished()"),self,SLOT("close()"))

    #清理及退出
    @pyqtSlot()
    def clearAll(self):
        global hasMessage
        self.disconnect(self.animation,SIGNAL("finished()"),self,SLOT("clearAll()"))        
        self.close()        #退出
        hasMessage = False


if __name__ == "__main__":
    #app = QApplication(sys.argv)
    #message = messageBox("hello↑↑↑↑")
    #message.show()
    #sys.exit(app.exec_())
    app = QApplication(sys.argv)
    dialog = mainWidget()
    dialog.resize(950,300)

    hotKey = hotKeyThread()
    hotKey.start()   

    timer = QTimer()
    workThread = WorkThread()

    dialog.execButton.clicked.connect(work)
    
    #timer.moveToThread(hotKey)
    timer.timeout.connect(countTime)
    #dialog.show()
    dialog.execButton.click()

    #msg = wintypes.MSG()
    #while user32.GetMessageA(byref(msg), None, 0, 0) != 0:
    #    if msg.message == win32con.WM_HOTKEY:
    #        action_to_take = HOTKEY_ACTIONS.get(msg.wParam)
    #        if action_to_take:
    #            action_to_take(1)
    sys.exit(app.exec_())
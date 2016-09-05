#coding=utf-8
import sys
from PyQt4 import QtGui,QtCore
import urllib.request  
import urllib.parse  
import re  
import urllib.request
import urllib.parse
import http.cookiejar  
import time  
import os
import json

ISOTIMEFORMAT = '%Y-%m-%d %X'


global shenzhen,shanghai,stock,code
shenzhen = ''
shanghai = ''
stock = ''
code = ''

class WorkThread(QtCore.QThread):
    trigger = QtCore.pyqtSignal()
    def __int__(self):
        super(WorkThread,self).__init__()

    def getHtml(self,url): 
      
        cj = http.cookiejar.CookieJar()  
        opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(cj))  
        opener.addheaders = [('User-Agent','Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2272.101 Safari/537.36'),('Cookie','4564564564564564565646540'),('apikey','d537c2a89195597876e920678da7d066')]  
  
        urllib.request.install_opener(opener)  
      
        page = urllib.request.urlopen(url)  
        html = page.read().decode('UTF-8')
        return html  

    def GetContext(self,context,param):
        result = ''    
        for s in str(param).split('/'):
            result = result + '' + str(context[s]) + ','
        return result

    def run(self):
        global shenzhen,shanghai,stock,code
        while True:            
            html = self.getHtml('http://apis.baidu.com/apistore/stockservice/stock?stockid=' + code + '&list=1')
            html = json.dumps(json.loads(html),ensure_ascii=False)
            html = json.loads(html)
            i = 0
            stock = ''
            for s in code.split(','):
                stockinfo = html['retData']['stockinfo'][i]
            #name/code/date/time/OpenningPrice/closingPrice/currentPrice/hPrice/lPrice
                stockinfo = self.GetContext(stockinfo,'name/code/date/time/currentPrice/hPrice/lPrice/OpenningPrice/closingPrice')
                stock = stock + str(stockinfo)
                i = i + 1
            stock = stock[:-1]
            shanghai = html['retData']['market']['shanghai']
            #name/curdot/curprice/rate
            shanghai = self.GetContext(shanghai,'name/curdot/curprice/rate')
            shenzhen = html['retData']['market']['shenzhen']
            #name/curdot/curprice/rate
            shenzhen = self.GetContext(shenzhen,'name/curdot/curprice/rate')   
            time.sleep(10) 
        self.trigger.emit() 
      
def countTime():
    global shenzhen,shanghai,stock,code
    dialog.indexLabel.setText(str(shanghai[:-1] + '\n' + shenzhen[:-1]))
    stockArr = stock.split(',')
    total = len(stock.split(','))
    num = 0
    rowcount = 0
    while rowcount < len(code.split(',')):
        for j in range(dialog.table.columnCount()-1):
            if num < total:
                cnt = stockArr[num]
                newItem = QtGui.QTableWidgetItem(cnt)
                dialog.table.setItem(rowcount,j,newItem)
                num = num + 1        
        if  dialog.table.item(rowcount,4) :
            if float(dialog.table.item(rowcount,4).text()) > float(dialog.table.item(rowcount,8).text()):
                cnt = stockArr[4 + rowcount * 9]
                newItem = QtGui.QTableWidgetItem(cnt)
                newItem.setTextColor(QtGui.QColor(255,0,0))
                dialog.table.setItem(rowcount,4,newItem)
            if float(dialog.table.item(rowcount,4).text()) < float(dialog.table.item(rowcount,8).text()):
                cnt = stockArr[4 + rowcount * 9]
                newItem = QtGui.QTableWidgetItem(cnt)
                newItem.setTextColor(QtGui.QColor(0,255,0))
                dialog.table.setItem(rowcount,4,newItem)
            if float(dialog.table.item(rowcount,4).text()) == float(dialog.table.item(rowcount,8).text()):
                cnt = stockArr[4 + rowcount * 9]
                newItem = QtGui.QTableWidgetItem(cnt)
                newItem.setTextColor(QtGui.QColor(0,0,0))
                dialog.table.setItem(rowcount,4,newItem)
        if dialog.table.item(rowcount,4) and dialog.table.item(rowcount,8):
            rate = float(dialog.table.item(rowcount,4).text()) / float(dialog.table.item(rowcount,8).text()) - 1
            rate = round(rate * 100,2)            
            if rate > 0:
                newItem = QtGui.QTableWidgetItem(str(rate))
                newItem.setTextColor(QtGui.QColor(255,0,0))
                dialog.table.setItem(rowcount,9,newItem)
            if rate < 0:
                newItem = QtGui.QTableWidgetItem(str(rate))
                newItem.setTextColor(QtGui.QColor(0,255,0))
                dialog.table.setItem(rowcount,9,newItem)
            if rate == 0:
                newItem = QtGui.QTableWidgetItem(str(rate))
                newItem.setTextColor(QtGui.QColor(0,0,0))
                dialog.table.setItem(rowcount,9,newItem)
        rowcount = rowcount + 1
    dialog.timeLabel.setText(time.strftime(ISOTIMEFORMAT, time.localtime()))
    dialog.table.repaint()    

def work():
    global shenzhen,shanghai,stock,code
    c = dialog.lineEdit.text()
    dialog.table.clearContents()
    code = ''
    for s in c.split(','):
        code = code + 'sh' + s + ',' if s.startswith('60') else code + 'sz' + s + ','
    code = code[:-1]
    timer.start(1000)               
    workThread.start()              
    #workThread.trigger.connect(timeStop)
def timeStop():
    workThread.run()


class firstDialog(QtGui.QWidget):
    def __init__(self,parent=None):
        QtGui.QWidget.__init__(self,parent)
        self.timeLabel = QtGui.QLabel()
        self.pe = QtGui.QPalette()
        self.pe.setColor(QtGui.QPalette.WindowText,QtGui.QColor(255,255,255))
        self.timeLabel.setPalette(self.pe)
        self.timeLabel.setText(time.strftime(ISOTIMEFORMAT, time.localtime()))
        self.descriptLabel = QtGui.QLabel('input code ,split with comma like \',\'')
        self.descriptLabel.setPalette(self.pe)
        self.lineEdit = QtGui.QLineEdit()
        self.execButton = QtGui.QPushButton('exec') 
        
        self.nameCheckBox = QtGui.QCheckBox('name')
        self.nameCheckBox.setPalette(self.pe)
        self.nameCheckBox.setChecked(True)
        self.nameCheckBox.connect(self.nameCheckBox,QtCore.SIGNAL('clicked()'),self.setHideOrShow)
        self.codeCheckBox = QtGui.QCheckBox('code')
        self.codeCheckBox.setPalette(self.pe)
        self.codeCheckBox.setChecked(True)
        self.codeCheckBox.connect(self.codeCheckBox,QtCore.SIGNAL('clicked()'),self.setHideOrShow)
        self.dateCheckBox = QtGui.QCheckBox('date')
        self.dateCheckBox.setPalette(self.pe)
        self.dateCheckBox.setChecked(True)
        self.dateCheckBox.connect(self.dateCheckBox,QtCore.SIGNAL('clicked()'),self.setHideOrShow)
        self.timeCheckBox = QtGui.QCheckBox('time')
        self.timeCheckBox.setPalette(self.pe)
        self.timeCheckBox.setChecked(True)
        self.timeCheckBox.connect(self.timeCheckBox,QtCore.SIGNAL('clicked()'),self.setHideOrShow)
        self.currentPriceCheckBox = QtGui.QCheckBox('currentPrice')
        self.currentPriceCheckBox.setPalette(self.pe)
        self.currentPriceCheckBox.setChecked(True)
        self.currentPriceCheckBox.connect(self.currentPriceCheckBox,QtCore.SIGNAL('clicked()'),self.setHideOrShow)
        self.hPriceCheckBox = QtGui.QCheckBox('hPrice')
        self.hPriceCheckBox.setPalette(self.pe)
        self.hPriceCheckBox.setChecked(True)
        self.hPriceCheckBox.connect(self.hPriceCheckBox,QtCore.SIGNAL('clicked()'),self.setHideOrShow)
        self.lPriceCheckBox = QtGui.QCheckBox('lPrice')
        self.lPriceCheckBox.setPalette(self.pe)
        self.lPriceCheckBox.setChecked(True)
        self.lPriceCheckBox.connect(self.lPriceCheckBox,QtCore.SIGNAL('clicked()'),self.setHideOrShow)
        self.OpenningPriceCheckBox = QtGui.QCheckBox('OpenningPrice')
        self.OpenningPriceCheckBox.setPalette(self.pe)
        self.OpenningPriceCheckBox.setChecked(True)
        self.OpenningPriceCheckBox.connect(self.OpenningPriceCheckBox,QtCore.SIGNAL('clicked()'),self.setHideOrShow)
        self.closingPriceCheckBox = QtGui.QCheckBox('closingPrice')
        self.closingPriceCheckBox.setPalette(self.pe)    
        self.closingPriceCheckBox.setChecked(True)
        self.closingPriceCheckBox.connect(self.closingPriceCheckBox,QtCore.SIGNAL('clicked()'),self.setHideOrShow) 
        self.RateCheckBox = QtGui.QCheckBox('Rate')
        self.RateCheckBox.setPalette(self.pe)    
        self.RateCheckBox.setChecked(True)
        self.RateCheckBox.connect(self.RateCheckBox,QtCore.SIGNAL('clicked()'),self.setHideOrShow)       
               
        self.indexLabel = QtGui.QLabel()
        self.indexLabel.setPalette(self.pe)
        self.table = QtGui.QTableWidget(10,10)
        self.table.setHorizontalHeaderLabels(['name','code','date','time','currentPrice','hPrice','lPrice','OpenningPrice','closingPrice','Rate'])        
        self.table.verticalHeader().setVisible(False)
        self.table.setEditTriggers(QtGui.QTableWidget.NoEditTriggers)
        self.table.setAlternatingRowColors(True)              

        self.horLayout = QtGui.QHBoxLayout()
        self.horLayout.addWidget(self.descriptLabel)
        self.horLayout.addWidget(self.lineEdit)
        self.horLayout.addWidget(self.execButton)

        self.midLayout = QtGui.QHBoxLayout()
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

        self.varLayout = QtGui.QVBoxLayout()
        self.varLayout.addWidget(self.indexLabel)
        self.varLayout.addWidget(self.table)

        self.layout = QtGui.QVBoxLayout()
        self.layout.addWidget(self.timeLabel)
        self.layout.addLayout(self.horLayout)
        self.layout.addLayout(self.midLayout)
        self.layout.addLayout(self.varLayout)

        self.setLayout(self.layout)
        self.setWindowTitle('stock v1.1')

        self.icon = QtGui.QIcon()
        self.icon.addPixmap(QtGui.QPixmap(os.getcwd() + '/hehe.png'), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.setWindowIcon(self.icon)

        self.setAutoFillBackground(True)
        self.palette = QtGui.QPalette()
        self.palette.setBrush(QtGui.QPalette.Background,QtGui.QBrush(QtGui.QPixmap(os.getcwd() + '/www.png')))
        self.setPalette(self.palette)   

    def  setHideOrShow(self):
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


app = QtGui.QApplication(sys.argv)
dialog = firstDialog()
dialog.resize(950,240)
timer = QtCore.QTimer()
workThread = WorkThread()
dialog.execButton.clicked.connect(work)
timer.timeout.connect(countTime)
dialog.show()
sys.exit(app.exec_())

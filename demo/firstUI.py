#coding=utf-8
import sys
from PyQt4 import QtGui,QtCore
import urllib.request  
import urllib.parse  
import re  
import urllib.request,urllib.parse,http.cookiejar  
import time  
import os
import json

ISOTIMEFORMAT='%Y-%m-%d %X'


global shenzhen,shanghai,stock,c
shenzhen=''
shanghai=''
stock=''
c=''

class WorkThread(QtCore.QThread):
    trigger = QtCore.pyqtSignal()
    def __int__(self):
        super(WorkThread,self).__init__()

    def getHtml(self,url): 
      
        cj=http.cookiejar.CookieJar()  
        opener=urllib.request.build_opener(urllib.request.HTTPCookieProcessor(cj))  
        opener.addheaders=[('User-Agent','Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2272.101 Safari/537.36'),('Cookie','4564564564564564565646540'),('apikey','d537c2a89195597876e920678da7d066')]  
  
        urllib.request.install_opener(opener)  
      
        page = urllib.request.urlopen(url)  
        html = page.read().decode('UTF-8')
        return html  

    def GetContext(self,context,param):
        result=''    
        for s in str(param).split('/'):
            result=result+''+str(context[s])+','
        return result

    def run(self):
        global shenzhen,shanghai,stock,c
        while True:
            code=''
            for s in c.split(','):
                code=code+'sh'+s+',' if s.startswith('60') else code+'sz'+s+','
            html = self.getHtml('http://apis.baidu.com/apistore/stockservice/stock?stockid='+code[:-1]+'&list=1')
            html=json.dumps(json.loads(html),ensure_ascii=False)
            html=json.loads(html)
            i=0
            stock=''
            for s in c.split(','):
                stockinfo=html['retData']['stockinfo'][i]
            #name/code/date/time/OpenningPrice/closingPrice/currentPrice/hPrice/lPrice
                stockinfo=self.GetContext(stockinfo,'name/code/date/time/currentPrice/hPrice/lPrice/OpenningPrice/closingPrice')
                stock=stock+str(stockinfo)
                i=i+1
            shanghai=html['retData']['market']['shanghai']
            #name/curdot/curprice/rate
            shanghai=self.GetContext(shanghai,'name/curdot/curprice/rate')
            shenzhen=html['retData']['market']['shenzhen']
            #name/curdot/curprice/rate
            shenzhen=self.GetContext(shenzhen,'name/curdot/curprice/rate')    
        self.trigger.emit() 
      
def countTime():
    global shenzhen,shanghai,stock,c
    dialog.indexLabel.setText(str(shanghai[:-1]+'\n'+shenzhen))
    stockArr=stock.split(',')
    num=0
    rowcount=0
    while rowcount<len(c.split(',')):
        for j in range(dialog.table.columnCount()):
            cnt = stockArr[num]
            newItem = QtGui.QTableWidgetItem(cnt)
            dialog.table.setItem(rowcount,j,newItem)
            #self.table.item(j,rowcount).setText(cnt)
            num=num+1        
        if dialog.table.item(rowcount,4).text()!='':
            if float(dialog.table.item(rowcount,4).text())>float(dialog.table.item(rowcount,8).text()):
                cnt = stockArr[4+rowcount*9]
                newItem = QtGui.QTableWidgetItem(cnt)
                newItem.setTextColor(QtGui.QColor(255,0,0))
                dialog.table.setItem(rowcount,4,newItem)
            if float(dialog.table.item(rowcount,4).text())<float(dialog.table.item(rowcount,8).text()):
                cnt = stockArr[4+rowcount*9]
                newItem = QtGui.QTableWidgetItem(cnt)
                newItem.setTextColor(QtGui.QColor(0,255,0))
                dialog.table.setItem(rowcount,4,newItem)
            if float(dialog.table.item(rowcount,4).text())==float(dialog.table.item(rowcount,8).text()):
                cnt = stockArr[4+rowcount*9]
                newItem = QtGui.QTableWidgetItem(cnt)
                newItem.setTextColor(QtGui.QColor(0,0,0))
                dialog.table.setItem(rowcount,4,newItem)
        rowcount=rowcount+1
    dialog.timeLabel.setText(time.strftime( ISOTIMEFORMAT, time.localtime() ))
    dialog.table.repaint()

def work():
    global shenzhen,shanghai,stock,c
    c=dialog.lineEdit.text()
    timer.start(1000)               #计时器每秒计数
    workThread.start()              #计时开始
    #workThread.trigger.connect(timeStop)   #当获得循环完毕的信号时，停止计数

def timeStop():
    workThread.run()


class firstDialog(QtGui.QWidget):
    def __init__(self,parent=None):
        QtGui.QWidget.__init__(self,parent)
        self.timeLabel=QtGui.QLabel()
        self.pe=QtGui.QPalette()
        self.pe.setColor(QtGui.QPalette.WindowText,QtGui.QColor(255,255,255));
        self.timeLabel.setPalette(self.pe)
        self.timeLabel.setText(time.strftime( ISOTIMEFORMAT, time.localtime() ))
        self.descriptLabel=QtGui.QLabel('input code ,split with comma like \',\'')
        self.descriptLabel.setPalette(self.pe)
        self.lineEdit=QtGui.QLineEdit()
        self.execButton=QtGui.QPushButton('exec')        
        #self.connect(self.execButton,QtCore.SIGNAL('clicked()'),self.beginGet)
        self.indexLabel=QtGui.QLabel()
        self.indexLabel.setPalette(self.pe)
        self.table =QtGui.QTableWidget(10,9)
        self.table.setHorizontalHeaderLabels(['name','code','date','time','currentPrice','hPrice','lPrice','OpenningPrice','closingPrice'])        
        self.table.verticalHeader().setVisible(False)
        self.table.setEditTriggers(QtGui.QTableWidget.NoEditTriggers)
        self.table.setAlternatingRowColors(True)
        self.table.hideColumn(0)

        self.horLayout=QtGui.QHBoxLayout()
        self.horLayout.addWidget(self.descriptLabel)
        self.horLayout.addWidget(self.lineEdit)
        self.horLayout.addWidget(self.execButton)

        self.varLayout=QtGui.QVBoxLayout()
        self.varLayout.addWidget(self.indexLabel)
        self.varLayout.addWidget(self.table)

        self.layout=QtGui.QVBoxLayout()
        self.layout.addWidget(self.timeLabel)
        self.layout.addLayout(self.horLayout)
        self.layout.addLayout(self.varLayout)

        self.setLayout(self.layout)
        self.setWindowTitle('stock v1.0')

        self.icon = QtGui.QIcon()
        self.icon.addPixmap(QtGui.QPixmap(os.getcwd()+'/hehe.png'), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.setWindowIcon(self.icon)

        self.setAutoFillBackground(True)
        self.palette=QtGui.QPalette()
        self.palette.setBrush(QtGui.QPalette.Background,QtGui.QBrush(QtGui.QPixmap(os.getcwd()+'/www.png')));
        self.setPalette(self.palette);



    #def beginGet(self):
    #    c=self.lineEdit.text()
    #    while True:
                
    #        self.indexLabel.setText(str(shanghai+shenzhen))
    #        stockArr=stock.split(',')
    #        num=0
    #        rowcount=0
    #        while rowcount<len(c.split(',')):
    #            for j in range(self.table.rowCount()):
    #                cnt = stockArr[num]
    #                newItem = QtGui.QTableWidgetItem(cnt)
    #                self.table.setItem(j,rowcount,newItem)
    #                #self.table.item(j,rowcount).setText(cnt)
    #                num=num+1
    #            rowcount=rowcount+1
    #        self.timeLabel.setText(time.strftime( ISOTIMEFORMAT, time.localtime() ))
    #        self.table.repaint()
    #        self.table.setItemDelegateForRow
    #        time.sleep(1)
        

    

app=QtGui.QApplication(sys.argv)
dialog=firstDialog()
dialog.resize(950,240)
timer=QtCore.QTimer()
workThread=WorkThread()
dialog.execButton.clicked.connect(work)
timer.timeout.connect(countTime)
dialog.show()
sys.exit(app.exec_())

# coding=utf-8
#import sip 
#sip.setapi('QVariant', 1)

#from PyQt4.QtCore import * 
#from PyQt4.QtGui import * 
#import sys

#####################################################################
#def main():
#    app = QApplication(sys.argv)
#    w = MyWindow()
#    w.show()
#    sys.exit(app.exec_())

#####################################################################
#class MyWindow(QWidget):
#    def __init__(self, *args):
#        QWidget.__init__(self, *args)

#        # create objects
#        list_data = [1,2,3,4]
#        lm = MyListModel(list_data, self)
#        de = MyDelegate(self)
#        lv = QListView()
#        lv.setModel(lm)
#        lv.setItemDelegate(de)

#        # layout
#        layout = QVBoxLayout()
#        layout.addWidget(lv)
#        self.setLayout(layout)

#####################################################################
#class MyDelegate(QItemDelegate):
#    def __init__(self, parent=None, *args):
#        QItemDelegate.__init__(self, parent, *args)

#    def paint(self, painter, option, index):
#        painter.save()

#        # set background color
#        painter.setPen(QPen(Qt.NoPen))
#        if option.state & QStyle.State_Selected:
#            painter.setBrush(QBrush(Qt.red))
#        else:
#            painter.setBrush(QBrush(Qt.white))
#        painter.drawRect(option.rect)

#        # set text color
#        painter.setPen(QPen(Qt.black))
#        value = index.data(Qt.DisplayRole)
#        if value.isValid():
#            text = value.toString()
#            painter.drawText(option.rect, Qt.AlignLeft, text)

#        painter.restore()

#####################################################################
#class MyListModel(QAbstractListModel):
#    def __init__(self, datain, parent=None, *args):
#        """ datain: a list where each item is a row
#        """
#        QAbstractTableModel.__init__(self, parent, *args)
#        self.listdata = datain

#    def rowCount(self, parent=QModelIndex()):
#        return len(self.listdata)

#    def data(self, index, role):
#        if index.isValid() and role == Qt.DisplayRole:
#            return QVariant(self.listdata[index.row()])
#        else:
#            return QVariant()

#####################################################################
#if __name__ == "__main__":
#    main()



# coding=utf-8
__author__ = 'a359680405'

from PyQt4.QtCore import *
from PyQt4.QtGui import *

global sec
sec=0

class WorkThread(QThread):
    trigger = pyqtSignal()
    def __int__(self):
        super(WorkThread,self).__init__()

    def run(self):
        for i in range(203300030):
            pass
        self.trigger.emit()         #ѭ����Ϻ󷢳��ź�

def countTime():
    global  sec
    sec+=1
    lcdNumber.display(sec)          #LED��ʾ����+1

def work():
    timer.start(1000)               #��ʱ��ÿ�����
    workThread.start()              #��ʱ��ʼ
    workThread.trigger.connect(timeStop)   #�����ѭ����ϵ��ź�ʱ��ֹͣ����

def timeStop():
    timer.stop()
    print('total',lcdNumber.value())
    global sec
    sec=0

app=QApplication([])
top=QWidget()
layout=QVBoxLayout(top)             #��ֱ������QVBoxLayout��
lcdNumber=QLCDNumber()              #�Ӹ���ʾ��
layout.addWidget(lcdNumber)
button=QPushButton('test')
layout.addWidget(button)

timer=QTimer()
workThread=WorkThread()

button.clicked.connect(work)
timer.timeout.connect(countTime)      #ÿ�μ�ʱ����������setTime

top.show()
app.exec()

#!/usr/bin/python  
#-*-coding:utf-8-*-
from PyQt4.QtGui import *
from PyQt4.Qt import *
from PyQt4.QtCore import *

class AboutUsDialog(QWidget):        
    def __init__(self, parent=None):        
        super(AboutUsDialog, self).__init__(parent)        
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.Dialog)            
        
    def isInTitle(self, xPos, yPos):        
        return yPos < 30        
    
class MyApplication(QApplication):        
    def __init__(self, args):        
        super(MyApplication, self).__init__(args)        
            
    def GET_X_LPARAM(self, param):              
        return param & 0xffff    
        
    def GET_Y_LPARAM(self, param):        
        return param >> 16        
        
    def winEventFilter(self, msg):        
        if msg.message == 0x84: #WM_NCHITTEST
            form = self.activeWindow()            
        if form:                
            xPos = self.GET_X_LPARAM(msg.lParam) - form.frameGeometry().x()                
            yPos = self.GET_Y_LPARAM(msg.lParam) - form.frameGeometry().y()
            #                鼠标在窗体自定义标题范围内，窗体自定义一个isInTitle的方法判断
            #
                
        if yPos < 30 and xPos < 456:                
            if not form.isMaximized() and hasattr(form, 'isInTitle') and form.isInTitle(xPos, yPos):                    
                return True, 0x2 #HTCAPTION
                    
        return False, 0        
        
if __name__ == '__main__':        
    import sys    
    app = MyApplication(sys.argv)    
    aboutus = AboutUsDialog()    
    aboutus.showNormal()    
    sys.exit(app.exec_()) 
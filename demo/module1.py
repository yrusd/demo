# coding=gbk

# 导入模块
import sys
from PyQt4 import QtGui,QtCore
######################################### 自定义窗口类 ########################################
class MyWindow(QtGui.QMainWindow):
    '''自定义窗口类'''
    ###################################### 构造、析构函数 ###################################
    def __init__(self,parent=None):
        '''构造函数'''
        # 调用父类构造函数
        super(MyWindow,self).__init__(parent)
        # 设置窗口标记（无边框|任务栏右键菜单）
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint | QtCore.Qt.WindowSystemMenuHint)
        # 便于显示，设置窗口背景颜色(采用QSS)
        self.setStyleSheet('''background-color:cyan;''')
    ####################################### 覆盖函数 #######################################    
    def showMaximized(self):
        '''最大化'''
        # 得到桌面控件
        desktop = QtGui.QApplication.desktop()
        # 得到屏幕可显示尺寸
        rect = desktop.availableGeometry()
        # 设置窗口尺寸
        self.setGeometry(rect)
        # 设置窗口显示
        self.show()

########################################### 主函数 #########################################        
if __name__ == "__main__":
    '''主函数'''
    # 声明变量
    app = QtGui.QApplication(sys.argv)
    # 创建窗口
    window = MyWindow()
    # 调用最大化显示
    window.showMaximized()
    # 应用程序事件循环
    sys.exit(app.exec_())
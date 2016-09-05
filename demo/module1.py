# coding=gbk

# ����ģ��
import sys
from PyQt4 import QtGui,QtCore
######################################### �Զ��崰���� ########################################
class MyWindow(QtGui.QMainWindow):
    '''�Զ��崰����'''
    ###################################### ���졢�������� ###################################
    def __init__(self,parent=None):
        '''���캯��'''
        # ���ø��๹�캯��
        super(MyWindow,self).__init__(parent)
        # ���ô��ڱ�ǣ��ޱ߿�|�������Ҽ��˵���
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint | QtCore.Qt.WindowSystemMenuHint)
        # ������ʾ�����ô��ڱ�����ɫ(����QSS)
        self.setStyleSheet('''background-color:cyan;''')
    ####################################### ���Ǻ��� #######################################    
    def showMaximized(self):
        '''���'''
        # �õ�����ؼ�
        desktop = QtGui.QApplication.desktop()
        # �õ���Ļ����ʾ�ߴ�
        rect = desktop.availableGeometry()
        # ���ô��ڳߴ�
        self.setGeometry(rect)
        # ���ô�����ʾ
        self.show()

########################################### ������ #########################################        
if __name__ == "__main__":
    '''������'''
    # ��������
    app = QtGui.QApplication(sys.argv)
    # ��������
    window = MyWindow()
    # ���������ʾ
    window.showMaximized()
    # Ӧ�ó����¼�ѭ��
    sys.exit(app.exec_())
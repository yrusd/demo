import sys
#from PyQt4 import QtGui,QtCore

#app=QtGui.QApplication(sys.argv)
#label=QtGui.QLabel('Hello Qt!')
#label.show()
#sys.exit(app.exec_())

#app=QtGui.QApplication(sys.argv)
#quit=QtGui.QPushButton('Quit')
#QtCore.QObject.connect(quit,QtCore.SIGNAL('clicked()'),app,QtCore.SLOT('quit()'))
#quit.show()
#sys.exit(app.exec_())

#app=QtGui.QApplication(sys.argv)
#quit=QtGui.QPushButton('Quit')
#quit.resize(75,30)
#quit.setFont(QtGui.QFont('Times',18,QtGui.QFont.Bold))
#QtCore.QObject.connect(quit,QtCore.SIGNAL('clicked()'),app,QtCore.SLOT('quit()'))
#quit.show()
#sys.exit(app.exec_())

#app=QtGui.QApplication(sys.argv)
#window=QtGui.QWidget()
#spinBox=QtGui.QSpinBox()
#slider=QtGui.QSlider(QtCore.Qt.Vertical)
#spinBox.setRange(0,130)
#slider.setRange(0,130)
#QtCore.QObject.connect(spinBox,QtCore.SIGNAL('valueChanged(int)'),slider,QtCore.SLOT('setValue(int)'))
#QtCore.QObject.connect(slider,QtCore.SIGNAL('valueChanged(int)'),spinBox,QtCore.SLOT('setValue(int)'))
#spinBox.setValue(35)
#layout=QtGui.QHBoxLayout()
#layout.addWidget(spinBox)
#layout.addWidget(slider)
#window.setLayout(layout)
#window.show()
#sys.exit(app.exec_())

#app=QtGui.QApplication(sys.argv)
#dialog=QtGui.QDialog()
#quit=QtGui.QPushButton('Quit',dialog)
#QtCore.QObject.connect(quit,QtCore.SIGNAL('clicked()'),app,QtCore.SLOT('quit()'))
#dialog.show()
#sys.exit(app.exec_())


#app=QtGui.QApplication(sys.argv)
#window=QtGui.QWidget()
#window.resize(200,120)
#quit=QtGui.QPushButton('Quit',window)
#quit.setFont(QtGui.QFont('Times',18,QtGui.QFont.Bold))
#quit.setGeometry(10,40,180,40)
#QtCore.QObject.connect(quit,QtCore.SIGNAL('clicked()'),app,QtCore.SLOT('quit()'))
#window.show()
#sys.exit(app.exec_())


#class MyWidget(QtGui.QWidget):
#    def __init__(self, parent=None):
#        QtGui.QWidget.__init__(self, parent)
#        self.setFixedSize(200, 120)
#        self.quit = QtGui.QPushButton("Quit", self)
#        self.quit.setGeometry(62, 40, 75, 30)
#        self.quit.setFont(QtGui.QFont("Times", 18, QtGui.QFont.Bold))
#        self.connect(self.quit, QtCore.SIGNAL("clicked()"),
#            self, QtCore.SLOT("close()"))

#app = QtGui.QApplication(sys.argv)
#widget = MyWidget()
#widget.move(350,50)
#widget.setWindowTitle("A Widget")
#widget.show()
#anotherWidget = MyWidget()
#anotherWidget.move(50,50)
#anotherWidget.setWindowTitle("Another Widget")
#anotherWidget.show()
#sys.exit(app.exec_())

#class MyDialog(QtGui.QDialog):
#    def __init__(self, parent=None):
#        QtGui.QDialog.__init__(self, parent)
#        self.setFixedSize(200, 120)
#        self.quit = QtGui.QPushButton("Quit", self)
#        self.quit.setGeometry(62, 40, 75, 30)
#        self.quit.setFont(QtGui.QFont("Times", 18, QtGui.QFont.Bold))
#        self.connect(self.quit, QtCore.SIGNAL("clicked()"),self, QtCore.SLOT("close()"))

#app = QtGui.QApplication(sys.argv)
#dialog = MyDialog()
#dialog.show()
#sys.exit(app.exec_())

#class MyDialog(QtGui.QDialog):
#    def __init__(self,parent=None):
#        QtGui.QDialog.__init__(self,parent)
#        self.quit=QtGui.QPushButton('Quit')
#        self.change=QtGui.QPushButton('Change')
#        self.change.setEnabled(False)
#        self.lcd=QtGui.QLCDNumber(3)
#        self.slider=QtGui.QSlider(QtCore.Qt.Horizontal)        
#        self.slider.setRange(0,999)
#        self.slider.setValue(0)
#        self.lineEdit=QtGui.QLineEdit()
#        intValidator = QtGui.QIntValidator(0,999, self)
#        self.lineEdit.setValidator(intValidator)

#        self.connect(self.quit,QtCore.SIGNAL('clicked()'),QtGui.qApp,QtCore.SLOT('quit()'))
#        self.connect(self.lineEdit,QtCore.SIGNAL('textChanged(const QString&)'),self.enableChangeButton)
#        self.connect(self.slider,QtCore.SIGNAL('valueChanged(int)'),self.sliderChange)
#        self.connect(self.change,QtCore.SIGNAL('clicked()'),self.Change)

#        self.rightLayout=QtGui.QVBoxLayout()
#        self.rightLayout.addWidget(self.lineEdit)
#        self.rightLayout.addWidget(self.change)

#        self.leftLayout=QtGui.QVBoxLayout()
#        self.leftLayout.addWidget(self.lcd)
#        self.leftLayout.addWidget(self.slider)

#        self.layout=QtGui.QHBoxLayout()
#        self.layout.addWidget(self.quit)
#        self.layout.addLayout(self.leftLayout)
#        self.layout.addLayout(self.rightLayout)

#        self.setLayout(self.layout)

#    def enableChangeButton(self,text):
#        self.change.setEnabled(len(text)>0)
#        #self.change.setEnabled(text.isEmpty()==False)

#    def Change(self):
#        value=int(self.lineEdit.text())
#        self.lcd.display(value)
#        self.slider.setValue(value)

#    def sliderChange(self):
#        value=self.slider.value()
#        self.lcd.display(value)
#        self.lineEdit.setText(str(value))


#app=QtGui.QApplication(sys.argv)
#dialog=MyDialog()
#dialog.show()
#sys.exit(app.exec_())



from PyQt4.QtGui import *
from PyQt4.QtCore import *
import sip 
sip.setapi('QVariant', 2)

model = QStandardItemModel()
item = QStandardItem("Item")
item.setFlags(Qt.ItemIsUserCheckable | Qt.ItemIsEnabled)
item.setData(QVariant(Qt.Checked), Qt.CheckStateRole)
model.appendRow(item)

view = QListView()
view.setModel(model)
view.show()
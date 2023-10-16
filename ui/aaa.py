'''
import sys
from PyQt5.QtWidgets import QWidget,QApplication
app=QApplication(sys.argv)
widget=QWidget()
widget.resize(640,480)
widget.setWindowTitle("hello,PYQT5!")
widget.show()
sys.exit(app.exec())

'''
import sys
import SQEAutoTest
from PyQt5 import QtWidgets,QtCore,QtGui
app=QtWidgets.QApplication(sys.argv)
app.setStyle('Fusion')
MainWindow=QtWidgets.QMainWindow()
Ui=SQEAutoTest.Ui_MainWindow()
Ui.setupUi(MainWindow)

MainWindow.show()
sys.exit(app.exec_())

import sys,os
from ui import SQEAutoTest
from utils import FileUtil
from tab_precision import offlineProcessingSpeed
from PyQt5.QtWidgets import QApplication,QMainWindow,QFileDialog
class MainWindow(QMainWindow):
    __errorFormat='<font color="#DC143C">{}</font>'
    __warningFormat = '<font color="#DAA520">{}</font>'
    __validFormat = '<font color="#006400">{}</font>'
    def __init__(self,parent=None):
        super(QMainWindow,self).__init__(parent)
        self.ui=SQEAutoTest.Ui_MainWindow()
        self.ui.setupUi(self)

    def showRefineSpeedResult(self):
        input_file=self.ui.textEdit_SFLog.toPlainText().strip()
        if len(input_file)==0:
            self.ui.textEdit_offlineSpeedResult.setText(self.__errorFormat.format("input file cannot be empty!"))

        else:
            contents=offlineProcessingSpeed.refineSpeed(input_file)
            #contents=FileUtil.getFileContent(result_file)
            if len(contents)==0:
                self.ui.textEdit_offlineSpeedResult.setText(self.__warningFormat.format("no refine result output"))
            else:
                self.ui.textEdit_offlineSpeedResult.setText(self.__validFormat.format('<br/>'.join(contents)))

    def openFile(self):
        fileName, _ = QFileDialog.getOpenFileName(self, 'Open file', os.environ.get("USERPROFILEtaoqi",r"C:\ProgramData\DEXIS IS\ScanFlow\log"),"CSV UTF-8 (Comma delimited)(*.csv)")
        self.ui.textEdit_SFLog.setPlainText(fileName)
        self.ui.textEdit_offlineSpeedResult.setText("")

def generate_gui():
    myapp = QApplication(sys.argv)
    myapp.setStyle('Fusion')
    myWindow=MainWindow()
    myWindow.show()
    sys.exit(myapp.exec_())

if __name__=='__main__':
    #myapp=QApplication(sys.argv)
    #myapp.setStyle('Fusion')
    #myWindow=MainWindow()
    #myWindow.show()
    #sys.exit(myapp.exec_())
    generate_gui()

from PyQt5.QtWidgets import QFileDialog, QMainWindow, QApplication
import sys,os


class Example(QMainWindow):

    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        self.setGeometry(300, 300, 450, 400)
        self.setWindowTitle('File dialog')
        self.show()
        self.openFile()



    def openFile(self):
        fileName, _ = QFileDialog.getOpenFileName(self, 'Open file', os.environ.get("USERPROFILE","c:\\"),"CSV UTF-8 (Comma delimited)(*.csv)")
        print(fileName)
        return fileName
if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec_())
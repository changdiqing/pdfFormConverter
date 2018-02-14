import sys
import os.path
import FormLayerCreator
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QPushButton, QLineEdit, QLabel
from Ui_MainWindow import Ui_MainWindow
from pdfrw import PdfReader

class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.setupUi(self)
        self.initUI()

    def initUI(self):
        self.button = CustomLabel('Drop here.', self)
        self.button.move(0,0)

        self.lineEdit.textChanged.connect(self.lineEditTextChangeMethod)

    def lineEditTextChangeMethod(self):
        self.button.targetText = self.lineEdit.text()+'_'



class CustomLabel(QLabel):

    def __init__(self, title, parent):
        super().__init__(title, parent)
        self.setStyleSheet("margin:5px;  min-width: 28em;min-height: 18em ; border:1px solid rgb(0, 0, 0); ")
        self.setAcceptDrops(True)
        self.targetText = ""

    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls():
            event.accept()
        else:
            event.ignore()

    def dropEvent(self, event):
        for url in event.mimeData().urls():
            path = url.toLocalFile()

            print(os.path.isfile(path))
            FormLayerCreator.createFormLayerByTarget(path, self.targetText)
            #path = url.toLocalFile().toLocal8Bit().data()
            #if os.path.isfile(path):
            #    print(path)
            # do other stuff with path...

if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec_())

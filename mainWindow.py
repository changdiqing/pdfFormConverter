import sys
import os.path
import FormLayerCreator
from PyQt5.QtWidgets import QApplication, QMessageBox, QMainWindow, QPushButton, QLabel, QListWidget, QFileDialog, QAbstractItemView
from PyQt5.QtCore import pyqtSignal
from Ui_MainWindow import Ui_MainWindow
from PyPDF2 import PdfMerger
import pickle

class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.setupUi(self)
        self.initUI()

    def initUI(self):
        self.button = CustomLabel('Drop to add the main file.', self)
        self.button.move(5,0)
        self.fileList = CustomListWidget('Drop here.', self)
        self.fileList.move(5,260)

        self.lineEdit.textEdited.connect(self.lineEditTextEditedMethod)
        self.lineEdit.placeholderText="Keyword"

        self.convertButton = QPushButton('New Button', self)
        self.convertButton.setText('Convert')
        self.convertButton.move(5, 410)
        self.convertButton.clicked.connect(self.convert)

        try:
            foo = pickle.load(open("savedKeyword.pickle", "rb"))
            self.lineEdit.setText(foo)
        except (OSError, IOError) as e:
            foo = self.lineEdit.text()
            pickle.dump(foo, open("savedKeyword.pickle", "wb"))

        self.fileList.itemChanged.connect(self.fileListChangeMethod)

        fileNames = self.scannAttachments()
        for fileName in fileNames:
            self.fileList.addItem(fileName)

        self.fileListChangeMethod()

    def fileListChangeMethod(self):
        items = []
        for index in range(self.fileList.count()):
            itemText = self.fileList.item(index).text()
            fullPath = os.path.join("attachments", itemText)
            items.append(fullPath)


    def lineEditTextEditedMethod(self):
        text = self.lineEdit.text()
        with open('savedKeyword.pickle', 'wb') as handle:
            pickle.dump(text, handle, protocol=pickle.HIGHEST_PROTOCOL)

    def scannAttachments(self):
        fileNames = []
        for file in os.listdir("attachments"):
            if file.endswith(".pdf"):
                fileNames.append(file)
        return fileNames

    def mergePDFs(self, pdfs):
        merger = PdfMerger()
        for pdf in pdfs:
            merger.append(pdf)

        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        fileName, _ = QFileDialog.getSaveFileName(None,"QFileDialog.getSaveFileName()","Project Overview for Cable Lengths.pdf","PDF (*.pdf)", options=options)
        if fileName:
            merger.write(fileName)

    def convert(self):
        path = self.button.text()
        targetText = self.lineEdit.text()+'_'
        annexesRelPaths = []
        for fileName in self.fileList.getSelectedItems(False):
            annexesRelPaths.append(os.path.join("attachments", fileName))

        try:
            mergedBytesIO = FormLayerCreator.createFormLayerByTarget(path, targetText)
        except Exception as e:
            error_message= f"An error occurred: {e}"
            QMessageBox.critical(self, "Error", error_message)
            return
        self.mergePDFs([mergedBytesIO]+annexesRelPaths)

class CustomLabel(QLabel):

    def __init__(self, title, parent):
        super().__init__(title, parent)
        self.setStyleSheet("margin:5px;  min-width: 28em;min-height: 12em ; border:1px solid rgb(0, 0, 0); ")
        self.setAcceptDrops(True)
        self.fileNames = []

    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls():
            event.accept()
        else:
            event.ignore()

    def dropEvent(self, event):
        if (event.mimeData().hasUrls()):
            firstFilePath = event.mimeData().urls()[0].toLocalFile()
            self.setText(firstFilePath)


class CustomListWidget(QListWidget):
    def __init__(self, type, parent=None):
        super(CustomListWidget, self).__init__(parent)
        self.setStyleSheet("margin:5px;  min-width: 28em;min-height: 10em ; border:1px solid rgb(0, 0, 0); ")
        #self.setIconSize(QtCore.QSize(124, 124))
        #self.setDragDropMode(QtGui.QAbstractItemView.DragDrop)
        self.setSelectionMode(QAbstractItemView.MultiSelection)
        self.setAcceptDrops(True)

    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls():
            event.accept()
        else:
            super(CustomListWidget, self).dragEnterEvent(event)

    def dragMoveEvent(self, event):
        if event.mimeData().hasUrls():
            #event.setDropAction(QtCore.Qt.CopyAction)
            event.accept()
        else:
            super(CustomListWidget, self).dragMoveEvent(event)

    def dropEvent(self, event):
        if event.mimeData().hasUrls():
            #event.setDropAction(QtCore.Qt.CopyAction)
            event.accept()
            links = []
            for url in event.mimeData().urls():
                links.append(str(url.toLocalFile()))
            #self.emit(QtCore.SIGNAL("dropped"), links)
        else:
            #event.setDropAction(QtCore.Qt.MoveAction)
            super(CustomListWidget, self).dropEvent(event)

    def getSelectedItems(self, reversed=False):
        items = []
        # if reversed, collect the items in reverse order
        if reversed:
            for index in range(self.count()):
                item = self.item(self.count() - 1 - index)
                items.append(str(item.text()))
        else:
            for item in self.selectedItems():
                items.append(str(item.text()))
        return items

if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec_())

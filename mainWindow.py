import sys
import os.path
import FormLayerCreator
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QListWidget, QFileDialog
from ui.Ui_MainWindow import Ui_MainWindow
from PyPDF2 import PdfFileMerger
import pickle

class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.setupUi(self)
        self.initUI()

    def initUI(self):
        self.button = CustomLabel('Drop here the main file to start generation.', self)
        self.button.move(5,0)
        self.fileList = CustomListWidget('Drop here.', self)
        self.fileList.move(5,300)

        self.lineEdit.textChanged.connect(self.lineEditTextChangeMethod)
        self.lineEdit.textEdited.connect(self.lineEditTextEditedMethod)
        self.lineEdit.placeholderText="Keyword"

        try:
            foo = pickle.load(open("savedKeyword.pickle", "rb"))
            self.lineEdit.setText(foo)
        except (OSError, IOError) as e:
            foo = self.lineEdit.text()
            pickle.dump(foo, open("savedKeyword.pickle", "wb"))

        self.fileList.itemChanged.connect(self.fileListChangeMethod)

        fileNames = self.scannAttachments()
        for fileName in fileNames:
            #rowPosition = self.fileList.rowCount()
            #self.fileList.insertRow(rowPosition)
            self.fileList.addItem(fileName)

        self.fileListChangeMethod()

    def fileListChangeMethod(self):
        items = []
        for index in range(self.fileList.count()):
            itemText = self.fileList.item(index).text()
            fullPath = os.path.join("attachments", itemText)
            items.append(fullPath)

        self.button.fileNames = items
        print(self.button.fileNames)

    def lineEditTextChangeMethod(self):
        self.button.targetText = self.lineEdit.text()+'_'

    def lineEditTextEditedMethod(self):
        text = self.lineEdit.text()
        with open('savedKeyword.pickle', 'wb') as handle:
            pickle.dump(text, handle, protocol=pickle.HIGHEST_PROTOCOL)

    def scannAttachments(self):
        fileNames = []
        for file in os.listdir("attachments"):
            if file.endswith(".pdf"):
                fileNames.append(file)
                #print(os.path.join("attachments", file))
        return fileNames

class CustomLabel(QLabel):

    def __init__(self, title, parent):
        super().__init__(title, parent)
        self.setStyleSheet("margin:5px;  min-width: 28em;min-height: 14em ; border:1px solid rgb(0, 0, 0); ")
        self.setAcceptDrops(True)
        self.targetText = ""
        self.fileNames = []

    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls():
            event.accept()
        else:
            event.ignore()

    def dropEvent(self, event):
        for url in event.mimeData().urls():
            path = url.toLocalFile()
            print(os.path.isfile(path))
            mergedBytesIO = FormLayerCreator.createFormLayerByTarget(path, self.targetText)
            self.mergePDFs([mergedBytesIO]+self.fileNames)
            #path = url.toLocalFile().toLocal8Bit().data()
            #if os.path.isfile(path):
            #    print(path)
            # do other stuff with path...

    def mergePDFs(self, pdfs):
        merger = PdfFileMerger()
        for pdf in pdfs:
            merger.append(pdf)

        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        fileName, _ = QFileDialog.getSaveFileName(None,"QFileDialog.getSaveFileName()","Project Overview for Cable Lengths.pdf","PDF (*.pdf)", options=options)
        if fileName:
            merger.write(fileName)

class CustomListWidget(QListWidget):
    def __init__(self, type, parent=None):
        super(CustomListWidget, self).__init__(parent)
        self.setStyleSheet("margin:5px;  min-width: 28em;min-height: 10em ; border:1px solid rgb(0, 0, 0); ")
        #self.setIconSize(QtCore.QSize(124, 124))
        #self.setDragDropMode(QtGui.QAbstractItemView.DragDrop)
        #self.setSelectionMode(QtGui.QAbstractItemView.ExtendedSelection)
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

if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec_())

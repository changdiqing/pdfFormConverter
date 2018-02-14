from pdfminer.pdfparser import PDFParser
from pdfminer.pdfdocument import PDFDocument
from pdfminer.pdfpage import PDFPage
from pdfminer.pdfpage import PDFTextExtractionNotAllowed
from pdfminer.pdfinterp import PDFResourceManager
from pdfminer.pdfinterp import PDFPageInterpreter
from pdfminer.pdfdevice import PDFDevice
from pdfminer.layout import LAParams, LTTextBox, LTTextLine, LTFigure
from pdfminer.converter import PDFPageAggregator
import pdfminer

class textBox:
    def __init__(self, coor1, coor2, coor3, coor4, text):
        self.coorxl = coor1
        self.cooryl = coor2
        self.coorxr = coor3
        self.cooryr = coor4
        self.text = text

class pdfTextParser:
    def __init__(self):
        self.textBoxList = []
        self.pageSize = [0, 0]

    def extractTargetText(self, targetPath, targetText = '10m'):

        # Open a PDF file.
        #fp = open('/Users/diqingchang/Desktop/Untitled.pdf', 'rb')
        fp = open(targetPath, 'rb')

        # Create a PDF parser object associated with the file object.
        parser = PDFParser(fp)

        # Create a PDF document object that stores the document structure.
        # Password for initialization as 2nd parameter
        document = PDFDocument(parser)

        # Check if the document allows text extraction. If not, abort.
        if not document.is_extractable:
            raise PDFTextExtractionNotAllowed

        # Create a PDF resource manager object that stores shared resources.
        rsrcmgr = PDFResourceManager()

        # Create a PDF device object.
        device = PDFDevice(rsrcmgr)

        # BEGIN LAYOUT ANALYSIS
        # Set parameters for analysis.
        laparams = LAParams()

        # Create a PDF page aggregator object.
        device = PDFPageAggregator(rsrcmgr, laparams=laparams)

        # Create a PDF interpreter object.
        interpreter = PDFPageInterpreter(rsrcmgr, device)

        # loop over all pages in the document
        for page in PDFPage.create_pages(document):

            # read the page into a layout object
            interpreter.process_page(page)
            layout = device.get_result()

            # extract text from this object
            extractedList = parse_obj(layout._objs)
            self.textBoxList = self.textBoxList + extractedList

def parse_obj(lt_objs):

    myStack = []
    # loop over the object list
    for obj in lt_objs:

        # if it's a textbox, print text and location
        #if isinstance(obj, pdfminer.layout.LTTextBoxHorizontal):
        if isinstance(obj, LTTextBox):
            for myTextLine in obj:
                myStack.append(textBox(myTextLine.bbox[0], myTextLine.bbox[1], myTextLine.bbox[2], myTextLine.bbox[3],myTextLine.get_text().replace('\n', '_')))
        elif isinstance(obj, LTTextLine):
            #print ("%6d, %6d, %s" % (obj.bbox[0], obj.bbox[1], obj.get_text().replace('\n', '_')))
            #print(obj.bbox[2])
            #print(obj.bbox[3])
            myStack.append(textBox(obj.bbox[0], obj.bbox[1], obj.bbox[2], obj.bbox[3],obj.get_text().replace('\n', '_')))

        # if it's a container, recurse
        elif isinstance(obj, pdfminer.layout.LTFigure):
            parse_obj(obj._objs)
    return myStack

if __name__ == "__main__":

    targetPath = 'G17170085 Radiant Opto Taiwan.pdf'
    pdfTextParser().extractTargetText(targetPath)


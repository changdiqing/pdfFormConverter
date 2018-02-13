from PdfParser import pdfTextParser
from PyPDF2 import PdfFileWriter, PdfFileReader
from FormularLayerGenerator import FormularLayerGenerator
from PdfMerger import PdfMerger

# file to be modified and keyword that is to be watermarked
def createFormLayerByTarget(targetFile, targetText):

    # instantiate classes
    myParser = pdfTextParser()
    myFormLayerGenerator = FormularLayerGenerator()
    myMerger = PdfMerger()

    # get page size from target file
    existing_pdf = PdfFileReader(open(targetFile, "rb"))
    page = existing_pdf.getPage(0)
    x1, x2, xTR, yTR = page.mediaBox


    # parse the target file and extract text coordinates
    coorList = []
    myParser.extractTargetText(targetFile)

    for item in myParser.textBoxList:
        if item.text == targetText:
            print(item.text)
            coorList.append([item.coorxl, item.cooryl, item.coorxr, item.cooryr])

    # create intermediate pdf file as new formular layer with pageSize and coordinates
    myBytesIO = myFormLayerGenerator.createFormLayer(xTR, yTR, coorList)

    # merge the formular layer and the original file
    myMerger.merge('intermediate.pdf',targetFile)

    return myBytesIO

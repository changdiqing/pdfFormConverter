from PdfParser import pdfTextParser
from PyPDF2 import PdfReader
from FormularLayerGenerator import FormularLayerGenerator
from PdfMerger import PdfMerger

# file to be modified and keyword that is to be watermarked
def createFormLayerByTarget(targetFile, targetText):

    # instantiate classes
    myParser = pdfTextParser()
    myFormLayerGenerator = FormularLayerGenerator()
    myMerger = PdfMerger()

    # get page size from target file
    # check if is valid pdf file
    try:
        existing_pdf = PdfReader(open(targetFile, "rb"))
    except:
        print("exception thrown when reading the pdf file")
        raise

    page = existing_pdf.pages[0]
    x1, x2, xTR, yTR = page.mediabox


    # parse the target file and extract text coordinates
    coorList = []
    myParser.extractTargetText(targetFile)

    for item in myParser.textBoxList:
        if item.text == targetText:
            coorList.append([item.coorxl, item.cooryl, item.coorxr, item.cooryr])
        else:
            pass

    # check if is valid pdf file
    if not coorList:
        print("Nothing here")
        return

    # create intermediate pdf file as new formular layer with pageSize and coordinates
    myBytesIO = myFormLayerGenerator.createFormLayer(xTR, yTR, coorList)

    # merge the formular layer and the original file
    mergedBytesIO = myMerger.merge(myBytesIO,targetFile)

    return mergedBytesIO

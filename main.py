from pdfMiner import pdfTextParser

myPath = '/Users/diqingchang/Desktop/Untitled.pdf'
myTargetPath = ' '
myParser = pdfTextParser()
myParser.extractTargetText(myPath)
print(myParser.textBoxList[0].text)
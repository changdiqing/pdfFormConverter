from PyPDF2 import PdfFileWriter, PdfFileReader
import io
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter

class FormularLayerGenerator:

    def createFormLayer(self, pageSizeX, pageSizeY, coorList):
        packet = io.BytesIO()
        # create a new PDF with Reportlab
        can = canvas.Canvas('intermediate.pdf')#packet)#, pagesize=(595.28.0, 841.89.0))
        #can = canvas.Canvas(packet)#, pagesize=(595.28.0, 841.89.0))
        can.setPageSize((pageSizeX,pageSizeY))
        # can.drawString(10, 100, "Hello world")
        counter = 1
        extraBorderWidth = 3
        for i in coorList:
            can.acroForm.textfield(
                value='',
                x=i[0]-extraBorderWidth,y=i[1],
                width = i[2]-i[0]+ 2*extraBorderWidth, height = i[3]-i[1],
                name='tfield'+str(counter),
                fillColor=None,
                fontSize = 6,
                borderWidth = 0.1,
                tooltip = 'please enter a length in mm',
                forceBorder=True
            )
            counter += 1
        # can.acroForm.checkbox(
        #  name='er',
        #  tooltip='Field CB0',
        #  checked=True,
        #  x=72,y=72+4*36,
        #  buttonStyle='diamond',
        #  borderStyle='bevelled',
        #  borderWidth=2,
        #  # borderColor=red,
        #  # fillColor=green,
        #  # textColor=blue,
        #  forceBorder=True)
        can.save()

        #move to the beginning of the StringIO buffer
        packet.seek(0)
        return packet
        #new_pdf = PdfFileReader(packet)
        # read your existing PDF
        #existing_pdf = PdfFileReader(open("Untitled.pdf", "rb"))
        #output = PdfFileWriter()
        # add the "watermark" (which is the new pdf) on the existing page
        #page = existing_pdf.getPage(0)
        #print(page.mediaBox)
        #page.mergePage(new_pdf.getPage(0))
        #output.addPage(page)
        # finally, write "output" to a real file
        #outputStream = open("destination.pdf", "wb")
        #output.write(outputStream)
        #outputStream.close()

if __name__ == "__main__":
    coorList = [[176,758,213.1,775.795],[159,601,196.1,618.795],[159, 507, 196.1, 524.795],[159, 431, 196.1, 448.795]]
    print(coorList[0][0])
    FormularLayerGenerator().createFormLayer(595.28, 841.89, coorList)

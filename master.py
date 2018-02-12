from PyPDF2 import PdfFileWriter, PdfFileReader
import io
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter

packet = io.BytesIO()
# create a new PDF with Reportlab
can = canvas.Canvas('original.pdf')#, pagesize=(595.28.0, 841.89.0))
can.setPageSize((595.28,841.89))
print(letter)
# can.drawString(10, 100, "Hello world")
can.acroForm.textfield(
    value='',
    x=176,y=758,
    name='tfield',
    forceBorder=True)
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
#new_pdf = PdfFileReader(packet)
# read your existing PDF
existing_pdf = PdfFileReader(open("Untitled.pdf", "rb"))
output = PdfFileWriter()
# add the "watermark" (which is the new pdf) on the existing page
page = existing_pdf.getPage(0)
print(page.mediaBox)
#page.mergePage(new_pdf.getPage(0))
#output.addPage(page)
# finally, write "output" to a real file
#outputStream = open("destination.pdf", "wb")
#output.write(outputStream)
#outputStream.close()
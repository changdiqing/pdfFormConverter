#!/usr/bin/env python
import sys
import os.path
from PyPDF2 import PdfFileReader, PdfFileWriter, PdfFileMerger

def scannAttachments():
        fileNames = []
        for file in os.listdir("attachments"):
            if file.endswith(".pdf"):
                fileNames.append(os.path.join("attachments", file))
        print(fileNames)
        return fileNames

def pdf_cat(input_files, output_stream):
    input_streams = []
    try:
        # First open all the files, then produce the output file, and
        # finally close the input files. This is necessary because
        # the data isn't read from the input files until the write
        # operation. Thanks to
        # https://stackoverflow.com/questions/6773631/problem-with-closing-python-pypdf-writing-getting-a-valueerror-i-o-operation/6773733#6773733
        for input_file in input_files:
            input_streams.append(open(input_file))
        writer = PdfFileWriter()
        for reader in map(PdfFileReader, input_streams):
            for n in range(reader.getNumPages()):
                writer.addPage(reader.getPage(n))
        writer.write(output_stream)
    finally:
        for f in input_streams:
            f.close()

if __name__ == '__main__':
    fileNames = scannAttachments()
    #pdf_cat(['attachments/G17170085 Radiant Opto Taiwan.pdf'], 'test123455667.pdf')
    #pdf_cat(sys.argv[1:], sys.stdout
    pdfs = ['attachments/G17170085 Radiant Opto Taiwan copy 2.pdf', 'attachments/G17170085 Radiant Opto Taiwan copy 3.pdf', 'attachments/G17170085 Radiant Opto Taiwan copy.pdf', 'attachments/G17170085 Radiant Opto Taiwan.pdf', 'attachments/origina2l.pdf']

    pdf1 = ['intermediate2.pdf'] + pdfs
    merger = PdfFileMerger()

    for pdf in pdfs:
        merger.append(pdf)

    merger.write("result.pdf")
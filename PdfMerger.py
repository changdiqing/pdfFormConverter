#!/usr/bin/env python

'''
Simple example of watermarking using form xobjects (pdfrw).
usage:   watermark.py [-u] my.pdf single_page.pdf
Creates watermark.my.pdf, with every page overlaid with
first page from single_page.pdf.  If -u is selected, watermark
will be placed underneath page (painted first).
NOTE 1: This program assumes that all pages (including the watermark
        page) are the same size.  For other possibilities, see
        the fancy_watermark.py example.
NOTE 2: At one point, this example was extremely complicated, with
        multiple options.  That only led to errors in implementation,
        so it has been re-simplified in order to show basic principles
        of the library operation and to match the other examples better.
'''

import sys
import os
from PyQt5.QtWidgets import QApplication, QWidget, QInputDialog, QLineEdit, QFileDialog
from PyQt5.QtGui import QIcon
from pdfrw import PdfReader, PdfWriter, PageMerge

class PdfMerger(QWidget):
    def merge(self, layer1, layer2):
        #argv = sys.argv[1:]
        argv = [layer1,layer2]
        underneath = '-u' in argv
        if underneath:
            del argv[argv.index('-u')]
        inpfn, wmarkfn = argv
        wmark = PageMerge().add(PdfReader(wmarkfn).pages[0])[0]
        trailer = PdfReader(inpfn)
        for page in trailer.pages:
            PageMerge(page).add(wmark, prepend=underneath).render()

        #options = QFileDialog.Options()
        #options |= QFileDialog.DontUseNativeDialog
        #fileName, _ = QFileDialog.getSaveFileName(None,"QFileDialog.getSaveFileName()","","PDF (*.pdf)", options=options)
        #if fileName:
        #    PdfWriter(fileName, trailer=trailer).write()
        PdfWriter('intermediate2.pdf', trailer=trailer).write()

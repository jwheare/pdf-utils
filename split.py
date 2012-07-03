#!/usr/bin/env python

# http://pypi.python.org/pypi/fish/
# This is the only essential dependency
from fish import SwimFishProgressSync, SingleLineFishPrinter, Bird
import string
class YayLook(SingleLineFishPrinter):
    shape = " :D" # choose your own shape!
    trans = string.maketrans("/\[](){}<>76D", "\/][)(}{></9C")
    def render(self, step, reverse=False):
        
        rev_shape = self.shape.translate(self.trans)[::-1]
        return [rev_shape if reverse else self.shape]
    @property
    def own_length(self):
        return len(self.shape)

class ProgressYay(SwimFishProgressSync, YayLook):
    pass

# http://pybrary.net/pyPdf/
from pyPdf import PdfFileWriter, PdfFileReader

import sys, os, threading

"""
split.py

Split apart double page spreads in a PDF

Usage: ./split.py <pdf>
"""

input_file = sys.argv[1]
input_base, input_ext = os.path.splitext(input_file)

input_pdf = PdfFileReader(file(input_file, "rb"))
output_pdf = PdfFileWriter()

split_count = 0

pages = input_pdf.getNumPages()

progress = ProgressYay(total=pages)

for i in range(pages):
    p = input_pdf.getPage(i)
    
    x = p.mediaBox.getUpperRight_x()
    y = p.mediaBox.getUpperRight_y()
    
    if x > y:
        # Landscape page, split it in 2
        page1 = output_pdf.addBlankPage(x/2, y)
        page1.mergePage(p)
        
        page2 = output_pdf.addBlankPage(x/2, y)
        page2.mergeTranslatedPage(p, -x/2, 0)
        
        split_count = split_count + 1
    else:
        # Portrait, fine on its own
        output_pdf.addPage(p)
    
    progress.animate(amount=i)
    
progress.animate(amount=pages)

print 'Total pages: %d -> %d ' % (
    pages,
    output_pdf.getNumPages()
)
if split_count:
    print '/-{ %d }-\\ double spreads split apart' % split_count

print 'Writing... here is a bird to keep you company'

def write_file():
    # Write the file
    output_file = file(input_base + '.split' + input_ext, "wb")
    output_pdf.write(output_file)
    output_file.close()

t = threading.Thread(target=write_file)
t.start()

b = Bird(velocity=30)
while t.is_alive():
    b.animate()

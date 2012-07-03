#!/usr/bin/env python

# http://pybrary.net/pyPdf/
from pyPdf import PdfFileWriter, PdfFileReader

import sys, os

"""
filter.py

Filter out specific page numbers from a PDF

Usage: ./filter.py <pdf> page[ page ...]
"""

input_file = sys.argv[1]
input_base, input_ext = os.path.splitext(input_file)

input_pdf = PdfFileReader(file(input_file, "rb"))
output_pdf = PdfFileWriter()

to_remove = sys.argv[2:]

pages = input_pdf.getNumPages()

for i in range(pages):
    if str(i) not in to_remove:
        output_pdf.addPage(input_pdf.getPage(i))

print 'Total pages: %d -> %d' % (
    pages,
    output_pdf.getNumPages()
),

# Write the file
output_file = file(input_base + '.filtered' + input_ext, "wb")
output_pdf.write(output_file)
output_file.close()

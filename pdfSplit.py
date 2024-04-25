#!/usr/bin/env python3
# Description: Split the PDF file

from pypdf import PdfReader, PdfWriter
from pdfChecks import ValidPDF

class PdfSplit:
    """Split the PDF file in multiple pages"""
    def __init__(self, pdf_file):
        self.pdf_file = pdf_file

    def split(self):
        f_reader = PdfReader(self.pdf_file)
        custom_writer = ValidPDF()
        if not f_reader.is_encrypted:
            for _ in range(len(f_reader.pages)):
                f_write = PdfWriter()
                f_write.add_page(f_reader.pages[_])
                custom_writer.write_file(self.pdf_file, data=f_write, of=f"split-page-{_+1}-")
            print(f"{self.pdf_file} has been split out")
        else:
            print(f"{self.pdf_file} File encrypted, not possible to split it out.")

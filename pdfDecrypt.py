#!/usr/bin/env python3
# Description: Decrypt a PDF file

from pypdf import PdfReader, PdfWriter
from pdfChecks import ValidPDF

class Decrypt:
    """Decrypt PDF file using a known password"""
    def __init__(self, pdf_file, password):
        self._password = password
        self.pdf_file = pdf_file

    @property
    def password(self):
        return self._password

    def decrypt_pdf(self):
        try:
            f_read = PdfReader(self.pdf_file)
            f_write = PdfWriter()

            if f_read.is_encrypted:
                f_read.decrypt(self.password)

                # Add all pages to the writer
                for page in f_read.pages:
                    f_write.add_page(page)

                # Save the new PDF to a file
                custom_writer = ValidPDF()
                custom_writer.write_file(self.pdf_file, data=f_write, of="decrypted-")
                print(f'PDF decrypted!')
            else:
                print("PDF file has no password!")
        except:
            print("Check the password, file not decrypted.")

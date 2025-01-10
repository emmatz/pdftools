#!/usr/bin/env python3
# Description: Get information of PDF file

from pypdf import PdfReader
from datetime import datetime

class GeneralInformation:
    '''Getting PDF information'''
    def __init__(self, pdf_file):
        self.pdf_file = pdf_file

    def _read_file(self):
        pdf_read = PdfReader(self.pdf_file)
        if pdf_read.is_encrypted:
            print(f"File {self.pdf_file} is protected.")
            exit(6)
        return pdf_read

    def get_metadata(self):
        f_read = self._read_file()
        meta = f_read.metadata

        # def meta_or_default(value):
        #     return value if value is not None else "No information available."

        for k,v in f_read.metadata.items():
            if "date" in k[1:] or "Date" in k[1:]:
                v = datetime.strptime(v[2:].replace("'", ""), "%Y%m%d%H%M%S%z").strftime("%Y-%m-%d %H:%M:%S %z")
            print(f'{k[1:]}: {v}')
        # print(f'Title:    {meta_or_default(meta.title)}')
        # print(f'Subject:  {meta_or_default(meta.subject)}')
        # print(f'Author:   {meta_or_default(meta.author)}')
        # print(f'Creator:  {meta_or_default(meta.creator)}')
        # print(f'Producer: {meta_or_default(meta.producer)}')
        # print(f'Creation Date:     {meta_or_default(meta.creation_date)}')
        # print(f'Modification Date: {meta_or_default(meta.modification_date)}')

    def page_size(self, page=1):
        fpdf = self._read_file()
        target_page = fpdf.pages[page-1]
        print(f"Page {page} size:")
        print(f"\tWidth:   {target_page.mediabox.width} pts")
        print(f"\theight:  {target_page.mediabox.height} pts")
        # print(f"Artbox.")
        # print(f"\tLEFT:   {target_page.artbox.left}\n"
        #       f"\tRIGHT:  {target_page.artbox.right}\n"
        #       f"\tTOP:    {target_page.artbox.top}\n"
        #       f"\tBOTTOM: {target_page.artbox.bottom}")

        def box_info(box_name, box):
            """Helper function to print box details."""
            print(f'{box_name.capitalize()}:')
            print(f'\tLEFT:   {box.left}\n'
                  f'\tRIGHT:  {box.right}\n'
                  f'\tTOP:    {box.top}\n'
                  f'\tBOTTOM: {box.bottom}')

        # Print boxes information
        box_info("mediabox", target_page.mediabox)
        box_info("cropbox", target_page.cropbox)
        box_info("trimbox", target_page.trimbox)
        box_info("bleedbox", target_page.bleedbox)
        box_info("artbox", target_page.artbox)

    def total_pages(self):
        f_pdf = self._read_file()
        return len(f_pdf.pages)

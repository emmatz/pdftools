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

        def meta_or_default(value):
            return value if value is not None else "No information available."

        # for k,v in f_read.metadata.items():
        #     if "date" in k[1:] or "Date" in k[1:]:
        #         v  = datetime.strptime(v[2:].replace("'", ""), "%Y%m%d%H%M%S%z").strftime("%Y-%m-%d %H:%M:%S %z")
        #     print(f'{k[1:]}: {v}')
        print(f'Title:    {meta_or_default(meta.title)}')
        print(f'Subject:  {meta_or_default(meta.subject)}')
        print(f'Author:   {meta_or_default(meta.author)}')
        print(f'Creator:  {meta_or_default(meta.creator)}')
        print(f'Producer: {meta_or_default(meta.producer)}')
        print(f'Creation Date:     {meta_or_default(meta.creation_date)}')
        print(f'Modification Date: {meta_or_default(meta.modification_date)}')

    def page_size(self, page=1):
        fpdf = self._read_file()
        target_page = fpdf.pages[page-1]
        print(f"Page {page}.\nSize:")
        print(f"  Width:   {target_page.mediabox.width} pts")
        print(f"  height:  {target_page.mediabox.height} pts")
        print(f"Mediabox:")
        print(f"  LEFT:   {target_page.mediabox.left}\n"
              f"  RIGHT:  {target_page.mediabox.right}\n"
              f"  TOP:    {target_page.mediabox.top}\n"
              f"  BOTTOM: {target_page.mediabox.bottom}")

    def total_pages(self):
        f_pdf = self._read_file()
        return len(f_pdf.pages)

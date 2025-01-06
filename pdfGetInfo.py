#!/usr/bin/env python3
# Description: Get information of PDF file

from pypdf import PdfReader

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
        # for k,v in f_read.metadata.items():
        #     print(f'{k[1:]}: {v} ==> {type(v)}')
        print(f'Title:    {meta.title}')
        print(f'Subject:  {meta.subject}')
        print(f'Author:   {meta.author}')
        print(f'Creator:  {meta.creator}')
        print(f'Producer: {meta.producer}')
        print(f'Creation Date:     {meta.creation_date}')
        print(f'Modification Date: {meta.modification_date}')

    def page_size(self, page=1):
            fpdf = self._read_file()
            target_page = fpdf.pages[page-1]
            print(f"Page {page} size:")
            print(f"Width:   {target_page.mediabox.width} pts")
            print(f"height:  {target_page.mediabox.height} pts")

    def total_pages(self):
        f_pdf = self._read_file()
        return len(f_pdf.pages)
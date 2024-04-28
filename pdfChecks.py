#!/usr/bin/env python3
# Description: Validate if file is PDF, if exits and so on

import os
from pypdf import PdfReader
import glob

class ValidPDF:
    '''PDF file validation'''

    def file_exist(self, file):
        '''Checks if file exist'''
        if os.path.isfile(file):
            return True
        else:
            print(f'{file} does not exists.')
            return False

    def is_pdf(self, file):
        '''Checks if it's a valid PDF file'''
        if self.file_exist(file):
            try:
                f_read = PdfReader(file)
                if f_read.pdf_header[0:4] == "%PDF":
                    return True
            except:
                print(f'{file} is not a valid PDF file')
        return False

    def write_file(self, pdf_file, data, of="new-"):
        '''Writes the new PDF file'''
        full_path = os.path.join(os.path.dirname(pdf_file), of + os.path.basename(pdf_file))
        with open(full_path, "wb") as pf:
            data.write(pf)

    def is_encrypted(self, file):
        '''Check if the PDF has password'''
        f_read = PdfReader(file)
        if f_read.is_encrypted:
            return True
        return False

    def is_glob(self,args):
        '''Check if the argument should be expanded'''
        return glob.glob(args)


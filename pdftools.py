#!/usr/bin/env python3
# Author: emmatz
# Description: A comprehensive tool for PDF file management, including decryption, encryption, password cracking,
#               file rotation, merging, and more.

import argparse
from pdfEncrypt import Password, Encrypt
from pdfDecrypt import Decrypt
from pdfSplit import PdfSplit
from pdfCrack import Crack
from pdfChecks import ValidPDF
from pdfMerge import Merger
from pdfGetInfo import GeneralInformation
import re

class Menu:
    def __init__(self):
        self.args = self.menu()

    def menu(self):
        """Menu"""
        menu = argparse.ArgumentParser(description="Manipulate PDF files.",
                                       formatter_class=argparse.RawTextHelpFormatter)

        # Mutual exclusive
        group = menu.add_mutually_exclusive_group()
        group.add_argument('-c', metavar="file", nargs=2, help='Crack the PDF\'s password.\n'
                                                               '-c [PDF_FILE] [Dictionary]')
        group.add_argument('-d', metavar="data", nargs=2, help="Decrypt PDF file.\n"
                                               "-d [PDF_FILE] [PASSWORD]")
        group.add_argument('-e', metavar="file", help='Encrypt PDF file.')
        group.add_argument('-m', metavar="file", nargs="*", help='Merge PDF files.\n'
                                                                 '[PDF_FILES] [PDF_MERGED]')
        group.add_argument('-s', metavar="file", help='Split PDF file.')
        group.add_argument('-gm', metavar="file", help="Get metadata.\n"
                                                      "-gm [PDF_FILE]")
        group.add_argument('-sp', metavar="file", help="Get size of specific page.\n"
                                                      "-p [PDF_FILE] [Page_Number (Default=1)]")
        group.add_argument('-tp', metavar="file", help="Get total number of pages.\n"
                                                       "-tp [PDF_FILE]")
        menu.add_argument('-V', '--version', action='version', version='%(prog)s  [version 2.2]')

        return menu.parse_args()

class PdfTools:
    def __init__(self):
        self.menu_instance = Menu()

    def encrypt(self, pdf_file):
        if self.check(pdf_file):
            pwd = Password()
            answer = input('Do you like to generate the password automatically [y/n]: ')
            if answer.lower().strip() == 'y':
                password = pwd.generate_secure_password()
                print(f'PASS: {password}')
            else:
                pwd.password = None
            encrypter = Encrypt(pdf_file, pwd.password)
            encrypter.encrypt_pdf()

    def decrypt(self, pdf_file, password):
        if self.check(pdf_file):
            file_to_decrypt = Decrypt(pdf_file, password)
            file_to_decrypt.decrypt_pdf()

    def split(self, pdf_file):
        if self.check(pdf_file):
            pdf_split = PdfSplit(pdf_file)
            pdf_split.split()

    def crack(self, pdf_file, dict):
        if self.check(pdf_file):
            pdf_crack = Crack(pdf_file, dict)
            pdf_crack.crack()

    def metadata(self, pdf_file):
        if self.check(pdf_file):
            pdf_metadata = GeneralInformation(pdf_file)
            pdf_metadata.get_metadata()

    def page_size(self, pdf_file, page):
        if self.check(pdf_file):
            try:
                if page <= 0:
                    print(f"Page {page} doesn't exits.")
                    return
                psize = GeneralInformation(pdf_file)
                psize.page_size(page)
            except IndexError:
                print(f"Page {page} doesn't exits.")

    def total_page(self, pdf_file):
        if self.check(pdf_file):
            total = GeneralInformation(pdf_file)
            print(f"Number of pages: {total.total_pages()}")

    def merge(self, pdf_list):
        if len(pdf_list) < 2:
            print("Check help menu for details.")
            exit(4)

        pattern_expanded = []
        pdf = ValidPDF()

        # As Windows OS does not expand the wildcards automatically, we need to create a temporal file list
        # with absolute file paths
        for _ in pdf_list:
            if re.search(r'[\*\?\[\]]', _):
                pattern_expanded.append(pdf.is_glob(_))
            else:
                pattern_expanded.append(_)
        flat_list = [item for sublist in pattern_expanded for item in (sublist if isinstance(sublist, list) else [sublist])]
        del pattern_expanded

        # Checking if arguments are valid
        for file in flat_list[:len(flat_list)-1]:
            if not pdf.is_pdf(file):
                exit(2)
            if pdf.is_encrypted(file):
                print(f'Encrypted file: {file}')
                exit(3)

        merged = Merger(flat_list[:len(flat_list)-1], flat_list[-1])
        merged.merger()

    def check(self, file):
        '''Validate the PDF file'''
        pdf_file = ValidPDF()
        return pdf_file.is_pdf(file)

    def run(self):
        try:
            if self.menu_instance.args.e:
                self.encrypt(self.menu_instance.args.e)
            if self.menu_instance.args.d:
                self.decrypt(self.menu_instance.args.d[0], self.menu_instance.args.d[1])
            if self.menu_instance.args.s:
                self.split(self.menu_instance.args.s)
            if self.menu_instance.args.c:
                self.crack(self.menu_instance.args.c[0], self.menu_instance.args.c[1])
            if self.menu_instance.args.m:
                self.merge(self.menu_instance.args.m)
            if self.menu_instance.args.gm:
                self.metadata(self.menu_instance.args.gm)
            if self.menu_instance.args.sp:
                self.page_size(self.menu_instance.args.sp, 1)
            if self.menu_instance.args.tp:
                self.total_page(self.menu_instance.args.tp)
        except (KeyboardInterrupt, EOFError, FileNotFoundError) as e:
            print(f'\n{type(e).__name__}')
            # print(e)


if __name__ == '__main__':
    a = PdfTools()
    a.run()
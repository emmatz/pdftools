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

class Menu:
    def __init__(self):
        self.args = self.menu()

    def menu(self):
        """Menu"""
        menu = argparse.ArgumentParser(description="Manipulate PDF files.",
                                       formatter_class=argparse.RawTextHelpFormatter)

        # Mutual exclusive
        group = menu.add_mutually_exclusive_group()
        group.add_argument('-d', metavar="data", nargs=2, help="Decrypt PDF file.\n"
                                               "-d [PDF_FILE] [PASSWORD]")
        group.add_argument('-e', metavar="file", help='Encrypt PDF file.')
        group.add_argument('-c', metavar="file", nargs=2, help='Crack the PDF\'s password.\n'
                                                               '-c [PDF_FILE] [Dictionary]')
        group.add_argument('-s', metavar="file", help='Split PDF file.')
        menu.add_argument('-V', '--version', action='version', version='%(prog)s  [version 2.1]')

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
        except (KeyboardInterrupt, EOFError, FileNotFoundError) as e:
            print(f'\n{type(e).__name__}')
            # print(e)


if __name__ == '__main__':
    a = PdfTools()
    a.run()
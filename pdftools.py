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
from pdfModify import Transform
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
        group.add_argument('-c', metavar=("[file]", "[dictionary]"), nargs=2,
                           help="Crack the PDF's password.")
        group.add_argument('-d', metavar=("[file]", "[password]"), nargs=2, help="Decrypt PDF file.")
        group.add_argument('-e', metavar="[file]", help='Encrypt PDF file.')
        group.add_argument('-m', metavar=("file"), nargs="*", help='Merge PDF files.\n'
                                                                 '[PDF_FILES] [PDF_MERGED]')
        group.add_argument('-s', metavar="[file]", help='Split PDF file.')
        group.add_argument('-gm', metavar="[file]", help="Get metadata.")
        group.add_argument('-sp', metavar=("file", "page_num"), nargs='+',
                           help="Get size of specific page. Default page 1.")
        group.add_argument('-tp', metavar="[file]", help="Get total number of pages.")
        group.add_argument('-scale-factor', metavar=("[file]", "[page]","[factor_rate]"), nargs=3,
                           help="Scale a PDF page by factor.\n"
                                " -scale-factor test.pdf 3 0.5")
        group.add_argument('-scale-wh', metavar=("[file]", "[page]", "[width]", "[height]"), nargs=4,
                           help="Scale a PDF page specifying WIDTH and HEIGHT values.\n"
                                " -scale-wh test.pdf 3 850.5 950.0")
        group.add_argument('-resize',
                           metavar=("[file]","[page]","[left_size]","[bottom_size]","[right_size]","[top_size]"),
                           nargs=6,
                           help="Resize manually a page. You need to specify values of Mediabox, Cropbox, Trimbox, "
                                "Bleedbox and Artbox.\nAll of them will have same values for LEFT, BOTTOM, "
                                "RIGHT and TOP\n"
                                "Mediabox: Defines the total area of the page, including all visible and invisible "
                                "content.\n\tIt is the largest box and represents the dimensions of the document.\n"
                                "Cropbox: Defines the visible area of the page.\n"
                                "\tOnly the content within the Cropbox is visible when the PDF is displayed or printed."
                                "\n\tIt is a sub-box of the Mediabox.\n"
                                "Trimbox: Specifies the boundaries of the page after trimming, typically for printing."
                                "\n\tIt is commonly used to adjust margins for production purposes.\n"
                                "Bleedbox: Defines the bleed area.\n\tIt is used when the page content needs to "
                                "extend beyond the edge to ensure there\n\tare no white borders after trimming.\n"
                                "Artbox: Defines the area that contains the visual content or layout of the page.")
        group.add_argument('-rotate', metavar=("[file]", "[page]", "[degrees]"), nargs=3,
                           help="Rotate a page of a PDF file.\n"
                                "It is a clockwise rotation of the page by multiples of 90 degrees.")
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
                    raise IndexError(f"Page {page} doesn't exist.")
                    # print(f"Page {page} doesn't exist.")
                    # return
                psize = GeneralInformation(pdf_file)
                psize.page_size(page)
            except IndexError:
                print(f"Page {page} doesn't exist.")

    def total_page(self, pdf_file):
        if self.check(pdf_file):
            total = GeneralInformation(pdf_file)
            print(f"Number of pages: {total.total_pages()}")

    def merge(self, pdf_list):
        if len(pdf_list) < 2:
            raise ValueError(f'Check help menu for details.')
            # print("Check help menu for details.")
            # exit(4)

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

    def scaleFactor(self, pdf_file):
        if self.check(pdf_file):
            Transform.scale(pdf_file, )

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
                if len(self.menu_instance.args.sp) == 1:
                    self.page_size(self.menu_instance.args.sp[0], 1)
                elif len(self.menu_instance.args.sp) == 2:
                    self.page_size(self.menu_instance.args.sp[0], int(self.menu_instance.args.sp[1]))
                else:
                    print("-sp accepts at most 2 arguments: [PDF_FILE] [Page_Number]")
            if self.menu_instance.args.tp:
                self.total_page(self.menu_instance.args.tp)
            if self.menu_instance.args.scale_factor:
                if self.check(self.menu_instance.args.scale_factor[0]):
                    Transform.scale(input_pdf=self.menu_instance.args.scale_factor[0],
                                    page_number=int(self.menu_instance.args.scale_factor[1]),
                                    scale_factor=float(self.menu_instance.args.scale_factor[2]))
            if self.menu_instance.args.scale_wh:
                if self.check(self.menu_instance.args.scale_wh[0]):
                    Transform.scale(input_pdf=self.menu_instance.args.scale_wh[0],
                                    page_number=int(self.menu_instance.args.scale_wh[1]),
                                    new_width=float(self.menu_instance.args.scale_wh[2]),
                                    new_height=float(self.menu_instance.args.scale_wh[3]))
            if self.menu_instance.args.resize:
                if self.check(self.menu_instance.args.resize[0]):
                    Transform.resize(input_pdf=self.menu_instance.args.resize[0],
                                     page_number=int(self.menu_instance.args.resize[1]),
                                     left_pt=float(self.menu_instance.args.resize[2]),
                                     bottom_pt=float(self.menu_instance.args.resize[3]),
                                     right_pt=float(self.menu_instance.args.resize[4]),
                                     top_pt=float(self.menu_instance.args.resize[5]))
            if self.menu_instance.args.rotate:
                if self.check(self.menu_instance.args.rotate[0]):
                    Transform.rotate(input_file=self.menu_instance.args.rotate[0],
                                     page_number=int(self.menu_instance.args.rotate[1]),
                                     degrees=int(self.menu_instance.args.rotate[2]))
        except (KeyboardInterrupt, EOFError, FileNotFoundError, ValueError, IndexError, PermissionError) as e:
            print(f'{type(e).__name__}: {e}')
            # print(e)


if __name__ == '__main__':
    a = PdfTools()
    a.run()
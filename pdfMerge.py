#!/usr/bin/env python3
# Description: Merge PDF files

from pypdf import PdfWriter
import os


class Merger:
    '''
    Merge PDF files

    :param files: List PDF files
    :param merged_file: Name of new merged file
    :return: None
    '''

    def __init__(self, files, merged_file):
        self._files = files
        self._merged_file = merged_file

    @property
    def files(self):
        return self._files

    @property
    def merged_file(self):
        return self._merged_file

    @merged_file.setter
    def merged_file(self, value):
        self._merged_file = value

    def merger(self):
        merger = PdfWriter()
        for pdf in self.files:
            merger.append(pdf)

        # Check if the file has PDF extension, if not it's added
        f_name, ext = os.path.splitext(self.merged_file)
        if not ext:
            self.merged_file += ".pdf"

        # if merged file's name exist, raise an error and exit
        if os.path.isfile(self.merged_file):
            print(f'{self.merged_file} Already exist, nothing changed.')
            exit(5)

        # Checking if the path is specified
        if not os.path.isabs(self.merged_file):
            with open(os.path.join(os.getcwd(), self.merged_file), "wb") as f:
                merger.write(f)
            print(f'{os.path.join(os.getcwd(), self.merged_file)} created.')
        # Check if path exists
        elif os.path.isabs(self.merged_file):
            if os.path.exists(os.path.dirname(self.merged_file)):
                with open(self.merged_file, "wb") as f:
                    merger.write(f)
                print(f'{self.merged_file} created.')
            else:
                print(f'{os.path.dirname(self.merged_file)} directory does not exist!')


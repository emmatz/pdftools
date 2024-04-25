#!/usr/bin/env python3
# Description: Cracking the PDF file

from pypdf import PdfReader

class Crack:
    '''Dictionary attack'''
    def __init__(self, pdf_file, dictionary):
        self.pdf_file = pdf_file
        self.dictionary = dictionary

    def crack(self):
        cnt = 0
        with open(self.pdf_file, 'rb') as file:
            pdf = PdfReader(file)
            if pdf.is_encrypted:
                with open(self.dictionary, 'r') as f:
                    for word in f:
                        cnt += 1
                        print(f"\rAttempts: {cnt}", end="", flush=True)
                        word = word.strip()
                        if pdf.decrypt(word):
                            print(f"\nPassword found: {word}")
                            break
                    else:
                        print(f"\nPassword not found!")
            else:
                print(f"{self.pdf_file} Not encrypted file")

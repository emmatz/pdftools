# pdftools

## Description

With this tool you'll be able to split, merge, rotate, encrypt, decrypt and crack the password of a PDF file. Cracking the password is based in a dictionary attack, you should use your own dictionary. 

Actually there are many online services to do the same, the advantage of tool is that you won't upload your personal information to a third party service.

This initial version of the tool does not check if the file to be process is a real PDF file, it's assumed you will be working with a PDF file. Also the original PDF file is not deleted, instead a copy of the file is created with
the requested modification (merge, decrypt, rotate, etc).

**== DECRYPT PDF.** You need to provide the PDF's password and then a copy of the file is created without password.

**== ENCRYPT PDF.** A new protected PDF file is created with the password you set.

**== MERGE PDF.** Concatenate pages from PDF files into a single PDF file

**== CRACK PDF.** It is needed a dictionary to crack the PDF, if the password is found, it will be shown on the screen.

**== ROTATE PDF.** You can rotete a scpecific page of the PDF in clockwise sense.

## Usage

```bash
python pdftools.py -h

usage: pdftools.py [-h] [-d data data | -e file | -c file file | -s file] [-V]

Manipulate PDF files.

options:
  -h, --help     show this help message and exit
  -d data data   Decrypt PDF file.
                 -d [PDF_FILE] [PASSWORD]
  -e file        Encrypt PDF file.
  -c file file   Crack the PDF's password.
                 -c [PDF_FILE] [Dictionary]
  -s file        Split PDF file.
  -V, --version  show program's version number and exit

```

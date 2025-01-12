# pdftools

## Description


With this tool, you'll be able to split, merge, rotate, encrypt, decrypt, and attempt to crack the password of a PDF file.
Password cracking is performed using a dictionary attack, and you will need to provide your own dictionary for this process.

While many online services offer similar functionality, the advantage of this tool lies in its offline nature, ensuring that you won't need to upload your personal information or files to a third-party service.

This wrapper operates under the assumption that a valid PDF file will be provided. Furthermore, the original PDF file remains intact throughout the process. A modified copy of the file (e.g., merged, decrypted, rotated, etc.) is created to reflect the requested changes, ensuring the original file is preserved.


**== DECRYPT PDF.** You need to provide the PDF's password and then a copy of the file is created without password.

**== ENCRYPT PDF.** A new protected PDF file is created with the password you set.

**== MERGE PDF.** Concatenate pages from PDF files into a single PDF file

**== CRACK PDF.** It is needed a dictionary to crack the PDF, if the password is found, it will be shown on the screen.

**== ROTATE PDF.** You can rotete a scpecific page of the PDF in clockwise sense.

== SCALE PDF. You can modify the page size either by scaling it using a factor or by specifying width and height values.

== RESIZE PDF. You can resize a page by adjusting the mediabox, cropbox, trimbox, bleedbox, and artbox.


## Usage

```bash

python pdftools.py -h
usage: pdftools.py [-h] [-c [file] [dictionary] | -d [file] [password] | -e [file] | -m [file ...] | -s [file] | -gm [file] | -sp file [page_num ...] | -tp [file] | -scale-factor [file] [page]
                   [factor_rate] | -scale-wh [file] [page] [width] [height] | -resize [file] [page] [left_size] [bottom_size] [right_size] [top_size] | -rotate [file] [page] [degrees]] [-V]

Manipulate PDF files.

options:
  -h, --help            show this help message and exit
  -c [file] [dictionary]
                        Crack the PDF's password.
  -d [file] [password]  Decrypt PDF file.
  -e [file]             Encrypt PDF file.
  -m [file ...]         Merge PDF files.
                        [PDF_FILES] [PDF_MERGED]
  -s [file]             Split PDF file.
  -gm [file]            Get metadata.
  -sp file [page_num ...]
                        Get size of specific page. Default page 1.
  -tp [file]            Get total number of pages.
  -scale-factor [file] [page] [factor_rate]
                        Scale a PDF page by factor.
                         -scale-factor test.pdf 3 0.5
  -scale-wh [file] [page] [width] [height]
                        Scale a PDF page specifying WIDTH and HEIGHT values.
                         -scale-wh test.pdf 3 850.5 950.0
  -resize [file] [page] [left_size] [bottom_size] [right_size] [top_size]
                        Resize manually a page. You need to specify values of Mediabox, Cropbox, Trimbox, Bleedbox and Artbox.
                        All of them will have same values for LEFT, BOTTOM, RIGHT and TOP
                        Mediabox: Defines the total area of the page, including all visible and invisible content.
                                It is the largest box and represents the dimensions of the document.
                        Cropbox: Defines the visible area of the page.
                                Only the content within the Cropbox is visible when the PDF is displayed or printed.
                                It is a sub-box of the Mediabox.
                        Trimbox: Specifies the boundaries of the page after trimming, typically for printing.
                                It is commonly used to adjust margins for production purposes.
                        Bleedbox: Defines the bleed area.
                                It is used when the page content needs to extend beyond the edge to ensure there
                                are no white borders after trimming.
                        Artbox: Defines the area that contains the visual content or layout of the page.
  -rotate [file] [page] [degrees]
                        Rotate a page of a PDF file.
                        It is a clockwise rotation of the page by multiples of 90 degrees.
  -V, --version         show program's version number and exit


```

#!/usr/bin/env python3
# Description: Transforming PDF file
#              https://pypdf.readthedocs.io/en/latest/user/cropping-and-transforming.html

from pypdf import PdfReader, PdfWriter
from pypdf.generic import RectangleObject
from pdfChecks import ValidPDF
import os

class Transform:
    @staticmethod
    def _check_encryption(input_pdf):
        '''
        Verifies if the PDF is encrypted and raises an error if so.
        :param input_pdf: PDF file
        :type input_pdf: str
        :return:
        :rtype:
        '''
        if ValidPDF().is_encrypted(input_pdf):
            raise PermissionError(f"The file '{input_pdf}' is password-protected and cannot be processed.")

    @staticmethod
    def _write_output_pdf(input_pdf, writer, prefix):
        '''
        Writes the output PDF to the same directory as the input with a given prefix.

        :param input_pdf: PDF file
        :type input_pdf: str
        :param writer: PdfWriter object with the modified PDF.
        :type writer: PdfWriter
        :param prefix: Prefix for the output file name.
        :type prefix: str
        :return: Path to the saved PDF file.
        :rtype: str
        '''

        output_file = os.path.join(os.path.dirname(input_pdf), f'{prefix}-{os.path.basename(input_pdf)}')
        with open(output_file, "wb") as output_file:
            writer.write(output_file)

        print(f"New PDF saved: {output_file.name}")

        return output_file

    @staticmethod
    def scale(input_pdf, page_number, scale_factor=None, new_width=None, new_height=None):
        '''
        Scale a specific page on a PDF file.

        :param input_pdf: PDF source
        :type input_pdf: str
        :param page_number: Page number
        :type page_number: int
        :param scale_factor: Scaling factor. Example 2.0 doubles the size, 0.5 reduces it by half.
        :type scale_factor: float
        :param new_width: New width in points (optional if scale_factor is provided)
        :type new_width: float
        :param new_height: New height in points (optional if scale_factor is provided).
        :type new_height: float
        :return: Path to the saved PDF file.
        :rtype: str
        '''

        # if ValidPDF().is_encrypted(input_pdf):
        #     print(f"File {input_pdf} is protected.")
        #     exit(7)
        Transform._check_encryption(input_pdf)

        reader = PdfReader(input_pdf)
        writer = PdfWriter()

        if page_number > len(reader.pages):
            raise IndexError(f"Page {page_number} doesn't exist.")

        # Iterate through the pages of the PDF
        for i, page in enumerate(reader.pages):
            if i == page_number-1:
                if scale_factor:
                    page.scale_by(scale_factor)
                elif new_width and new_height:
                    page.scale_to(new_width, new_height)
                else:
                    raise ValueError("You must provide either 'scale_factor' or both 'new_width' and 'new_height'.")

            # Add the page to the final PDF
            writer.add_page(page)

        # with open(os.path.join(os.path.dirname(input_pdf), "scaled-" + os.path.basename(input_pdf)), "wb") as f:
        #     writer.write(f)
        return ValidPDF().write_file(input_pdf, writer, prefix="scaled")
        # return  Transform._write_output_pdf(input_pdf, writer, prefix="scaled")

    @staticmethod
    def resize(input_pdf, page_number, left_pt=0, bottom_pt=0, right_pt=0, top_pt=0):
        '''
        Scaling a page with more control of all its components

        :param input_pdf: PDF file
        :type input_pdf: str
        :param page_number: Page to resize
        :type page_number: int
        :param left_pt: New points to be either added or removed
        :type left_pt: float
        :param bottom_pt: New points to be either added or removed
        :type bottom_pt: float
        :param right_pt: New points to be either added or removed
        :type right_pt: float
        :param top_pt: New points to be either added or removed
        :type top_pt: float
        :return: Path to the saved PDF file
        :rtype: str
        '''

        # Mediabox:
        #  > Defines the total area of the page, including all visible and invisible content.
        #  > It is the largest box and represents the dimensions of the document.
        #
        # Cropbox:
        #  > Defines the visible area of the page.
        #  > It is a sub-box of the Mediabox. Only the content within the Cropbox is
        #  visible when the PDF is displayed or printed.
        #
        # Trimbox:
        #  > Specifies the boundaries of the page after trimming, typically for printing.
        #  > It is commonly used to adjust margins for production purposes.
        #
        # Bleedbox:
        #  > Defines the bleed area. It is used when the page content needs to extend beyond
        #  the edge to ensure there are no white borders after trimming.
        #
        # Artbox:
        #  > Defines the area that contains the visual content or layout of the page.

        # if ValidPDF().is_encrypted(input_pdf):
        #     print(f"File {input_pdf} is protected.")
        #     exit(8)
        Transform._check_encryption(input_pdf)

        reader = PdfReader(input_pdf)
        writer = PdfWriter()

        # Page to scale
        page = reader.pages[page_number-1]

        # Current page's dimensions
        mb = page.mediabox

        for boxes in ('mediabox', 'cropbox', 'trimbox', 'bleedbox', 'artbox'):
            setattr(page, boxes, RectangleObject((mb.left + left_pt, mb.bottom + bottom_pt,
                                                  mb.right + right_pt, mb.top + top_pt)))
        # print(f'mediabox: {page.mediabox}\n'
        #       f'cropbox:  {page.cropbox}\n'
        #       f'trimbox:  {page.trimbox}\n'
        #       f'bleedbox: {page.bleedbox}\n'
        #       f'artbox:   {page.artbox}')

        # Storing page modified
        writer.add_page(page)

        # with open(os.path.join(os.path.dirname(input_pdf), "resized-page-" + str(page_number) + "-"
        #                                                    + os.path.basename(input_pdf)), "wb") as f:
        #     writer.write(f)
        return ValidPDF().write_file(input_pdf, writer, prefix=f'resized-page-{page_number}')
        # return Transform._write_output_pdf(input_pdf, writer, prefix=f'resized-page-{page_number}')

    @staticmethod
    def rotate(input_file, page_number, degrees=0):
        '''
        Rotate a page
        :param input_file: PDF file
        :type input_file: str
        :param page_number: Page to be rotated
        :type page_number: int
        :param degrees: Multiples of 90 (Clockwise rotation)
        :type degrees: int
        :return: Path to the saved PDF file
        :rtype: str
        '''
        Transform._check_encryption(input_file)

        reader = PdfReader(input_file)
        writer = PdfWriter()

        writer.add_page(reader.pages[page_number-1])
        writer.pages[(page_number-1)].rotate(degrees)
        return ValidPDF().write_file(input_file, writer, prefix=f"rotated-page-{page_number}")

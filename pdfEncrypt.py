#!/usr/bin/env python3
# Description: Protect a PDF file with password

import getpass
import secrets
import string
from pypdf import PdfReader, PdfWriter
from pdfChecks import ValidPDF


class Password:
	''' Set or generate a secure password '''

	def __init__(self):
		self._password = None

	@property
	def password(self):
		"""Getting password."""
		return self._password

	@password.setter
	def password(self, value):
		"""Setting password with validation."""
		try:
			if not value:
				value = getpass.getpass('Password: ')

			if not value.strip():
				raise ValueError("Password cannot be empty!")

			if len(value.strip()) < 10:
				raise ValueError("Password must be at least 10 characters long.")

			self._password = value
		except Exception as error:
			print(f'An error occurred: {error}')

	def generate_secure_password(self):
		"""Generates a secure password."""
		alphabet = string.printable[0:-6]
		self._password = ''.join(secrets.choice(alphabet) for _ in range(10))
		return self._password


class Encrypt:
	"""Encrypt the PDF file"""
	def __init__(self, pdf_file, password):
		self.pdf_file = pdf_file
		self.password = password

	def encrypt_pdf(self):
		f_read = PdfReader(self.pdf_file)
		f_write = PdfWriter()

		if self.password == None or len(self.password) < 10:
			exit(1)

		# Add all pages to the writer
		for page in f_read.pages:
			f_write.add_page(page)

		# Add a password to the new PDF
		f_write.encrypt(self.password, algorithm="AES-256")

		custom_writer = ValidPDF()
		custom_writer.write_file(self.pdf_file, data=f_write, of="encrypted-")
# setup.py
from setuptools import setup, find_packages

setup(
    name="pdftool",
    version="2.1",
    packages=find_packages(),
    entry_points={
        "console_scripts": [
            "pdftool_cli = pdftools.__main__:pdftools",
        ],
      },
)
# tools/__init__.py
# This file marks the tools directory as a Python package and can be used to register tool functions for AI agents.

from .csvParser import get_csv_data
from .pdfParser import get_pdf_text

def parse_file_by_type(path: str, extension: str) -> str:
    """
    Segregate file parsing by type for AI agent tools.
    """
    if extension == ".csv":
        return get_csv_data(path)
    elif extension == ".pdf":
        return get_pdf_text(path)
    else:
        with open(path, 'r', encoding='utf-8', errors='ignore') as f:
            return f.read()

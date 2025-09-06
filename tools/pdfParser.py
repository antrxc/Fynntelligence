from PyPDF2 import PdfReader

def get_pdf_text(path:str) -> str:
    reader = PdfReader(path)
    data = ""
    for page in reader.pages:
        text = page.extract_text()
        if text:
            data += text
        data += "\n======= PAGE BREAK =======\n"
    return data

    


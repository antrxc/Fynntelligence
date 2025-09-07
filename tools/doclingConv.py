from docling.document_converter import DocumentConverter

def DocConvert(url):
    converted = DocumentConverter()
    result = converted.convert(url)
    return result.document.export_to_markdown() 
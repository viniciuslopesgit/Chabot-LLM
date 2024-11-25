import pymupdf

# Extrai texto do ficheiro .pdf
def pdf_extract():
    doc = pymupdf.open("pdf/pdf/manual_inst_6.0_PT.pdf")
    out = open("pdf/txt/output.txt", "wb")
    for page in doc:
        text = page.get_text().encode("utf8")
        out.write(text)
        out.write(bytes((12,)))
    out.close()
import pymupdf

def pdf_extract():
    doc = pymupdf.open("pdf/pdf/manual_inst_6.0_PT.pdf")
    with open("pdf/txt/output.txt", "w", encoding="utf-8") as out:
        for page in doc:
            text = page.get_text()
            out.write(text)
            out.write("\n" + "="*80 + "\n")  # Adiciona uma linha separadora entre páginas, se necessário

    print("Texto extraído com sucesso para pdf/txt/output.txt")

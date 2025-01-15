import re
import textwrap

def formatar_texto(texto, largura=100):
    paragrafos = texto.strip().split("\n")
    texto_formatado = []
    for paragrafo in paragrafos:
        if re.match(r"^\d+\.", paragrafo.strip()) or re.match(r"^- ", paragrafo.strip()):
            itens = re.split(r"(\d+\..*?)(?=\d+\.)", paragrafo)
            for item in itens:
                if item.strip():
                    texto_formatado.append(f"<p>{textwrap.fill(item.strip(), width=largura)}</p>")
        else:
            texto_formatado.append(f"<p>{textwrap.fill(paragrafo.strip(), width=largura)}</p>") 
    return "\n".join(texto_formatado)


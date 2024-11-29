import re
import textwrap

def formatar_texto(texto, largura=80):
    """Formata o texto para melhor apresentação."""
    paragrafos = texto.strip().split("\n")
    texto_formatado = []

    for paragrafo in paragrafos:
        # Detecta listas numeradas ou com marcadores
        if re.match(r"^\d+\.", paragrafo.strip()) or re.match(r"^- ", paragrafo.strip()):
            itens = re.split(r"(\d+\..*?)(?=\d+\.)", paragrafo)
            for item in itens:
                if item.strip():
                    # Adiciona tags HTML para listas
                    texto_formatado.append(f"<p>{textwrap.fill(item.strip(), width=largura)}</p>")
        else:
            # Formata parágrafos normais
            texto_formatado.append(f"<p>{textwrap.fill(paragrafo.strip(), width=largura)}</p>")
    
    # Junta os parágrafos com uma linha em branco
    return "\n".join(texto_formatado)


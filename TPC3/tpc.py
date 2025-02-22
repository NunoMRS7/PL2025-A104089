import sys
import re

regexCabecalho = re.compile(r'^(#{1,3})\s*(.+)')
regexBold = re.compile(r'(\*\*)([^\*]*)(\1)')
regexItalic = re.compile(r'(\*)([^\*]*)(\1)')
regexLista = re.compile(r'\d\.\s+(.*)')
regexImagem = re.compile(r'!\[([^\]]*)\]\(([^\)]+)\)')
regexLink = re.compile(r'\[([^\]]*)\]\(([^\)]+)\)')

linhaAnteriorEraLista = "OFF"

for linha in sys.stdin:
    if regexLista.search(linha):
        if linhaAnteriorEraLista == "ON": # verificar se a linha atual não é a primeira linha da lista
            print(regexLista.sub(r'<li>\1</li>', linha), end="")
        elif linhaAnteriorEraLista == "OFF": # verificar se a linha atual é a primeira linha da lista
            print("<ol>")
            print(regexLista.sub(r'<li>\1</li>', linha), end="")
        linhaAnteriorEraLista = "ON" # atualizar linhaAnteriorEraLista para ON para a próxima leitura
    else:
        if linhaAnteriorEraLista == "ON": # verificar se a linha atual procede uma linha que pertencia a uma lista
            print("</ol>")
            linhaAnteriorEraLista = "OFF" # atualizar linhaAnteriorEraLista para OFF para a próxima leitura

        if res := regexCabecalho.search(linha):
            nivelCabecalho = len(res.group(1))
            print(regexCabecalho.sub(lambda m: f'<h{nivelCabecalho}>{m.group(2)}</h{nivelCabecalho}>', linha), end="")
        elif regexBold.search(linha):
            print(regexBold.sub(r'<b>\2</b>', linha), end="")
        elif regexItalic.search(linha):
            print(regexItalic.sub(r'<i>\2</i>', linha), end="")
        elif regexImagem.search(linha):
            print(regexImagem.sub(r'<img src="\2" alt="\1"/>', linha), end="")
        elif regexLink.search(linha):
            print(regexLink.sub(r'<a href="\2">\1</a>', linha), end="")

print("")
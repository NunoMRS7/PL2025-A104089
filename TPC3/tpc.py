import sys
import re

regexCabecalho = re.compile(r'^(#{1,3})\s*(.+)')
regexBold = re.compile(r'(\*\*)([^\*\*]+)(\1)')
regexItalic = re.compile(r'(\*)([^\*]+)(\1)')
regexLista = re.compile(r'\d\.\s+(.*)')
regexImagem = re.compile(r'!\[([^\]]*)\]\(([^\)]+)\)')
regexLink = re.compile(r'\[([^\]]*)\]\(([^\)]+)\)')

linhaAnteriorEraLista = False

linhaOutput = ""

for linha in sys.stdin:
    
    linhaOutput = linha

    if regexLista.search(linhaOutput):
        if not linhaAnteriorEraLista: # verificar se a linha atual é a primeira linha da lista
            print("<ol>")
        linhaOutput = regexLista.sub(r'<li>\1</li>', linhaOutput)
        linhaAnteriorEraLista = True # atualizar linhaAnteriorEraLista para ON para a próxima leitura
    else:
        if linhaAnteriorEraLista: # verificar se a linha atual procede uma linha que pertencia a uma lista
            print("</ol>")
            linhaAnteriorEraLista = False # atualizar linhaAnteriorEraLista para OFF para a próxima leitura

        if res := regexCabecalho.search(linhaOutput):
            nivelCabecalho = len(res.group(1))
            linhaOutput = regexCabecalho.sub(lambda m: f'<h{nivelCabecalho}>{m.group(2)}</h{nivelCabecalho}>', linhaOutput)
        if regexBold.search(linhaOutput):
            linhaOutput = regexBold.sub(r'<b>\2</b>', linhaOutput)
        if regexItalic.search(linhaOutput):
            linhaOutput = regexItalic.sub(r'<i>\2</i>', linhaOutput)
        if regexImagem.search(linhaOutput):
            linhaOutput = regexImagem.sub(r'<img src="\2" alt="\1"/>', linhaOutput)
        if regexLink.search(linhaOutput):
            linhaOutput = regexLink.sub(r'<a href="\2">\1</a>', linhaOutput)
    
    print(linhaOutput, end="")

print("")
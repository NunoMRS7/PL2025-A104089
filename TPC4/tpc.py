import sys
import re

comentario = re.compile(r'^#.*')
palavraChave = re.compile(r'select|SELECT|where|WHERE|limit|LIMIT') # DÚVIDA - está bem? !!!!!!!!!
variavel = re.compile(r'\?\w+')
simbolo = re.compile(r'[.{}]') # DÚVIDA - está bem? !!!!!!!!!
atributo = re.compile(r'\w+:\w+') # DÚVIDA - está bem? !!!!!!!!!
string = re.compile(r'"[^"]+"')
tagIdioma = re.compile(r'@\w+') # DÚVIDA - é necessário? !!!!!!!!!
numero = re.compile(r'\d+')

# FALTA APANHAR O 'a' da primeira linha após chaveta

res = []

for linha in sys.stdin:
    # comentários
    cmt = comentario.search(linha)
    if cmt: res.append((cmt.group(0),"COMMENT"))
    
    # palavras chave
    for pc in palavraChave.findall(linha):
        res.append((pc,"KEYWORD"))

    # variaveis
    for v in variavel.findall(linha):
        res.append((v,"VARIABLE"))
    
    # simbolos
    for s in simbolo.findall(linha):
        res.append((s,"SIMBOL"))

    # atributos
    for a in atributo.findall(linha):
        res.append((a,"ATRIBUTE"))

    # strings
    for str in string.findall(linha):
        res.append((str,"STRING"))

    # tags de idioma
    for ti in tagIdioma.findall(linha):
        res.append((ti,"TAG"))
    
    # números
    for n in numero.findall(linha):
        res.append((n,"NUMBER"))

for r in res:
    print(r)
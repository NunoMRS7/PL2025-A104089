import sys
import re


def tokenize(content):

    token_specification = [
        ('COMMENT', r'^#.*'),
        ('STRING', r'"[^"]+"'),
        ('TAG', r'@\w+'),
        ('VARIABLE', r'\?\w+'),
        ('NUM', r'\d+'),
        ('DOT', r'\.'),
        ('LBRACE', r'{'),
        ('RBRACE', r'}'),
        ('COLON', r'\:'),
        ('PREFIX', r'(?P<left>\w+)(?=:)'),
        ('TERM', r'(?<=:)(?P<right>\w+)'),
        ('KEYWORD', r'[a-zA-Z]+'),
        ('NEWLINE', r'\n'),
        ('SKIP', r'[ \t]+'),
        ('ERROR', r'.')
    ]

    token_regex = '|'.join([f'(?P<{id}>{expreg})' for (id,expreg) in token_specification])

    res = []
    lineNo = 1

    mo = re.finditer(token_regex, content)

    for m in mo:
        dic = m.groupdict()

        if dic['COMMENT']:
            t = ("COMMENT", dic['COMMENT'], lineNo, m.span())
        elif dic['STRING']:
            t = ("STRING", dic['STRING'], lineNo, m.span())
        elif dic['TAG']:
            t = ("TAG", dic['TAG'], lineNo, m.span())
        elif dic['VARIABLE']:
            t = ("VARIABLE", dic['VARIABLE'], lineNo, m.span())
        elif dic['NUM']:
            t = ("NUM", int(dic['NUM']), lineNo, m.span())
        elif dic['DOT']:
            t = ("DOT", dic['DOT'], lineNo, m.span())
        elif dic['LBRACE']:
            t = ("LBRACE", dic['LBRACE'], lineNo, m.span())
        elif dic['RBRACE']:
            t = ("RBRACE", dic['RBRACE'], lineNo, m.span())
        elif dic['COLON']:
            t = ("COLON", dic['COLON'], lineNo, m.span())
        elif dic['PREFIX']:
            t = ("PREFIX", m.group('left'), lineNo, m.span())
        elif dic['TERM']:
            t = ("TERM", m.group('right'), lineNo, m.span())
        elif dic['KEYWORD']:
            t = ("KEYWORD", dic['KEYWORD'], lineNo, m.span())
        elif dic['NEWLINE']:
            lineNo += 1
            pass
        elif dic['SKIP']:
            pass
        else:
            t = ("ERROR", m.group(), lineNo, m.span())

        if not (dic['SKIP'] or dic['NEWLINE']): res.append(t)

    return res



linhas = []

for linha in sys.stdin:
    linhas.append(linha)

conteudo = "".join(linhas)

for token in tokenize(conteudo):
    print(token)
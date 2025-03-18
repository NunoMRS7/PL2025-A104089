import ply.lex as lex

tokens = (
    'ADD',
    'SUB',
    'MUL',
    'DIV',
    'NUM'
)

t_ADD = r'\+'
t_SUB = r'-'
t_MUL = r'\*'
t_DIV = r'\/'
t_NUM = r'\d+'

t_ignore = ' \t\n'

def t_error(t):
    print("Caráter ilegal:", t.value[0])
    t.lexer.skip(1)

lexer = lex.lex()
import ply.yacc as yacc
from tpc_lex import tokens
import sys

precedence = (
    ('left', 'ADD', 'SUB'),
    ('left', 'MUL', 'DIV'),
)

def p_geral(p):
    """
    S : Exp
    """
    p[0] = p[1]
    print(p[0])

def p_MUL(p):
    """
    Exp : Exp MUL Exp
    """
    p[0] = p[1] * p[3]

def p_DIV(p):
    """
    Exp : Exp DIV Exp
    """
    p[0] = p[1] / p[3]

def p_ADD(p):
    """
    Exp : Exp ADD Exp
    """
    p[0] = p[1] + p[3]

def p_SUB(p):
    """
    Exp : Exp SUB Exp
    """
    p[0] = p[1] - p[3]

def p_NUM(p):
    """
    Exp : NUM
    """
    p[0] = int(p[1])

def p_error(p):
    print("Erro sintático:", p)
    parser.success = False

parser = yacc.yacc()

for linha in sys.stdin:
    parser.success = True
    parser.parse(linha)
    if parser.success:
        print("Resultado =", linha)
    else:
        print("Não é possivel gerar um resultado pois a expressão é inválida")
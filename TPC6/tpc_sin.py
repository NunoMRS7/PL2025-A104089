import ply.yacc as yacc
from tpc_lex import tokens
import sys

def p_geral(p):
    """
    S : Exp
    """
    p[0] = p[1]
    print("Resultado =", p[0])

def p_ADD(p):
    """
    Exp : Exp ADD Termo
    """
    p[0] = p[1] + p[3]

def p_SUB(p):
    """
    Exp : Exp SUB Termo
    """
    p[0] = p[1] - p[3]

def p_TERMO(p):
    """
    Exp : Termo
    """
    p[0] = p[1]

def p_MUL(p):
    """
    Termo : Termo MUL Fator
    """
    p[0] = p[1] * p[3]

def p_DIV(p):
    """
    Termo : Termo DIV Fator
    """
    p[0] = p[1] / p[3]

def p_FATOR(p):
    """
    Termo : Fator
    """
    p[0] = p[1]

def p_PARENTESES(p):
    """
    Fator : PA Exp PF
    """
    p[0] = p[2]

def p_NUM(p):
    """
    Fator : NUM
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
        print("Expressão válida:", linha)
    else:
        print("Não é possivel gerar um resultado pois a expressão é inválida")
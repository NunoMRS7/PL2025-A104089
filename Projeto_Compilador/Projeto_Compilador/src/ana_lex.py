import ply.lex as lex

literals = ['(', ')', ';', '.', ',', ':',
            '{', '}', '>', '<', '=', '*', '+', '-', '/', '[', ']']

tokens = (
    'PROGRAM', 'VAR', 'BEGIN', 'END', 'IF', 'THEN', 'ELSE', 'FOR', 'TO', 'DO', 'WHILE', 'DIV', 'MOD', 'AND', 'OR', 'NOT', 'ARRAY', 'OF', 'DOWNTO', 'FUNCTION', 'PROCEDURE',
    'id', 'string', 'num', 'boolean'
)


def t_PROGRAM(t):
    r'[pP][rR][oO][gG][rR][aA][mM]'
    return t


def t_FUNCTION(t):
    r'[fF][uU][nN][cC][tT][iI][oO][nN]'
    return t


def t_PROCEDURE(t):
    r'[pP][rR][oO][cC][eE][dD][uU][rR][eE]'
    return t


def t_VAR(t):
    r'[vV][aA][rR]'
    return t


def t_BEGIN(t):
    r'[bB][eE][gG][iI][nN]'
    return t


def t_END(t):
    r'[eE][nN][dD]'
    return t


def t_IF(t):
    r'[iI][fF]'
    return t


def t_THEN(t):
    r'[tT][hH][eE][nN]'
    return t


def t_ELSE(t):
    r'[eE][lL][sS][eE]'
    return t


def t_FOR(t):
    r'[fF][oO][rR]'
    return t


def t_TO(t):
    r'[tT][oO]'
    return t


def t_DOWNTO(t):
    r'[dD][oO][wW][nN][tT][oO]'
    return t


def t_DO(t):
    r'[dD][oO][^u]'
    return t


def t_WHILE(t):
    r'[wW][hH][iI][lL][eE]'
    return t


def t_DIV(t):
    r'[dD][iI][vV]'
    return t


def t_MOD(t):
    r'[mM][oO][dD]'
    return t


def t_AND(t):
    r'[aA][nN][dD]'
    return t


def t_OR(t):
    r'[oO][rR]'
    return t


def t_NOT(t):
    r'[nN][oO][tT]'
    return t


def t_ARRAY(t):
    r'[aA][rR][rR][aA][yY]'
    return t


def t_OF(t):
    r'[oO][fF]'
    return t


def t_string(t):
    r'\'[^\']*?\''
    t.value = t.value[1:-1]
    return t


def t_num(t):
    r'\d+'
    t.value = int(t.value)
    return t


def t_boolean(t):
    r'true|false'
    return t


def t_id(t):
    r'[a-zA-Z_]\w*'
    return t


t_ignore = ' \t\n\r'
t_ignore_COMMENT = r'{.*}'


def t_error(t):
    print(f"Caractere inválido: {t.value[0]}")
    t.lexer.skip(1)


lexer = lex.lex()

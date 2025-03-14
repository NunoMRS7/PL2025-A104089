import json
import sys
import ply.lex as lex

states = [
    ('SELECAO', 'exclusive'),
    ('COMPRA', 'exclusive')
]

tokens = [
    'LISTAR',
    'SELECIONAR',
    'SAIR',
    'CODIGO',
    'MOEDA',
    'QUANTIDADE',
]

t_ANY_ignore = ' \t.,'

def t_LISTAR(t):
    r'LISTAR'
    return t

def t_SAIR(t):
    r'SAIR'
    return t

def t_SELECIONAR(t):
    r'SELECIONAR'
    t.lexer.begin('SELECAO')
    return t

def t_SELECAO_CODIGO(t):
    r'[a-zA-Z]\d\d'
    t.lexer.begin('INITIAL')
    return t

def t_MOEDA(t):
    r'MOEDA'
    t.lexer.begin('COMPRA')
    return t

def t_COMPRA_QUANTIDADE(t):
    r'2[eE]|1[eE]|50[cC]|20[cC]|10[cC]|5[cC]|2[cC]|1[cC]'
    value = t.value.lower()
    if 'e' in value:
        t.value = int(value[:-1]) * 100  # converter euros em centimos
    else:
        t.value = int(value[:-1])
    return t

def t_COMPRA_newline(t):
    r'\n+'
    t.lexer.begin('INITIAL')

def t_ANY_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

def t_ANY_error(t):
    print("Caracter ilegal: ", t.value[0])
    t.lexer.skip(1)




def readJsonFile(filename):
    with open(filename, 'r') as file:
        return json.load(file)

def writeJsonFile(filename, data):
    with open(filename, 'w') as file:
        json.dump(data, file, indent=4)




def saldo_to_string(saldo):
    if saldo >= 100:
        if saldo % 100 == 0:
            str_saldo = str(saldo//100) + "e"
        else:
            str_saldo = str(saldo//100) + "e" + str(saldo%100) + "c"
    else:
        str_saldo = str(saldo) + "c"
    return str_saldo

def troco_to_string(saldo):
    troco = {"2e": 0, "1e": 0, "50c": 0, "20c": 0, "10c": 0, "5c": 0, "2c": 0, "1c": 0}
    while saldo > 0:
        if saldo >= 200:
            saldo -= 200
            troco['2e'] += 1
        elif saldo >= 100:
            saldo -= 100
            troco['1e'] += 1
        elif saldo >= 50:
            saldo -= 50
            troco['50c'] += 1
        elif saldo >= 20:
            saldo -= 20
            troco['20c'] += 1
        elif saldo >= 10:
            saldo -= 10
            troco['10c'] += 1
        elif saldo >= 5:
            saldo -= 5
            troco['5c'] += 1
        elif saldo >= 2:
            saldo -= 2
            troco['2c'] += 1
        elif saldo >= 1:
            saldo -= 1
            troco['1c'] += 1

    res = ""
    str_list = [f"{value}x {key}" for key, value in troco.items() if value > 0]
    if len(str_list) > 1:
        res = ", ".join(str_list[:-1]) + " e " + str_list[-1]
    else:
        res = str_list[0]

    return res

def produto(cod, stock):
    produto = None
    for item in stock:
        if item['cod'] == cod:
            produto = item
    return produto

def main():
    saldo = 0
    running = True

    stock = readJsonFile("stock.json")

    lexer = lex.lex()

    if stock is None:
        print("maq: 2025/03/14, Stock não carregado, Estado atualizado.")
    else:
        print("maq: 2025/03/14, Stock carregado, Estado atualizado.")
    print("maq: Bom dia. Estou disponível para atender o seu pedido.")

    while running:
        line = input()
        line += '\n'
        lexer.input(line)
        lista_tokens = []
        for tok in lexer:
            lista_tokens.append(tok)
        
        if not lista_tokens:
            print("maq: Comando inválido")
        elif lista_tokens[0].type == 'LISTAR':
            print("maq:")
            print("cod  |    nome    |   quantidade   |   preço")
            print("---------------------------------")
            for item in stock:
                print(item['cod'], " | ", item['nome'], " |      ", item['quant'], "      | ", item['preco'])
        elif lista_tokens[0].type == 'SELECIONAR':
            cod = lista_tokens[1].value
            p = produto(cod, stock)
            if p is None:
                print("maq: Produto não existe")
            elif p['quant'] == 0:
                print("maq: Produto esgotado")
            elif int(p['preco'] * 100) > saldo:
                print("Saldo insufuciente para satisfazer o seu pedido")
                print(f"maq: Saldo = {saldo_to_string(saldo)}; Pedido = {saldo_to_string(int(p['preco'] * 100))}")
            else:
                print(f"maq: Pode retirar o produto dispensado \"{p['nome']}\"")
                p['quant'] -= 1
                saldo -= int(p['preco'] * 100)
                print(f"maq: Saldo = {saldo_to_string(saldo)}")
        elif lista_tokens[0].type == 'MOEDA':
            for token in lista_tokens[1:]:
                saldo += token.value
            print(f"maq: Saldo = {saldo_to_string(saldo)}")
        elif lista_tokens[0].type == 'SAIR':
            print(f"maq: Pode retirar o troco: {troco_to_string(saldo)}")
            print("maq: Até à próxima")
            saldo = 0
            running = False
            writeJsonFile("stock.json", stock)
        else:
            print("maq: Comando inválido")

if __name__ == "__main__":
    main()
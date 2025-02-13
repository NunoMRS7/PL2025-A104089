import sys

soma = 0
on = True

for linha in sys.stdin:
    i = 0
    while i < len(linha):
        if linha[i] == '=':
            print(soma)
            i += 1
        elif linha[i] == 'o' or linha[i] == 'O':
            if i < len(linha)-1 and (linha[i+1] == 'n' or linha[i+1] == 'N'):
                on = True
                i += 2
            elif i < len(linha)-2 and (linha[i+1] == 'f' or linha[i+1] == 'F') and (linha[i+2] == 'f' or linha[i+2] == 'F'):
                on = False
                i += 3
            else:
                i += 1
        elif linha[i] in "0123456789":
            if on:
                numero = 0
                while linha[i] in "0123456789":
                    numero = numero*10 + int(linha[i])
                    i += 1
                soma += numero
            else:
                i += 1
        else:
            i += 1

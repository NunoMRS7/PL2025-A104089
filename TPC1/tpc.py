import sys

def somadorOnOff(texto):
    soma = 0
    on = 1

    i = 0
    while i < len(texto):
        if texto[i] == '=':
            print(soma)
            i += 1
        elif texto[i] == 'o' or texto[i] == 'O':
            if i < len(texto)-1 and (texto[i+1] == 'n' or texto[i+1] == 'N'):
                on = 1
                i += 1
            elif i < len(texto)-2 and (texto[i+1] == 'f' or texto[i+1] == 'F') and (texto[i+2] == 'f' or texto[i+2] == 'F'):
                on = 0
                i += 1
            else:
                i += 1
        elif texto[i] in "0123456789":
            if on == 1:
                numero = 0
                while texto[i] in "0123456789":
                    numero = numero*10 + int(texto[i])
                    i += 1
                soma += numero
            else:
                i += 1
        else:
            i += 1


entrada = sys.stdin.read()
somadorOnOff(entrada)
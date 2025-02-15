import sys
import re
import locale

locale.setlocale(locale.LC_ALL, 'pt_PT.UTF-8')


regexCompositor = r';\d\d\d\d;[^;]+;([^;]+);[^;]+;'
regexPeriodo    = r';\d\d\d\d;([^;]+);[^;]+;[^;]+;'
regexTitulo     = r'^\w[^;]+'


setCompositores = set()
dictPeriodosQuantidades = dict()
dictPeriodosTitulos = dict()
tituloAtual = ""


for linha in sys.stdin:
    resComp = re.search(regexCompositor, linha)
    resPer  = re.search(regexPeriodo, linha)
    resTitl = re.search(regexTitulo, linha)

    if resTitl:
        tituloAtual = resTitl.group()
    
    if resComp:
        compositor = resComp.group(1)
        setCompositores.add(compositor)

    if resPer:
        periodo = resPer.group(1)
        if periodo in dictPeriodosQuantidades:
            dictPeriodosQuantidades[periodo] = dictPeriodosQuantidades[periodo] + 1
        else:
            dictPeriodosQuantidades[periodo] = 1

        if periodo in dictPeriodosTitulos:
            dictPeriodosTitulos[periodo].append(tituloAtual)
        else:
            dictPeriodosTitulos[periodo] = [tituloAtual]


listaCompositores = list(setCompositores)
listaCompositores.sort(key=locale.strxfrm)
print("======== Lista ordenada de compositores musicais ========")
for c in listaCompositores:
    print(c)

print("\n\n\n======== Quantidade de obras por período ========")
for p, n in dictPeriodosQuantidades.items():
    print(f"{p}: {n}")

print("\n\n\n======== Títulos de obras por período ========")
for p, l in dictPeriodosTitulos.items():
    l.sort(key=locale.strxfrm)
    print(f"{p}:")
    for t in l:
        print("\t",t)
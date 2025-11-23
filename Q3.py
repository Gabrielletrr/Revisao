with open('triangulo.txt', 'w') as f:
    f.write('''3
7 4
2 4 6
8 5 9 3
''')

def carregar_triangulo(nome_arquivo):
    triangulo = []
    with open(nome_arquivo, 'r') as arquivo:
        for linha in arquivo:
            numeros = linha.strip().split()
            if numeros: 
                triangulo.append([int(n) for n in numeros])
    return triangulo

def maximo_total(triangulo):
    for i in range(len(triangulo) - 2, -1, -1):
        for j in range(len(triangulo[i])):
            triangulo[i][j] += max(triangulo[i + 1][j], triangulo[i + 1][j + 1])
    return triangulo[0][0]

try:
    triangulo = carregar_triangulo('triangulo.txt') 
    resultado = maximo_total(triangulo)
    print('Maior total possível:', resultado)
except Exception as e:
    print('Erro inesperado:', e)

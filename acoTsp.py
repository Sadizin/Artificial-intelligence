import os
import csv
import math
import random
import time
import matplotlib.pyplot as plt

def ler_cidades(nome_arquivo):
    cidades = {}
    try:
        with open(nome_arquivo, mode='r') as arquivo:
            leitor_csv = csv.DictReader(arquivo, delimiter=';')
            for linha in leitor_csv:
                id_cidade = int(linha['id'])
                x = float(linha['x'])
                y = float(linha['y'])
                cidades[id_cidade] = (x, y)
    except Exception as e:
        print(f"Erro ao ler o arquivo CSV: {e}")
        return None
    return cidades

def calcular_distancias(cidades):
    distancias = {}
    for id1, (x1, y1) in cidades.items():
        for id2, (x2, y2) in cidades.items():
            if id1 != id2:
                distancia = math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)
                distancias[(id1, id2)] = distancia
    return distancias

def funcao_objetivo(caminho, distancias):
    custo_total = 0
    for i in range(len(caminho) - 1):
        custo_total += distancias[(caminho[i], caminho[i + 1])]
    custo_total += distancias[(caminho[-1], caminho[0])]
    return custo_total

def aco(num_formigas, cidades, distancias, alfa, beta, rho, feromonio_inicial, max_iter):
    num_cidades = len(cidades)
    feromonios = {aresta: feromonio_inicial for aresta in distancias}
    melhor_caminho = None
    melhor_custo = float('inf')
    medias_custos = []  

    for iteracao in range(max_iter):
        progresso = (iteracao + 1) / max_iter * 100
        print(f"Progresso: {progresso:.2f}% concluído", end='\r')

        caminhos_formigas = []
        custos_formigas = []

        for _ in range(num_formigas):
            cidade_atual = random.choice(list(cidades.keys()))
            caminho = [cidade_atual]
            visitados = {cidade_atual}

            while len(caminho) < num_cidades:
                probabilidades = []
                cidades_disponiveis = []

                for prox_cidade in cidades:
                    if prox_cidade not in visitados:
                        cidades_disponiveis.append(prox_cidade)
                        aresta = (cidade_atual, prox_cidade)
                        tau = feromonios[aresta] ** alfa
                        eta = (1 / distancias[aresta]) ** beta
                        probabilidades.append(tau * eta)

                soma_probabilidades = sum(probabilidades)
                probabilidades = [p / soma_probabilidades for p in probabilidades]
                proxima_cidade = random.choices(cidades_disponiveis, weights=probabilidades, k=1)[0]

                caminho.append(proxima_cidade)
                visitados.add(proxima_cidade)
                cidade_atual = proxima_cidade

            custo = funcao_objetivo(caminho, distancias)
            caminhos_formigas.append(caminho)
            custos_formigas.append(custo)

            if custo < melhor_custo:
                melhor_caminho = caminho
                melhor_custo = custo

        for aresta in feromonios:
            feromonios[aresta] *= (1 - rho)

        for caminho, custo in zip(caminhos_formigas, custos_formigas):
            for i in range(len(caminho) - 1):
                aresta = (caminho[i], caminho[i + 1])
                feromonios[aresta] += 1 / custo

        media_custo_iteracao = sum(custos_formigas) / len(custos_formigas)
        medias_custos.append(media_custo_iteracao)

    print("\n")
    return melhor_caminho, melhor_custo, medias_custos


if __name__ == "__main__":

    inicio = time.time()
    nome_arquivo = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'dataset.txt')
    cidades = ler_cidades(nome_arquivo)

    if cidades:
        distancias = calcular_distancias(cidades)

        num_formigas = 40
        alfa = 1.0
        beta = 2.0
        rho = 0.1
        feromonio_inicial = 0.1
        max_iter = 1000

        melhor_caminho, melhor_custo, medias_custos = aco(num_formigas, cidades, distancias, alfa, beta, rho, feromonio_inicial, max_iter)

        print("Melhor caminho encontrado:", melhor_caminho)
        print("Custo do melhor caminho:", melhor_custo)

        fim = time.time()

        print(f"Tempo: {fim-inicio}")

        #Gráfico do melhor caminho
        x = [cidades[cidade][0] for cidade in melhor_caminho] + [cidades[melhor_caminho[0]][0]]
        y = [cidades[cidade][1] for cidade in melhor_caminho] + [cidades[melhor_caminho[0]][1]]

        plt.figure(figsize=(10, 5))
        plt.subplot(1, 2, 1)
        plt.plot(x, y, marker='o')
        plt.title("Melhor Caminho - Caixeiro Viajante - ACO")
        plt.xlabel("X")
        plt.ylabel("Y")
        plt.grid()

        #Gráfico de convergência
        plt.subplot(1, 2, 2)
        plt.plot(range(1, max_iter + 1), medias_custos, marker='o', color='r')
        plt.title("Convergência - Distância Média por Iteração")
        plt.xlabel("Iteração")
        plt.ylabel("Distância Média")
        plt.grid()

        plt.tight_layout()
        plt.show()

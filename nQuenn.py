import random
import time
import numpy as np



def gerar(n): 
    solucao = random.sample(range(1, n + 1), n) 
    return solucao

def calculo_fitness(solucao):
    
    diagonal_positiva = []
    diagonal_negativa = []   
    conflitos = 0
    n = len(solucao)
    
    for i in range(n):
        k_positivo = i - solucao[i] 
        k_negativo = i + solucao[i]
        
        if k_positivo in diagonal_positiva:
            conflitos += 1
        if k_negativo in diagonal_negativa:
            conflitos += 1
            
        diagonal_positiva.append(k_positivo)
        diagonal_negativa.append(k_negativo)
    return conflitos

def gerarVizinhos(solucao, iteracaoAtual, espera, listaGuardaTravada, listaGuardaIteracao, listaContador, listaContadorPosicao ):
    
    vizinho = solucao[:]
    n = len(solucao)
    
    if listaGuardaIteracao and listaGuardaIteracao[0] == iteracaoAtual:
        listaGuardaIteracao.pop(0) 
        listaGuardaTravada.pop(0)
        
    if len(listaGuardaTravada) < (n*(n-1)/2):
        posicaoTroca1, posicaoTroca2 = random.sample(range(n), 2)
        tupla = (posicaoTroca1, posicaoTroca2)
        
        while tupla in listaGuardaTravada or (tupla[1], tupla[0]) in listaGuardaTravada:
            posicaoTroca1, posicaoTroca2 = random.sample(range(n), 2)
            tupla = (posicaoTroca1, posicaoTroca2)

        vizinho[posicaoTroca1], vizinho[posicaoTroca2] = vizinho[posicaoTroca2], vizinho[posicaoTroca1]
        listaGuardaTravada.append(tupla)
        listaGuardaIteracao.append(iteracaoAtual+espera)
        
        if tupla in listaContadorPosicao:
            pos = listaContadorPosicao.index(tupla)
            listaContador[pos] += 1 
        else:
            listaContadorPosicao.append(tupla)
            listaContador.append(1)
                   
    else:
        
        menorContador = min(listaContador)
        indexMenor = listaContador.index(menorContador)
        itemNalistaPosicao = listaContadorPosicao[indexMenor] 
        pos1, pos2 = itemNalistaPosicao 
        vizinho[pos1], vizinho[pos2] = vizinho[pos2], vizinho[pos1]
        
    return vizinho

def buscaTabu(n, maxIteracoes, espera):
    
    solucao = gerar(n)
    fitness = calculo_fitness(solucao)
    listaGuardaTravada = [] 
    listaGuardaIteracao = []  
    listaContador = [] 
    listaContadorPosicao = [] 
    iteracaoAtual = 0
    
    for i in range(maxIteracoes):
        vizinho = gerarVizinhos(solucao, iteracaoAtual, espera, listaGuardaTravada, listaGuardaIteracao, listaContador, listaContadorPosicao)
        fitnessvizinho = calculo_fitness(vizinho)
        
        if fitnessvizinho < fitness:
            solucao[:] = vizinho[:]
            fitness = fitnessvizinho
            
        if fitness == 0:
            break
        
        iteracaoAtual += 1
        
    return solucao, fitness

if __name__ =="__main__":
    
    n = 100
    maxIteracoes = 5000
    espera = 3
    
    inicio = time.time()
    solucao, fitness = buscaTabu(n, maxIteracoes, espera) 
    fim = time.time()
    
    print("Solução", solucao)
    print("Fitness", fitness)
    print(f"Tempo de execução: {fim-inicio:.10f} segundos")
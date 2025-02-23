import numpy as np
import matplotlib.pyplot as plt

def rastrigin(x):  
    d = len(x)
    s = np.sum(np.array(x)**2 - 10*np.cos(2*np.pi*np.array(x)))
    return 10*d + s

def g(x):  
    return np.sin(2*np.pi*x) + 0.5

def h(x):  
    return np.cos(2*np.pi*x) + 0.5  

def penalizacao(x):
    penalidade = 0
    for xi in x:
        if g(xi) > 0:
            penalidade += 1e6
        if abs(h(xi)) > 1e-6:
            penalidade += 1e6
        penalidade += 1e4 * abs(xi + 0.33)
    return penalidade

def funcao_objetivo(x):
    return rastrigin(x) + penalizacao(x)

def pso(maxiter, W, C1, C2, qtdeparticulas, n_dimensoes, limite_inferior, limite_superior):
    posicoes = np.random.uniform(limite_inferior, limite_superior, (qtdeparticulas, n_dimensoes))
    velocidades = np.random.uniform(-1, 1, (qtdeparticulas, n_dimensoes))
    
    pbest = np.copy(posicoes)
    pbest_fitness = np.array([funcao_objetivo(p) for p in posicoes])
    gbest = posicoes[np.argmin(pbest_fitness)]
    gbest_fitness = np.min(pbest_fitness)
    
    ftmedia = []
    ftgbest = []
    ftstd = []
    
    for iter in range(maxiter):
        for i in range(qtdeparticulas):
            inercia = W * velocidades[i]
            r1, r2 = np.random.rand(n_dimensoes), np.random.rand(n_dimensoes)
            cognitivo = C1 * r1 * (pbest[i] - posicoes[i])
            social = C2 * r2 * (gbest - posicoes[i])
            
            velocidades[i] = inercia + cognitivo + social
            posicoes[i] = np.clip(posicoes[i] + velocidades[i], limite_inferior, limite_superior)
            
            fitness = funcao_objetivo(posicoes[i])
            if fitness < pbest_fitness[i]:
                pbest[i], pbest_fitness[i] = posicoes[i], fitness
                if fitness < gbest_fitness:
                    gbest, gbest_fitness = posicoes[i], fitness
        
        ftmedia.append(np.mean(pbest_fitness))
        ftgbest.append(gbest_fitness)
        ftstd.append(np.std(pbest_fitness))
        print(f"Iteração {iter + 1}/{maxiter}, Fitness do gbest: {gbest_fitness}")
    
    plt.figure(figsize=(12, 6))
    plt.subplot(1, 3, 1)
    plt.plot(ftgbest, label="Fitness do melhor indivíduo", color="orange")
    plt.xlabel("Geração")
    plt.ylabel("Fitness")
    plt.title("Melhor Fitness por Geração")
    plt.legend()
    
    plt.subplot(1, 3, 2)
    plt.plot(ftmedia, label="Fitness Média", color="blue")
    plt.xlabel("Geração")
    plt.ylabel("Fitness Média")
    plt.title("Fitness Média por Geração")
    plt.legend()
    
    plt.subplot(1, 3, 3)
    plt.plot(ftstd, label="Desvio Padrão", color="green")
    plt.xlabel("Geração")
    plt.ylabel("Desvio Padrão")
    plt.title("Desvio Padrão da Fitness")
    plt.legend()
    
    plt.tight_layout()
    plt.show()
    
    return gbest, gbest_fitness

#Parâmetros do PSO
maxiter = 500
w, c1, c2 = 0.4, 2.0, 2.0
qtdeparticulas = 150
n_dimensoes = 5
limite_inferior, limite_superior = -5.12, 5.12

resultados_fitness = []
for _ in range(20):
    _, gbest_fitness = pso(maxiter, w, c1, c2, qtdeparticulas, n_dimensoes, limite_inferior, limite_superior)
    resultados_fitness.append(gbest_fitness)

media_fitness = np.mean(resultados_fitness)
desvio_fitness = np.std(resultados_fitness)

print(f"Média da fitness dos melhores indivíduos em 20 execuções: {media_fitness}")
print(f"Desvio padrão da fitness dos melhores indivíduos em 20 execuções: {desvio_fitness}")

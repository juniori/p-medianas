import math

import numpy as np
import pandas as pd


# -----------------------------------------------------------------------
# Funções Auxiliares
# -----------------------------------------------------------------------
def obter_instancias_simuladas():
    d = []
    x1 = 0
    for i in range(1, 6):
        x1 += 5
        x2 = (x1 + 2)
        x3 = (x2 + 2)
        d.append([i, x1, 1])
        d.append([i, x1, 5])
        d.append([i, x2, 3])
        d.append([i, x3, 1])
        d.append([i, x3, 5])
        x1 += 5
    data = np.array(d)
    dataset2 = pd.DataFrame({'Grupo': data[:, 0], 'x': data[:, 1], 'y': data[:, 2]})
    dataset2 = dataset2[['x', 'y']]
    return dataset2.values

def escolherCentrosIniciais(entidades, p, seed):
    centros = np.random.RandomState(seed=seed).permutation([1 * i for i in range(0, len(entidades))])[:p]
    return centros

def calcularDistancia(entidades, index_a, index_b):
    a = entidades[index_a]
    b = entidades[index_b]
    d = math.sqrt(((a[0] - b[0]) ** 2) + ((a[1] - b[1]) ** 2))
    return d

def encontrarCentroDeMenorCustoParaCluster(entidades, alocacoes, centro):
    centroMenorCusto = None
    distancia = None
    elementosDoCentro = [i for i, e in enumerate(alocacoes) if e == centro]
    for i in elementosDoCentro:
        distancia_temp = 0
        for j in elementosDoCentro:
            distancia_temp += calcularDistancia(entidades, i, j)
        if (distancia is None or distancia_temp < distancia):
            distancia = distancia_temp
            centroMenorCusto = i
            #print("centro alt.", novo_centro)
        else:
            None
            #print("centro mant.", novo_centro)
    return centroMenorCusto

def printCentros(info,centros, entidades):
    print("{}-----------".format(info))
    for c in centros:
        print(entidades[c])


# -----------------------------------------------------------------------
#  Main
# -----------------------------------------------------------------------

# Distancia para cada ponto: 2.8284271247461903
# Custo da solução default: (2.8284271247461903 * 4) * 5 = 56.568542494923804
def main(entidades, p):

    alocacoes = [None for i in range(len(entidades))]

    custoSolucao = 0
    centros = []

    # 1) Choose an initial position for each centre
    seed = 42
    centros = escolherCentrosIniciais(entidades, p, seed)

    # 2) Repeat the following steps while the location of the centres varies:
    while True:

        houveAlteracao = False;

        # 2a) Allocate the entities given the centre locations.
        # Para cada entidade, percorre por todos os centros, aloca-a no centro mais próximos

        for e_index, e in enumerate(entidades):
            centroAtual = alocacoes[e_index]
            distancia = None
            novoCentro = None

            for j, centro in enumerate(centros):
                distancia_temp = calcularDistancia(entidades, e_index, centro)
                if distancia is None or distancia_temp < distancia:
                    distancia = distancia_temp;
                    novoCentro = centro;

            if centroAtual is None:
                alocacoes[e_index] = novoCentro
                custoSolucao += calcularDistancia(entidades, e_index, novoCentro)
            elif centroAtual != novoCentro:
                alocacoes[e_index] = novoCentro
                custoSolucao -= calcularDistancia(entidades, e_index, centroAtual)
                custoSolucao += distancia

        # 2b) Given the allocation made at step 2a, locate each centre optimally.
        # Realoca os centros de acordo com a distancia entre os elementos de cada centro
        for i in range(0, p):
            centroDeMenorCusto = encontrarCentroDeMenorCustoParaCluster(entidades, alocacoes, centros[i])
            if centros[i] != centroDeMenorCusto:
                houveAlteracao = True
                centros[i] = centroDeMenorCusto

        # location of the centres varies ?
        if (houveAlteracao == False):
            break

    return alocacoes, custoSolucao


#solucao, custoSolucao = main(obter_instancias_simuladas(), 5)
#print("Custo da solução: {:.3f}".format(custoSolucao))
#print("Solução: {} ".format(solucao))
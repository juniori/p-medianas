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
    centros = [None for i in range(0, p)]
    entidadeSorteada = np.random.RandomState(seed=seed).randint(low=len(entidades), size=1)[0]
    centros[0] = entidadeSorteada
    return centros

def calcularDistancia(entidades, index_a, index_b):
    a = entidades[index_a]
    b = entidades[index_b]
    d = math.sqrt(((a[0] - b[0]) ** 2) + ((a[1] - b[1]) ** 2))
    return d

def encontrarEntidadeMaisDistanteDoCentro(alocacoes, centro):
    centroMenorCusto = None
    distancia = None
    elementosDoCentro = [i for i, e in enumerate(alocacoes) if e == centro]
    for i in elementosDoCentro:
        distancia_temp = 0
        for j in elementosDoCentro:
            distancia_temp += calcularDistancia(i, j)
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
    for i in range(0,len(centros)):
        if centros[i] is None:
            print("{}-{}".format(i, centros[i]))
        else:
            print("{}-{}".format(i, entidades[i]))

def gruposToArray(alocacoes, centros, iteracao, custoDaSolucao):
    ents = []

    grupos = [[] for i in range(0, len(centros))]

    for c_index in range(0, len(centros)):
        grupos[c_index] = [i for i, e in enumerate(alocacoes) if e == c_index]

    for g_index, g in enumerate(grupos):
        for e in g:
            strGrupo = str(entidades[centros[g_index]][0]) +","+str(entidades[centros[g_index]][1])
            isCentro = " C" if centros[g_index] == e else ""
            xy=""
            if centros[g_index] == e:
                #xy =  str(entidades[e][0]) + "," + str(entidades[e][1]) + isCentro
                xy= str(g_index)
            ents.append("['" +str(iteracao) +" - Custo: "+ ("{:,}".format(round(custoDaSolucao, 2))) +"','" +strGrupo+"'," + str(entidades[e][0]) + "," + str(entidades[e][1]) + ",'"+ xy + "'],");

    strResult = ""
    for i in ents:
        strResult += i

    return strResult[:-1] # -1 para tirar a ultima virgula concatenada indevidamente

# -----------------------------------------------------------------------
#  Main
# -----------------------------------------------------------------------

# Distancia para cada ponto: 2.8284271247461903
# Custo da solução default: (2.8284271247461903 * 4) * 5 = 56.568542494923804
def main(entidades, p):

    alocacoes = [None for i in range(len(entidades))]
    distanciasEntidadeCentro = [None for i in range(len(entidades))] # Distancia da entidade para o seu centro atual
    centros = []

    # 1) Escolha uma entidade aleatoriamente e coloque um centro nesta entidade.
    seed = 42
    centros = escolherCentrosIniciais(entidades, p, seed)
    custoSolucao = 0
    #printCentros("Centros iniciais(semente)",centros,entidades);

    # 2) Alocar todas as entidades para este centro e calcular suas diferenças ponderadas.
    for i in range(0,len(entidades)):
        centro = centros[0]
        alocacoes[i] = centro
        distancia = calcularDistancia(entidades, i, centro)
        distanciasEntidadeCentro[i] = distancia
        custoSolucao += distancia

    # 3) Para k = 1 até p faça:
    for k in range(1, p):

        # 3a) Encontre a entidade que está mais longe de um centro (dissimilaridades ponderadas)
        # e coloque o k-ésimo centro na localização dessa entidade.
        distancia = None
        entidadeMaisDistanteDoCentro = None
        for i in range(0,len(entidades)):
            distanciaTemp = distanciasEntidadeCentro[i]
            if distancia is None or distanciaTemp > distancia:
                distancia = distanciaTemp
                entidadeMaisDistanteDoCentro = i
        centros[k] = entidadeMaisDistanteDoCentro

        # 3b) Para i = 1 até n faça, se a entidade i está alocada em um centro mais distante do centro k:
        # Aloque a entidade i para o centro k e atualize sua dissimilaridade ponderada.
        for i in range(0,len(entidades)):
            distanciaCentroAtual = distanciasEntidadeCentro[i]
            distanciaCentroK = calcularDistancia(entidades, i,centros[k])
            if distanciaCentroK < distanciaCentroAtual:
                alocacoes[i] = centros[k]
                distanciasEntidadeCentro[i] = distanciaCentroK
                custoSolucao -= distanciaCentroAtual
                custoSolucao += distanciaCentroK

    return alocacoes, custoSolucao

#solucao, custoSolucao = main(obter_instancias_simuladas(), 5)
#print("Custo da solução: {:.3f}".format(custoSolucao))
#print("Solução: {} ".format(solucao))







import statistics
import time
import sys

import numpy as np
import pandas as pd

import Teillard_Algoritmo_1 as algoritmo1
import Teillard_Algoritmo_2 as algoritmo2


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

exec = 2
print('Informe o identificador do algoritmo a ser executado:')
escolha = input()
if escolha:
    exec = escolha


# -----------------------------------------------------------------------
#  Input
# -----------------------------------------------------------------------
print("Carregando instâncias...")
dfs = {}
dfs['simulado'] = {"p":5, "n":25, "values":obter_instancias_simuladas()}
#dfs['Lorena-pmedian324'] = {"p":5, "n":324, "values":pd.read_csv("http://www.lac.inpe.br/~lorena/instances/pmedian/pmedian324.txt", delimiter=" ", names=['x', 'y'],skiprows=1).values}
#dfs['Lorena-pmedian818'] = {"p":5, "n":818, "values":pd.read_csv("http://www.lac.inpe.br/~lorena/instances/pmedian/pmedian818.txt", delimiter=" ", names=['x', 'y'],skiprows = 1).values}
#dfs['Lorena-pmedian3282'] = {"p":5, "n":3282, "values":pd.read_csv("http://www.lac.inpe.br/~lorena/instances/pmedian/pmedian3282.txt", delimiter=" ", names=['x', 'y'],skiprows = 1).values}
#dfs['A1'] = {"p":20, "n":3000, "values":pd.read_csv("http://cs.joensuu.fi/sipu/datasets/a1.txt", delimiter="   ", names=['x','y'],  engine='python').values}
#dfs['A2'] = {"p":35, "n":5250, "values":pd.read_csv("http://cs.joensuu.fi/sipu/datasets/a2.txt", delimiter="   ", names=['x','y'],  engine='python').values}
#dfs['A3'] = {"p":50, "n":7500, "values":pd.read_csv("http://cs.joensuu.fi/sipu/datasets/a3.txt", delimiter="   ", names=['x','y'],  engine='python').values}

print("Instâncias carregadas!")
# -----------------------------------------------------------------------
#  Execução
# -----------------------------------------------------------------------

for key, dados in dfs.items():
    #print("---- Instância: \"{}\", n={}, p={} ----".format(key, dados["n"], dados["p"]))
    qtdExecucoes = 100
    solucao = None
    tempoMedio = None
    tempos = []
    for i in range(0,qtdExecucoes):
        start = time.time()
        if exec == '1':
            solucao, custoSolucao = algoritmo1.main(entidades= dados["values"], p =dados["p"])
        elif exec == '2':
            solucao, custoSolucao = algoritmo2.main(entidades=dados["values"], p=dados["p"])
        else:
            print("Algoritmo a ser executado não foi informado.")

        end = time.time()
        tempos.append(end-start)
    tempoMedio = statistics.mean(tempos)

    #print("Tempo Médio:{:.3f}ms, Custo da solução:{:.3f}".format(tempoMedio*1000, custoSolucao))
    print("{:.2f}\t{:.2f}".format(tempoMedio*1000, custoSolucao))

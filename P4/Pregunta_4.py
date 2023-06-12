from deap import creator, base, tools, algorithms
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

grafo = pd.read_csv("grafo.csv", index_col=0)
print(grafo)
# Convertir el CSV en una matriz numpy
rutas = grafo.to_numpy()
toolbox = base.Toolbox()
n = 5
creator.create("FitnessMin", base.Fitness, weights=(-1.0,))
creator.create("EstrIndividuo", list, fitness=creator.FitnessMin)
toolbox.register("Genes", np.random.permutation, n)
toolbox.register("Individuos", tools.initIterate, creator.EstrIndividuo, toolbox.Genes)
toolbox.register("Poblacion", tools.initRepeat, list, toolbox.Individuos)
pop = toolbox.Poblacion(n=10)
toolbox.register("mate", tools.cxPartialyMatched)
toolbox.register("mutate", tools.mutShuffleIndexes, indpb=0.1)
toolbox.register("select", tools.selTournament, tournsize=2)

def sol(individuo):
    f = 0
    for i in range(n-1):
        local1 = individuo[i]
        local2 = individuo[i+1]
        distancia = rutas[local1][local2]
        f = f + distancia
    return f,
toolbox.register("evaluate", sol)
def estadisticaAux(individuo):
    return individuo.fitness.values
estadistica = tools.Statistics(estadisticaAux)
estadistica.register('mean', np.mean)
estadistica.register('min', np.min)
estadistica.register('max', np.max)
hof = tools.HallOfFame(1)
result, log = algorithms.eaSimple(pop,toolbox,cxpb=0.8,mutpb=0.1,stats=estadistica,ngen=30,halloffame=hof,verbose=True)
print("Mejor Recorrido:", hof)
mejor_recorrido = list(hof[0])
distancia =0 
for i in range(len(mejor_recorrido)- 1):
  distancia = distancia + rutas[mejor_recorrido[i]][mejor_recorrido[i+1]]
print("Distancia Total: ", distancia)
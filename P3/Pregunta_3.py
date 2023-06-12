import pandas as pd
import numpy as np
import random

# Leer el archivo CSV
grafo = pd.read_csv("grafo.csv", index_col=0)
print(grafo)
rutas = grafo.to_numpy()
n_nodos = len(rutas)
n_poblacion = 10
mutacion = 0.3
n_generaciones = 200
nodo_inicial = 0

# Función para calcular la distancia total de un recorrido
def calcular_distancia_total(recorrido):
    distancia_total = 0
    for i in range(len(recorrido) - 1):
        nodo_actual = recorrido[i]
        nodo_siguiente = recorrido[i + 1]
        distancia_total += rutas[nodo_actual][nodo_siguiente]
    return distancia_total

# Función para generar una población inicial aleatoria
def generar_poblacion_inicial():
    poblacion = []
    for _ in range(n_poblacion):
        recorrido = list(range(n_nodos))
        random.shuffle(recorrido)
        poblacion.append(recorrido)
    return poblacion

# Función para realizar el cruce de dos padres
def cruzar_padres(padre1, padre2):
    punto_cruce = random.randint(1, n_nodos - 1)
    hijo = padre1[:punto_cruce]
    for nodo in padre2:
        if nodo not in hijo:
            hijo.append(nodo)
    return hijo

# Función para realizar la mutación en un individuo
def mutar_individuo(individuo):
    for _ in range(int(n_nodos * mutacion)):
        idx1, idx2 = random.sample(range(1, n_nodos), 2)
        individuo[idx1], individuo[idx2] = individuo[idx2], individuo[idx1]
    return individuo

# Función para seleccionar los mejores individuos de la población
def seleccionar_mejores(poblacion, fitness, n_seleccionados):
    mejores_indices = np.argsort(fitness)[:n_seleccionados]
    mejores_poblacion = [poblacion[idx] for idx in mejores_indices]
    return mejores_poblacion

poblacion = generar_poblacion_inicial()

for generacion in range(n_generaciones):
    fitness = [calcular_distancia_total(recorrido) for recorrido in poblacion]
    mejores_poblacion = seleccionar_mejores(poblacion, fitness, n_poblacion // 2)
    nueva_generacion = []
    while len(nueva_generacion) < n_poblacion:
        padre1, padre2 = random.sample(mejores_poblacion, 2)
        hijo = cruzar_padres(padre1, padre2)
        nueva_generacion.append(hijo)
    
    nueva_generacion = [mutar_individuo(individuo) for individuo in nueva_generacion]
    poblacion = nueva_generacion

fitness = [calcular_distancia_total(recorrido) for recorrido in poblacion]
mejor_individuo_idx = np.argmin(fitness)
mejor_recorrido = poblacion[mejor_individuo_idx]

indice_nodo_inicial = mejor_recorrido.index(nodo_inicial)
mejor_recorrido = mejor_recorrido[indice_nodo_inicial:] + mejor_recorrido[:indice_nodo_inicial]

# Imprimir el mejor recorrido y su distancia total
print("Mejor recorrido:", mejor_recorrido)
print("Distancia total:", calcular_distancia_total(mejor_recorrido))

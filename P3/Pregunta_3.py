import pandas as pd
import numpy as np
import random

# Leer el archivo CSV
grafo = pd.read_csv("grafo.csv", index_col=0)
print(grafo)
# Convertir el CSV en una matriz numpy
rutas = grafo.to_numpy()

# Definir el número de nodos en el grafo
n_nodos = len(rutas)

# Definir el número de individuos en la población
n_poblacion = 10

# Definir la probabilidad de mutación
mutacion = 0.3

# Definir el número de generaciones
n_generaciones = 200

# Definir el nodo inicial
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

# Generar la población inicial
poblacion = generar_poblacion_inicial()

# Realizar las generaciones
for generacion in range(n_generaciones):
    # Calcular el fitness de cada individuo en la población
    fitness = [calcular_distancia_total(recorrido) for recorrido in poblacion]
    
    # Seleccionar los mejores individuos
    mejores_poblacion = seleccionar_mejores(poblacion, fitness, n_poblacion // 2)
    
    # Crear la nueva generación cruzando los mejores individuos
    nueva_generacion = []
    while len(nueva_generacion) < n_poblacion:
        padre1, padre2 = random.sample(mejores_poblacion, 2)
        hijo = cruzar_padres(padre1, padre2)
        nueva_generacion.append(hijo)
    
    # Aplicar la mutación a la nueva generación
    nueva_generacion = [mutar_individuo(individuo) for individuo in nueva_generacion]
    
    # Reemplazar la población anterior con la nueva generación
    poblacion = nueva_generacion

# Seleccionar el mejor individuo de la última generación
fitness = [calcular_distancia_total(recorrido) for recorrido in poblacion]
mejor_individuo_idx = np.argmin(fitness)
mejor_recorrido = poblacion[mejor_individuo_idx]

# Obtener el mejor recorrido iniciando en el nodo X
indice_nodo_inicial = mejor_recorrido.index(nodo_inicial)
mejor_recorrido = mejor_recorrido[indice_nodo_inicial:] + mejor_recorrido[:indice_nodo_inicial]

# Imprimir el mejor recorrido y su distancia total
print("Mejor recorrido:", mejor_recorrido)
print("Distancia total:", calcular_distancia_total(mejor_recorrido))

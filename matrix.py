from matplotlib import pyplot as plt
import numpy as np
import random
import math
import chess
import chess.svg

'''Parámetros de entrada
'''
tamaño_poblacion = int(input("Tamaño de la población: "))
porcentaje_padres = int(input("Porcentaje de padres: "))

''' Función que evalúa la aptitud de una solución
    E: solución <- Matriz de un tablero
    S: aptitud <- Aptitud de la solución dada
'''
def calcularAptitud(solucion):
    reinas_fils = 0
    reinas_cols = 0
    reinas_diag = 0
    for fila in range(solucion.shape[0]):
        if (np.sum(solucion[fila,:]) > 1):
            reinas_fils += np.sum(solucion[fila,:]) - 1
    for col in range(solucion.shape[1]):
        if (np.sum(solucion[:,col]) > 1):
            reinas_cols += np.sum(solucion[:,col]) - 1
    for i in range(-7,7):
        if (np.trace(solucion, i) > 1):
            reinas_diag += np.trace(solucion, i) - 1
        if (np.trace(np.rot90(solucion), -i) > 1):
            reinas_diag += np.trace(np.rot90(solucion), -i) - 1        
    return int(reinas_fils+reinas_cols+reinas_diag)

''' Función que genera la población inicial
    E: tamaño <- Tamaño de la población
    S: poblacio, aptitudes <- Lista de soluciones y su aptitud correspondiente  
'''
def generarPoblacion(tamaño):
    poblacion = []
    aptitudes = []
    for index in range (0,tamaño):
        solucion = np.zeros(64)
        pos_reinas = random.sample(range(0, 64), 8)
        for pos in pos_reinas:
            solucion[pos] = 1
        solucion = solucion.reshape((8,8))
        aptitud = calcularAptitud(solucion)
        aptitudes.append((index,aptitud))
        poblacion.append(solucion)
    return poblacion, aptitudes

''' Función que selecciona un porcentaje de la población
    E: poblacion,aptitudes,porcentaje
    S: padres <- Lista de soluciones padre  
'''
def seleccionarPadres(poblacion, aptitudes, porcentaje):
    no_padres = math.ceil((tamaño_poblacion*porcentaje)/100)
    padres = []
    aptitudes.sort(key=lambda a: a[1])
    i=0
    while i < no_padres:
        p = np.random.uniform(0,1)
        if (p < 0.6):
            pos = random.sample(range(0, math.ceil(tamaño_poblacion/3)), 1)
        elif (p > 0.6) & (p < 0.9):
            pos = random.sample(range(math.ceil(tamaño_poblacion/3), 2*math.ceil(tamaño_poblacion/3)), 1)
        elif (p > 0.9):
            pos = random.sample(range(2*math.ceil(tamaño_poblacion/3), tamaño_poblacion), 1)
        aptitud = aptitudes[pos[0]]
        indice = aptitud[0]
        padres.append(poblacion[indice])
        i+=1
    return padres

ppl, appts = generarPoblacion(tamaño_poblacion)
x = seleccionarPadres(ppl, appts, porcentaje_padres)

print(x)
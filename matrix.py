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
porcentaje_cruza = int(input("Porcentaje de cruza: "))
porcentaje_mutacion = int(input("Porcentaje de mutación: "))

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
    no_padres = int((tamaño_poblacion*porcentaje)/100)
    if ((no_padres % 2) != 0):
        no_padres+=1
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

def operadorCruza(solucion1, solucion2):    
    first_half1  = solucion1[:,:4]
    second_half1 = solucion1[:,4:]
    first_half2  = solucion2[:,:4]
    second_half2 = solucion2[:,4:]
    sol_1 = np.concatenate((first_half1,second_half2),axis=1)
    sol_2 = np.concatenate((first_half2,second_half1),axis=1)
    return sol_1, sol_2

def getRandomElement(solution, queen):
    if (queen == True):
        indxs = np.where(solution == 1)
    else:
        indxs = np.where(solution == 0)
    rows = indxs[0]
    cols = indxs[1]
    idx = random.randint(0, len(rows)-1)
    return rows[idx], cols[idx]

def repairBoard(solution):
    _, counts = np.unique(solution, return_counts=True)
    while (counts[1] > 8):
        row, col = getRandomElement(solution, queen=True)
        solution[row][col] = 0
        _, counts = np.unique(solution, return_counts=True)
    while (counts[1] < 8):
        row, col = getRandomElement(solution, queen=False)
        solution[row][col] = 1
        _, counts = np.unique(solution, return_counts=True)
    return solution

def mutateBoard(solution):
    row_a, col_a = getRandomElement(solution, queen=True)
    row_b, col_b = getRandomElement(solution, queen=False)
    solution[row_a][col_a] = 0
    solution[row_b][col_b] = 1
    return solution

# Inicializar población
ppl, appts = generarPoblacion(tamaño_poblacion)

# Cruzar padres y reparar hijos
ppdrs = seleccionarPadres(ppl, appts, porcentaje_padres)
hhjs = []    
no_cruzadores = int((len(ppdrs*porcentaje_cruza)/100))
if ((no_cruzadores % 2) != 0):
    no_cruzadores+=1
pares = list(range(0, no_cruzadores, 2))
for i in pares:
    hijo1, hijo2 = operadorCruza(ppdrs[i], ppdrs[i+1])
    hijo1 = repairBoard(hijo1)
    hijo2 = repairBoard(hijo2)
    hhjs.append(hijo1)
    hhjs.append(hijo2)

# Mutar hijos
no_mutados = int((len(hhjs*porcentaje_mutacion)/100))
for i in range(no_mutados):
    hhjs[i] = mutateBoard(hhjs[i])

# Actualizar población
ppl = ppl + hhjs
nuevas_apptitudes = []
for index in range(len(ppl)):
        aptitud = calcularAptitud(ppl[index])
        nuevas_apptitudes.append((index,aptitud))
nuevas_apptitudes.sort(key=lambda a: a[1])
nuevas_apptitudes = nuevas_apptitudes[:tamaño_poblacion] 
print(nuevas_apptitudes)
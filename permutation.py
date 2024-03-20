from matplotlib import pyplot as plt
import numpy as np
import random
import math
import chess
import chess.svg

'''Parámetros de entrada
'''
tamaño_poblacion = int(input("Tamaño de la población: "))
porcentaje_cruza = int(input("Porcentaje de cruza: "))
porcentaje_mutacion = int(input("Porcentaje de mutación: "))
evaluacion_limite = int(input("Número de evaluaciones: "))

def permutation2array(permutation):
    array = np.zeros(64)
    array = array.reshape((8,8))
    for i in range(8):
        indx = permutation[i]
        array[indx][i] = 1
    return array

def fitnessFunction(solution):
    row_queens = 0
    col_queens = 0
    dig_queens = 0
    for row in range(solution.shape[0]):
        if (np.sum(solution[row,:]) > 1):
            row_queens += np.sum(solution[row,:]) - 1
    for col in range(solution.shape[1]):
        if (np.sum(solution[:,col]) > 1):
            col_queens += np.sum(solution[:,col]) - 1
    for i in range(-7,7):
        if (np.trace(solution, i) > 1):
            dig_queens += np.trace(solution, i) - 1
        if (np.trace(np.rot90(solution), -i) > 1):
            dig_queens += np.trace(np.rot90(solution), -i) - 1        
    return int(row_queens+col_queens+dig_queens)

def generatePopulation(size):
    population = []
    apptitudes = []
    for index in range (0,size):
        queens = random.sample(range(0, 8), 8)
        # 2. Fitness or aptitude  function with attacks
        apptitude = fitnessFunction(permutation2array(queens))
        apptitudes.append((index,apptitude))
        # 3. Solution population of boards
        population.append(queens)
        #print("{} <--- atacks {} \n".format(solution.astype(int), apptitude))
    return population, apptitudes

def parentSelection(population, fitness):
    parents = random.sample(range(0, len(fitness)), 5)
    temp = []
    for i in parents:
        temp.append(fitness[i])
    temp.sort(key=lambda a: a[1])
    index_1 = temp[0]
    index_2 = temp[1]
    
    parent_1 = population[index_1[0]]
    parent_2 = population[index_2[0]]
    return fitness, parent_1, parent_2 

def crossBoard(solution1, solution2):    
    cross_pt = random.randint(0, 9)
    first_half1  = solution1[:cross_pt]
    second_half1 = solution1[cross_pt:]
    first_half2  = solution2[:cross_pt]
    second_half2 = solution2[cross_pt:]
    sol_1 = np.concatenate((first_half1,second_half2))
    sol_2 = np.concatenate((first_half2,second_half1))
    return sol_1, sol_2

def repairBoard(solution):
    solution.sort()
    toadd = []
    for i in range(8):
        if ((i in solution) == False):
            toadd.append(i)
    a,b = np.unique(solution, return_counts=True)
    todel = []
    for i in range(len(b)):
        if (b[i] > 1):
            todel.append(a[i])
    #print(todel)
    for j in todel:
        #print(j)
        #print(solution)
        solution[j] = 10
    solution = np.delete(solution, np.where(solution == 10))
    #print(solution)
    for i in toadd:
        solution = np.append(solution,i)
    return solution

best_fitness = []
best_average = []
best_solution = 0
flag = False

# 1. Representation, 2. Fitness and 3. Population
population, apptitudes = generatePopulation(tamaño_poblacion)

for count in range(evaluacion_limite):
    # 4. Parent selection
    apptitudes, parent_1, parent_2 = parentSelection(population, apptitudes)

    pc = random.sample(range(0, 100), 1)
    if (pc[0] <= porcentaje_cruza):
        son_1, son_2 = crossBoard(parent_1, parent_2)
    else:
        son_1, son_2 = parent_1, parent_2

    if (len(np.unique(son_1))) != 8:
        son_1 = repairBoard(son_1)
    #print(son_1)

    if (len(np.unique(son_2))) != 8:
        son_2 = repairBoard(son_2)
    #print(son_2)
        
    pm = random.sample(range(0, 100), 1)
    if (pm[0] <= porcentaje_mutacion):
        indxs1 = random.sample(range(0, 8), 2)
        a1 = son_1[indxs1[0]]
        b1 = son_1[indxs1[1]]
        son_1[indxs1[0]] = b1
        son_1[indxs1[1]] = a1

        indxs2 = random.sample(range(0, 8), 2)
        a2 = son_2[indxs2[0]]
        b2 = son_2[indxs2[1]]
        son_2[indxs2[0]] = b2
        son_2[indxs2[1]] = a2

    population.append(list(son_1))
    population.append(list(son_2))
    #print(population)

    nueva_poblacion = []
    nuevas_aptitudes = []
    for index in range (0,tamaño_poblacion):
            apptitude = fitnessFunction(permutation2array(population[index]))
            nuevas_aptitudes.append((index,apptitude))
    nuevas_aptitudes.sort(key=lambda a: a[1])
    apptitudes = nuevas_aptitudes[:tamaño_poblacion] 
 
    for i in apptitudes:
        nueva_poblacion.append(population[i[0]])
    population = nueva_poblacion
    print(apptitudes[0])
'''
    nuevas_aptitudes.clear()
    average_fit = 0
    for index in range(len(population)):
            aptitud = fitnessFunction(permutation2array(population[index]))
            average_fit += aptitud
            nuevas_aptitudes.append((index,aptitud))
    apptitudes = nuevas_aptitudes
    average_fit = average_fit/tamaño_poblacion
    best_fitness.append(apptitudes[0][1])
    best_average.append(average_fit)
    if (apptitudes[0][1] == 0) and (flag == False):
        best_solution = count+1
        flag = True
'''    
print(population[0])
plt.plot(best_fitness, label='Best')
plt.plot(best_average, label='Average')

plt.xlabel("Evaluations")
plt.ylabel("Fitness")
plt.legend() 
plt.show()
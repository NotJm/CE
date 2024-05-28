from problems.cec2006problems import CEC2006_G01
import pyswarms as ps 
import numpy as np
import random as rd
import matplotlib.pyplot as plt
from pyswarms.utils.functions import single_obj as fx
from pyswarms.utils.plotters import plot_cost_history
from core.Restricciones import Restricciones

# Configuración
LimiteSuperior = np.array([1, 1, 1, 1, 1, 1, 1, 1, 1, 100, 100, 100, 1])
LimiteInferior = np.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0])

N_Poblacion = 100
dimensiones = 13

options = {'c1': 1.4944, 'c2': 1.4944, 'w': 0.95}

# Límite de los valores de un individuo
limites = (LimiteInferior, LimiteSuperior)

# Función para calcular el fitness y las violaciones
def Calcular_Fitness_Violaciones(x):
    problema = CEC2006_G01()
    fitness = np.array([problema.fitness(ind) for ind in x])
    
    # Calcular la penalización por restricciones
    penalties = np.zeros(fitness.shape)
    numViolaciones = np.zeros(fitness.shape)
    for i, ind in enumerate(x):
        for g in problema.rest_g:
            g_val = g(ind)
            if g_val > 0:
                penalties[i] += g_val ** 2  # Penalización cuadrática
                numViolaciones[i] += 1

    # Devuelve el fitness ajustado y las violaciones (para evaluación externa)
    return fitness + penalties, numViolaciones

# Función de fitness para PSO
def RetornarFitness(x):
    fitness, _ = Calcular_Fitness_Violaciones(x)
    return fitness

# Crear una instancia del optimizador PSO con restricciones de tipo bound
optimizer = ps.single.GlobalBestPSO(n_particles=N_Poblacion, dimensions=dimensiones, options=options, bounds=limites, bh_strategy="reflective")

# Ejecutar el optimizador
fitness, pos = optimizer.optimize(RetornarFitness, iters=25)

# Evaluar el mejor individuo encontrado 
best_fitness, best_violations = Calcular_Fitness_Violaciones(np.array([pos]))

print("Fitness: ", fitness)
print("Mejor individuo :", pos)
print("Número de violaciones: ", best_violations[0])

# Graficar el historial de costos
plot_cost_history(optimizer.cost_history)
plt.show()
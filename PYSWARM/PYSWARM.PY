from cec2006problems import *
from pyswarms import *
import pyswarms as ps 
import numpy as np
import random as rd
import matplotlib.pyplot as plt
from pyswarms.utils.functions import single_obj as fx
from pyswarms.utils.plotters import plot_cost_history
from Restricciones import *

problema = CEC2006_G02()
# Configuración


N_Poblacion = 100
dimensiones = 20

options = {'c1': 1.4944, 'c2': 1.4944, 'w': 0.95}

# Límite de los valores de un individuo
limites = (problema.INFERIOR, problema.SUPERIOR)


# Crear una instancia del optimizador PSO con restricciones de tipo bound
optimizer = ps.single.GlobalBestPSO(n_particles=N_Poblacion, dimensions=dimensiones, options=options, bounds=limites, bh_strategy="reflective")

# Ejecutar el optimizador
fitness, pos, violaciones= optimizer.optimize(problema.fitness, iters=1000,g_func=problema.rest_g ,h_func=problema.rest_h)



print("Fitness: ", fitness)
print("Mejor individuo :", pos)
print("Mejor violada :", violaciones)
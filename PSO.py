from utils.individuo import generar, isValid
from utils.constantes import NUMERO_DE_POBLACIONES, GENERACIONES, SUPERIOR, INFERIOR
from utils.restricciones import suma_violaciones
import numpy as np
import random as rd

class PSO:
    # Valor de aptitud de cada particula
    fitness = np.zeros(NUMERO_DE_POBLACIONES)
    # Valor de la mejor aptitud de una particula de sus poblacion
    pbestFitness = np.zeros(NUMERO_DE_POBLACIONES)
    # Valor de numero de violaciones por particula
    noViolaciones = np.zeros(NUMERO_DE_POBLACIONES)
    
    gbestAptitud = 0
    gbestViolacion = 0
    gbestIndVio = 0
    gbestIndviduo = []
    gbestVelocidad = [] 
    
        
    W = 0.95
    C1 = 1.4944
    C2 = 1.4944
    
    def __init__(self, limite, evaluar, restr_func, g_funcs=[], h_funcs=[]):
        # Funcion limite a ocupar
        self.limite = limite
        # Funcion aptitud que se va evaluar
        self.evaluar = evaluar
        # Funcion para restricciones funcionales
        self.restr_func = restr_func
        # Lista de funciones de restricciones de desigualdad
        self.g_funcs = g_funcs
        # Lista de funciones de restricciones de igualdad
        self.h_funcs = h_funcs
        # Solo para la generacion para 0
        # Inicializacion de particulas (poblacion) con vectores de posicion y velocidad
        self.particulas = generar(INFERIOR, SUPERIOR)
        self.velocidad = generar(INFERIOR, SUPERIOR)
        # Calculo de la aptitud (fitness) para cada particula (individuo)
        self.calularAptitud()
        # El primer pbest es inicial
        self.pbest = np.copy(self.particulas)
        # Obtener el mejor de la generacion 0
        self.calcularGbest()
    
    # Calculo de la aptitud (fitness) para cada particula (individuo)
    def calularAptitud(self):
        # Calculo del fitness para cada particula
        for index in range(len(self.particulas)):
            # Obtener el fitness
            fitness = self.evaluar(self.particulas[index])
            # Guardar fitness de la particula
            self.fitness[index] = fitness 
            # Guardar fitness del mejor de su poblacion
            self.pbestFitness[index] = fitness
            # Obtener la suma de violaciones
            total_de_violaciones = suma_violaciones(
                self.g_funcs,
                self.h_funcs,
                self.particulas[index]
            )
            # Guardar violacioens
            self.noViolaciones[index] = total_de_violaciones


    def calcularGbest(self):
        pass
            
    def report(self, generacion: int = 0):
        print("PSO Reporte")
        for ind, apt, vio in zip(self.particulas, self.fitness, self.noViolaciones):
            print("Individuo:", ind)
            print("Aptitud (Fitness):", apt)
            print("No Violaciones:", vio)
            print("Valido:", isValid(SUPERIOR, INFERIOR, ind))
        print("\n")
        print("Solucion Optima")
        print("Individuo:", self.gbestIndviduo)
        print("Fitness:", self.gbestAptitud)
        print("Num Violaciones:", self.gbestViolacion)
    def start(self):
        generacion = 1
        while generacion < GENERACIONES:
            self.actualizarVelocidad()
            self.actualizarPoblacion()
            self.actualizarAptitud()
            self.actualizarGbest()
            
            generacion += 1

    def reset(self):
        # Solo para la generacion para 0
        # Inicializacion de particulas (poblacion) con vectores de posicion y velocidad
        self.particulas = generar(INFERIOR, SUPERIOR)
        self.velocidad = generar(INFERIOR, SUPERIOR)
        # Calculo de la aptitud (fitness) para cada particula (individuo)
        self.calularAptitud()
        # El primer pbest es inicial
        self.pbest = np.copy(self.particulas)
        # Obtener el mejor de la generacion 0
        self.calculoGbest()


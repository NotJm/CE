from utils.constantes import NUMERO_DE_POBLACIONES, GENERACIONES
from utils.restricciones import suma_violaciones
from utils.restricciones import aEsMejorQueB_deb
from utils.Algorithm import Algorithm
import numpy as np
import random as rd

class PSO(Algorithm):
    # Particulas
    particulas = []
    # Velocidad de las particulas
    velocidad = []
    # Valor de aptitud de cada particula
    fitness = np.zeros(NUMERO_DE_POBLACIONES)
    # Valor de numero de violaciones por particula
    noViolaciones = np.zeros(NUMERO_DE_POBLACIONES)
    
    # Memoria de la mejor posicion de la particula
    pbest = []
    # Memoria del valor de la mejor aptitud de una particula de sus poblacion
    pbestFitness = []
    # Memoria del mejor numero de violaciones que tuvo la particula
    pbestViolaciones = []
    
    
    # Mejor aptitud de la particula
    gbestAptitud = 0
    # Mejor violacion de la particula <= 0
    gbestViolacion = 0
    # Mejor particula de la generacion    
    gbestParticula = []
    # Mejor velocidad de la particula
    gbestVelocidad = [] 
    
        
    W = 0.95
    C1 = 1.4944
    C2 = 1.4944
    
    def __init__(
        self,
        limite, # Funcion para limitar la particula
        evaluar, # Funcion para evaluar la particula
        superior,
        inferior,
        restr_func, # Funcion para restringir la funcion objectiva
        act_vel, # Funcion de Estrategia de actualizacion de velocidad
        g_funcs=[], # Lista de funciones de desigualdad <= 0
        h_funcs=[] # Lista de funciones de igualdad == 0
    ):
        # Funcion limite a ocupar
        self.limite = limite
        # Funcion aptitud que se va evaluar
        self.evaluar = evaluar
        # Limites self.superiores e self.inferiores
        self.superior = superior
        self.inferior = inferior
        # Funcion para restricciones funcionales
        self.restr_func = restr_func
        # Lista de funciones de restricciones de desigualdad
        self.g_funcs = g_funcs
        # Lista de funciones de restricciones de igualdad
        self.h_funcs = h_funcs
        # Estrategia para actualizar la velocidad
        self.act_vel = act_vel
        # Solo para la generacion para 0
        # Inicializacion de particulas (poblacion) con vectores de posicion y velocidad
        self.particulas = self.generar(self.inferior, self.superior)
        self.velocidad = self.generar(self.inferior, self.superior)
        # Calculo de la aptitud (fitness) para cada particula (individuo)
        self.calcularAptitud()
        # El primer pbest es inicial
        self.pbest = np.copy(self.particulas)
        # El primer pbesfitness es inicial
        self.pbestFitness = np.copy(self.fitness)
        # Memoria de violaciones que tuvo la particuka
        self.pbestViolaciones = np.copy(self.noViolaciones)
        # Obtener el mejor de la generacion 0
        self.calcularGbest()

        
    
    # Calculo de la aptitud (fitness) para cada particula (individuo)
    def calcularAptitud(self):
        # Calculo del fitness para cada particula
        for index, particula in enumerate(self.particulas):
            # Obtener el fitness
            fitness = self.evaluar(particula)
            # Guardar fitness de la particula
            self.fitness[index] = fitness 
            # Obtener la suma de violaciones
            total_de_violaciones = suma_violaciones(
                self.g_funcs,
                self.h_funcs,
                particula
            )

            # Guardar violacioens
            self.noViolaciones[index] = total_de_violaciones
        
        
    def calcularGbest(self):
        posicion = self.restr_func(self.particulas, self.fitness, self.noViolaciones)
        
        self.gbestParticula = self.particulas[posicion]
        self.gbestAptitud = self.fitness[posicion]
        self.gbestViolacion = self.noViolaciones[posicion]

    def actualizarPbest(self):
        for index in range(NUMERO_DE_POBLACIONES):
            # Si el número de violaciones coincide con el anterior
            
            if aEsMejorQueB_deb(self.pbestFitness[index] , self.pbestViolaciones[index], self.fitness[index], self.noViolaciones[index]) == False:
                self.pbest[index] = np.copy(self.particulas[index])
                self.pbestFitness[index] = self.fitness[index]
                self.pbestViolaciones[index] = self.noViolaciones[index]
                

    def actualizarAptitud(self):
        # Actualizar el ftiness de las particulas actuales de la generacion
        self.calcularAptitud()
        
        # Actualizar el pbest
        self.actualizarPbest()
        
    
    def actualizarVelocidad(self):
        for index in range(NUMERO_DE_POBLACIONES):
            for jndex in range(len(self.velocidad[index])):
                r1 = rd.uniform(0, 1)
                r2 = rd.uniform(0, 1)
                actVelocidad = (self.W * self.velocidad[index][jndex] + 
                                self.C1 * r1 * (self.pbest[index][jndex] - self.velocidad[index][jndex]) + 
                                    self.C2 * r2 * (self.gbestParticula[jndex] - self.velocidad[index][jndex]))
                self.velocidad[index][jndex] = actVelocidad
                
    def actualizarGbest(self):
        self.calcularGbest()
        
    def actualizarPosicion(self):
        for index in range(NUMERO_DE_POBLACIONES):
            for jndex in range(len(self.velocidad[index])):
                self.particulas[index][jndex] = self.particulas[index][jndex] + self.velocidad[index][jndex]
                
    def restriccionLimites(self):
        for index in range(NUMERO_DE_POBLACIONES):
            if not self.isValid(self.superior, self.inferior, self.particulas[index]):
                self.particulas[index] = self.limite(self.superior, self.inferior, self.particulas[index])
                self.velocidad[index] = self.act_vel(self.velocidad[index])
    
    def report(self):
        print("PSO Reporte")
        print("Solucion Optima")
        print("Individuo:", self.gbestParticula)
        print("Fitness:", self.gbestAptitud)
        print("Num Violaciones:", self.gbestViolacion)       
            
    def start(self):
        generacion = 1
        while generacion < GENERACIONES:
            self.actualizarVelocidad()
            self.actualizarPosicion()
            self.restriccionLimites()
            self.actualizarAptitud()
            self.actualizarGbest()
            
            generacion += 1
        
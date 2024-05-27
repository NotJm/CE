from utils.constantes import NUMERO_DE_POBLACIONES, GENERACIONES
from core.Restricciones import Restricciones
from core.Algorithm import Algorithm
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
    
    # Factor de inercia
    W = 0.95
    # Coeficiente aceleracion cognitiva
    C1 = 1.4944
    # Coeficiente aceleracion social
    C2 = 1.4944
    
    def __init__(
        self,
        limite, # Funcion para limitar la particula
        evaluar, # Funcion para evaluar la particula
        superior, # Limite Superior de la particulas
        inferior, # Limite Inferior de la particulas
        restriccion_de_funcion, # Funcion para restringir la funcion objectiva
        correcion_de_velocidad, # Funcion de Estrategia de actualizacion de velocidad
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
        self.restriccion_de_funcion = restriccion_de_funcion
        # Lista de funciones de restricciones de desigualdad
        self.g_funcs = g_funcs
        # Lista de funciones de restricciones de igualdad
        self.h_funcs = h_funcs
        # Estrategia para actualizar la velocidad
        self.act_vel = correcion_de_velocidad
        # Solo para la generacion para 0
        # Inicializacion de particulas (poblacion) con vectores de posicion y velocidad
        self.particulas = self.generar(self.inferior, self.superior)
        self.velocidad = self.generar(self.inferior, self.superior)
        # Calculo de la aptitud (fitness) para cada particula (individuo)
        self.calcularFitnessYSumaDeViolaciones()
        # El primer pbest es inicial
        self.pbest = np.copy(self.particulas)
        # El primer pbesfitness es inicial
        self.pbestFitness = np.copy(self.fitness)
        # Memoria de violaciones que tuvo la particuka
        self.pbestViolaciones = np.copy(self.noViolaciones)
        # Obtener el mejor de la generacion 0
        self.obtenerGgestPoblacion0()

        
    
    # Calculo de la aptitud (fitness) para cada particula (individuo)
    def calcularFitnessYSumaDeViolaciones(self):
        # Calculo del fitness para cada particula
        for index, particula in enumerate(self.particulas):
            # Obtener el fitness
            fitness = self.evaluar(particula)
            # Guardar fitness de la particula
            self.fitness[index] = fitness 
            # Obtener la suma de violaciones
            total_de_violaciones = Restricciones.suma_violaciones(
                self.g_funcs,
                self.h_funcs,
                particula
            )

            # Guardar violacioens
            self.noViolaciones[index] = total_de_violaciones
        
        
    

    def actualizarPbest(self):
        for index in range(NUMERO_DE_POBLACIONES):
            # Si el número de violaciones coincide con el anterior
            if self.restriccion_de_funcion(self.pbestFitness[index] , self.pbestViolaciones[index], self.fitness[index], self.noViolaciones[index]) == False:
                self.pbest[index] = np.copy(self.particulas[index])
                self.pbestFitness[index] = self.fitness[index]
                self.pbestViolaciones[index] = self.noViolaciones[index]
                

   
    
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
            
    def obtenerGbestPoblacion0(self):
        posInicialGbest=0
        self.gbestParticula = self.particulas[posInicialGbest]
        self.gbestAptitud = self.fitness[posInicialGbest]
        self.gbestViolacion = self.noViolaciones[posInicialGbest]
        self.actualizarPosicionGbestDePoblacion()
        
    def actualizarPosicionGbestDePoblacion(self):
        for x in range(0, len(self.particulas)):

            current_fitness = self.fitness[x]
            current_violacion = self.noViolaciones[x]
            
            if self.restriccion_de_funcion(self.gbestAptitud, self.gbestViolacion, current_fitness, current_violacion) == False:
                self.gbestAptitud = current_fitness
                self.gbestViolacion = current_violacion
                self.gbestParticula = self.particulas[x]      
    
    
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
            self.calcularFitnessYSumaDeViolaciones()
            self.actualizarPbest()
            self.actualizarPosicionGbestDePoblacion()
            
            generacion += 1
        
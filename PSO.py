from utils.individuo import (generar, isValid, NP, GENERACIONES)
from utils.limites import (boundary, reflex, random)
from utils.velocidad import (dba, rba)
from utils.restricciones import (g01, g02, evaluar)
import numpy as np
import random as rd
import time as tm
class PSO:

    superior = [
        10, 10, 10, 10, 10, 10, 10, 10, 10, 10,
        10, 10, 10, 10, 10, 10, 10, 10, 10, 10,
    ]
    inferior = [
        0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
        0, 0, 0, 0, 0, 0, 0, 0, 0, 0
    ]
    
    fitness = pbestFitness = np.zeros(NP)
        
    noViolaciones = np.zeros(NP)
    
    gbestAptitud:float = 0
    gbestViolacion:float = 0
    gbestIndVio:float = 0
    gbestIndviduo = []
    gbestVelocidad = []
        
    W = 0.95
    C1 = 1.4944
    C2 = 1.4944
    
    def __init__(self, limite:str):
        self.limite = limite
        # Solo para la generacion para 0
        # Inicializacion de particulas (poblacion) con vectores de posicion y velocidad
        self.poblacion = generar(self.inferior, self.superior)
        self.velocidad = generar(self.inferior, self.superior)
        # Calculo de la aptitud (fitness) para cada particula (individuo)
        self.calularAptitud()
        # El primer pbest es inicial
        self.pbest = np.copy(self.poblacion)
        # Obtener el mejor de la generacion 0
        self.calculoGbest()
    
    # Calculo de la aptitud (fitness) para cada particula (individuo)
    def calularAptitud(self):
        for x in range(NP):
            evaluacion = evaluar(self.poblacion[x], g02)
            self.fitness[x] = evaluacion["fitness"]
            self.pbestFitness[x] = evaluacion["fitness"]
            self.noViolaciones[x] = evaluacion["noViolaciones"]
    
    
    def evaluacionPbest(self):
        for i in range(len(self.pbest)):
            # Aptitud actual del individuo
            currentFitness = self.fitness[i]
            # Violaciones actuales del individuo
            currentViolaciones = self.noViolaciones[i]
            # Mejor aptitud personal hasta ahora
            pbestFitness = self.pbestFitness[i]
            # Mejor número de violaciones personal hasta ahora
            pbestViolaciones = self.noViolaciones[i]

            if currentViolaciones == 0 and pbestViolaciones == 0:  # Ambas soluciones son factibles
                if currentFitness < pbestFitness:  # Si la aptitud actual es mejor que el pbest
                    # Actualiza la mejor posición personal
                    self.pbest[i] = self.poblacion[i]
                    # Actualiza la mejor aptitud personal
                    self.pbestFitness[i] = currentFitness
                    # Actualiza el número de violaciones personal
                    self.noViolaciones[i] = currentViolaciones
            elif currentViolaciones == 0 and pbestViolaciones > 0:  # La actual es factible, el pbest no
                # Actualiza la mejor posición personal
                self.pbest[i] = self.poblacion[i]
                # Actualiza la mejor aptitud personal
                self.pbestFitness[i] = currentFitness
                # Actualiza el número de violaciones personal
                self.noViolaciones[i] = currentViolaciones
            elif currentViolaciones > 0 and pbestViolaciones == 0:  # El pbest es factible, la actual no
                continue  # No actualizar el pbest
            else:  # Ambas soluciones no son factibles
                if currentViolaciones < pbestViolaciones:  # Si la actual tiene menos violaciones
                    # Actualiza la mejor posición personal
                    self.pbest[i] = self.poblacion[i]
                    # Actualiza la mejor aptitud personal
                    self.pbestFitness[i] = currentFitness
                    # Actualiza el número de violaciones personal
                    self.noViolaciones[i] = currentViolaciones
                elif currentViolaciones == pbestViolaciones and currentFitness < pbestFitness:  # Si tienen el mismo número de violaciones pero mejor aptitud
                    # Actualiza la mejor posición personal
                    self.pbest[i] = self.poblacion[i]
                    # Actualiza la mejor aptitud personal
                    self.pbestFitness[i] = currentFitness
                    # Actualiza el número de violaciones personal
                    self.noViolaciones[i] = currentViolaciones



    def calculoGbest(self):
        gbestIndex = 0  # Índice del mejor global
        gbestM = self.pbestFitness[0]
        gbestV = self.noViolaciones[0]

        # Itera a través de todos los valores de aptitud (fitness) personales (pbest)
        for i in range(1, len(self.pbestFitness)):
            currentM = self.pbestFitness[i]
            currentV = self.noViolaciones[i]

            if gbestV == 0 and currentV == 0:  # Ambas soluciones son factibles
                if currentM < gbestM: 
                    gbestM = currentM  
                    gbestIndex = i  
            elif gbestV == 0 and currentV > 0:  # La mejor global es factible, la actual no
                continue  # Continúa con la siguiente iteración
            elif gbestV > 0 and currentV == 0:  # La mejor global no es factible, la actual sí
                gbestM = currentM  
                gbestV = currentV  
                gbestIndex = i  
            else:  # Ambas soluciones no son factibles
                if currentV < gbestV:  
                    gbestM = currentM  
                    gbestV = currentV  
                    gbestIndex = i  
                elif currentV == gbestV and currentM < gbestM:  # Si tienen el mismo número de violaciones pero mejor aptitud
                    gbestM = currentM  
                    gbestIndex = i  

        self.gbestIndviduo = self.pbest[gbestIndex]  # Actualiza el mejor individuo global
        self.gbestAptitud = gbestM  # Actualiza la mejor aptitud global
        self.gbestViolaciones = gbestV  # Actualiza el número de violaciones del mejor global
        self.gbestIndVio = self.noViolaciones[gbestIndex] # Actualiza el número de
        self.gbestVelocidad = self.velocidad[gbestIndex] # Actualiza el número de

                
    def actualizarVelocidad(self):
        for index in range(NP):
            rba(self.velocidad[index])      
            for jndex in range(len(self.velocidad[index])):
                r1 = rd.uniform(0, 1)
                r2 = rd.uniform(0, 1)
                actVelocidad = (self.W * self.velocidad[index][jndex] + 
                                self.C1 * r1 * (self.pbest[index][jndex] - self.velocidad[index][jndex]) + 
                                    self.C2 * r2 * (self.gbestIndviduo[jndex] - self.velocidad[index][jndex]))
                self.velocidad[index][jndex] = actVelocidad
            
    def actualizarGbest(self):
        self.calculoGbest()
        
    def actualizarPoblacion(self):
        for index in range(NP):
            for jndex in range(len(self.velocidad[index])):
                self.poblacion[index][jndex] = self.poblacion[index][jndex] + self.velocidad[index][jndex]
            
                
            if self.limite == "reflex":
                # ! Limite reflex
                self.poblacion[index] = reflex(self.superior, self.inferior, self.poblacion[index])
            elif self.limite == "random":
                # ! Limite random
                self.poblacion[index] = random(self.superior, self.inferior, self.poblacion[index])
            elif self.limite == "boundary":
                #! Limite bouncy
                self.poblacion[index] = boundary(self.superior, self.inferior, self.poblacion[index])
            
    def actualizarAptitud(self):
        self.calularAptitud()
        
        self.evaluacionPbest()
        
    def report_actulizacion(self):
        pass
    
    def report(self, generacion:int = 0):
        print("PSO Reporte")
        # for ind, apt, vio in zip(self.poblacion, self.fitness, self.noViolaciones):
        #     print("Individuo:", ind)
        #     print("Aptitud (Fitness):", apt)
        #     print("No Violaciones:", vio)
        #     print("Valido:", isValid(self.superior, self.inferior, ind))
        # print("\n")
        print("Mejor Individuo:", self.gbestIndviduo)
        print("Mejor Aptitud(Fitness):", self.gbestAptitud)
        print("Mejor Velocidad:", self.gbestVelocidad)
        print("No Violaciones:", "Sin Violaciones" if self.gbestIndVio == 0 else self.gbestIndVio)
        print("Valido:", isValid(self.superior, self.inferior, self.gbestIndviduo))
        print("\n")
        
    def start(self):
        generacion = 1
        while generacion < GENERACIONES:
            self.actualizarVelocidad()
            self.actualizarPoblacion()
            self.actualizarAptitud()
            self.actualizarGbest()
            
            poblacion_list = self.poblacion.tolist()
            random_individuos = rd.sample(poblacion_list, k=5)
            for i, individuo in enumerate(random_individuos):
                if self.noViolaciones[i] > 0:
                    ...
                    # print(f"Generación {generacion}:")
                    # print("********************************")
                    # print(f"Individuo {i+1}: {individuo}")
                    # print("Aptitud(Fitness):", self.fitness[i])
                    # print("NoViolacion:", self.noViolaciones[i])
                    # print("Valido:", isValid(self.superior, self.inferior, individuo))
                    # print("********************************")                  
            generacion += 1

    def reset(self):
        # Solo para la generacion para 0
        # Inicializacion de particulas (poblacion) con vectores de posicion y velocidad
        self.poblacion = generar(self.inferior, self.superior)
        self.velocidad = generar(self.inferior, self.superior)
        # Calculo de la aptitud (fitness) para cada particula (individuo)
        self.calularAptitud()
        # El primer pbest es inicial
        self.pbest = np.copy(self.poblacion)
        # Obtener el mejor de la generacion 0
        self.calculoGbest()
            
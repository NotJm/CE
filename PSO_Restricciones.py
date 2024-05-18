import numpy as np
import random
import math

class PSO_restricciones:
    NUMERO_POBLACION = 20 
    NUMERO_GENERACION = 1000
    NUMERO_DE_DIMENSIONES = 20
    
    _poblacion = np.zeros((NUMERO_POBLACION, NUMERO_DE_DIMENSIONES))
    _velocidad = np.zeros((NUMERO_POBLACION, NUMERO_DE_DIMENSIONES))
    _fitness = np.zeros(NUMERO_POBLACION)

    _gbest_c = np.zeros(NUMERO_DE_DIMENSIONES)  # gbest coordinates (position)
    _gbest_f = float('inf')  # gbest fitness (initialize to inf for minimization)

    _pbest = np.zeros((NUMERO_POBLACION, NUMERO_DE_DIMENSIONES))
    _pbest_fitness = np.full(NUMERO_POBLACION, float('inf'))
    
    _data_fitness = []

    MAX = 10
    MIN = 0

    W = 0.95
    C1 = 1.4944
    C2 = 1.4944

    def __init__(self):
        # Initialize individuals
        self._generar_poblacion()
        # Initialize velocities of the population
        self._generar_velocidad()
        # Initialize fitness
        self._calculo_fitness()
        # Initialize gBest
        self._calculo_gbest_()

    def _generar_individuo(self):
        return np.array([random.uniform(self.MIN, self.MAX) for _ in range(self.NUMERO_DE_DIMENSIONES)])
    
    def _generar_poblacion(self):
        for i in range(self.NUMERO_POBLACION):
            self._poblacion[i] = self._generar_individuo()
            self._pbest[i] = self._poblacion[i]
    
    def _generar_velocidad(self):
        for i in range(self.NUMERO_POBLACION):
            self._velocidad[i] = np.array([random.uniform(-1, 1) for _ in range(self.NUMERO_DE_DIMENSIONES)])

    def _calculo_fitness(self):
        for i in range(self.NUMERO_POBLACION):
            self._fitness[i] = self.funcion_objetivo(self._poblacion[i])
            self._pbest_fitness[i] = self._fitness[i]

    def funcion_objetivo(self, x):
        num = np.sum(np.cos(x)**4) - 2 * np.prod(np.cos(x)**2)
        den = np.sqrt(np.sum([(i+1) * x[i]**2 for i in range(self.NUMERO_DE_DIMENSIONES)]))
        return -abs(num / den)
    
    def g1(self, x):
        return 0.75 - np.prod(x)
    
    def g2(self, x):
        return np.sum(x) - 7.5 * self.NUMERO_DE_DIMENSIONES

    def calcular_violaciones(self, x):
        violaciones = 0
        if self.g1(x) > 0:
            violaciones += self.g1(x)**2
        if self.g2(x) > 0:
            violaciones += self.g2(x)**2
        return violaciones

    def _actualizar_pbest_(self): 
        for i in range(self.NUMERO_POBLACION):
            if self._fitness[i] < self._pbest_fitness[i]:
                self._pbest[i] = self._poblacion[i]
                self._pbest_fitness[i] = self._fitness[i]

    def _calculo_gbest_(self): 
        index = np.argmin(self._pbest_fitness)
        self._gbest_f = self._pbest_fitness[index] 
        self._gbest_c = self._poblacion[index]

    def _actualizar_fitness(self):
        for i in range(self.NUMERO_POBLACION):
            self._fitness[i] = self.funcion_objetivo(self._poblacion[i])
            violaciones = self.calcular_violaciones(self._poblacion[i])
            self._fitness[i] += violaciones

            if self._fitness[i] < self._pbest_fitness[i]:
                self._pbest_fitness[i] = self._fitness[i]
                self._pbest[i] = self._poblacion[i]

    def _actualizar_velocidad(self):
        for i in range(self.NUMERO_POBLACION):
            r1 = random.random()
            r2 = random.random()
            self._velocidad[i] = (self.W * self._velocidad[i] +
                                  self.C1 * r1 * (self._pbest[i] - self._poblacion[i]) +
                                  self.C2 * r2 * (self._gbest_c - self._poblacion[i]))

    def _actualizar_poblacion(self):
        for i in range(self.NUMERO_POBLACION):
            self._poblacion[i] = self._poblacion[i] + self._velocidad[i]
            self._poblacion[i] = np.clip(self._poblacion[i], self.MIN, self.MAX)

    def start(self):
        for generacion in range(self.NUMERO_GENERACION):
            self._actualizar_velocidad()
            self._actualizar_poblacion()
            self._actualizar_fitness()
            self._calculo_gbest_()
            self._data_fitness.append(self._gbest_f)
            print(f'Generación {generacion}: Mejor Fitness {self._gbest_f}')
        
        print("Mejor Individuo:", self._gbest_c)
        print("Mejor Fitness:", self._gbest_f)

# Ejecución del PSO con restricciones
pso = PSO_restricciones()
pso.start()

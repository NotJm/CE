import numpy as np
import random

class PSO:
    NUMERO_POBLACION = 10
    NUMERO_GENERACION = 30

    #numero de individios en la poblacion
    # 10 son las filas y 2 son las columnas
    _poblacion = np.zeros((NUMERO_POBLACION, 2))
    _velocidad = np.zeros((NUMERO_POBLACION, 2))
    _fitness   = np.zeros(NUMERO_POBLACION)

    _gbest_c = np.zeros(2)  #gbest cordenadas(posicion)
    _gbest_f = 0  #gbest fitness

    _pbest = np.zeros((NUMERO_POBLACION, 2))
    _pbest_fitness = np.zeros(NUMERO_POBLACION)

    limite_inferior = -20
    limite_superior = 20

    
    W = 0.95
    C1 = 1.4944
    C2 = 1.4944



    # Constructor
    def __init__(self):
        # Inicializacion de los individuos
        self._generar_individuo()
        # Inicializacion de la poblacion
        self._generar_poblacion()
        # Inicializacion de la velocidad de la poblacion
        self._generar_velocidad()
        # Inicilizacion del fitness
        self._calculo_fitness()
        # Inicilizacion del gBest
        self._calculo_gbest_()
        
    #genera valores aleatorios
    def _generar_individuo(self):
        # Crear un arreg
        _list = []
        # Solo dos valores
        for _ in range(2):
            # Generar valores aleatorios flotantes dentro del rango -20 a 20
            _list.append(random.uniform(-20, 20))
        # Regresa el arreglo como objeto numpy
        return np.array(_list)
    
    #genera una poblacion y la almacena en una matriz
    def _generar_poblacion(self):
        # Generacion  de la poblacion
        for i in range(self.NUMERO_POBLACION):
            # Se obtiene el individuo
            _individuo = self._generar_individuo()
            # Se añade a la poblacion
            self._poblacion[i] = _individuo

        for i in range(self.NUMERO_POBLACION):
            self._pbest[i] = self._poblacion[i]
    
    # Generar velocidades
    def _generar_velocidad(self):
        # Solo dos valores
        for i in range(self.NUMERO_POBLACION):
            # Generar valores aleatorios flotantes dentro del rango -20 a 20
            _velocidad = self._velocidad[i]
            # Generar numeros aleatorios para la velocidad
            for j in range(len(_velocidad)):
                # Generar numeros aleatorios
                _velocidad[j] = random.uniform(-20, 20)

            self._velocidad[i] = _velocidad

    # Actualizcion de pBest
    def _actualizar_pbest_(self): 
        for i in range(self.NUMERO_POBLACION):
            if self._fitness[i] < self._pbest_fitness[i]:
                self._pbest[i] = self._poblacion[i]
                self._pbest_fitness[i] = self._fitness[i]

    def _calculo_gbest_(self): 
        # Obtener el valor minimo
        index = np.argmin(self._pbest_fitness)
        self._gbest_f = self._pbest_fitness[index] 
        self._gbest_c = self._poblacion[index]

            
            
    # Calculo de fitness
    def _calculo_fitness(self):
        # (x1 ** 3 + x2 ** 3) / 100
        for i in range(self.NUMERO_POBLACION):
            # Extraigo el individuo de la poblacin
            _individuo = self._poblacion[i]
            # xObtengo el x1 y el x2 del individuo
            x1, x2 = _individuo
            # Calculo del fitness
            fitness = (x1 ** 3 + x2 ** 3) / 100
            # Guardo el fitness
            self._fitness[i] = fitness

            self._pbest_fitness[i] = fitness

    # Actualizacion de velocidad            
    def _actualizar_velocidad(self):
        for i in range(self.NUMERO_POBLACION):
            for j in range(len(self._velocidad[i])):
                r1 = random.random()
                r2 = random.random()
                v2 = self.W * self._velocidad[i][j] + self.C1 * r1 * (self._pbest[i][j] - self._velocidad[i][j]) + self.C2 * r2 * (self._gbest_c[j] - self._velocidad[i][j])
                
                if v2 < self.limite_inferior:
                    self._velocidad[i][j] = self.limite_inferior
                elif v2 > self.limite_superior:
                    self._velocidad[i][j] = self.limite_superior
                else:
                   self._velocidad[i][j] = v2

    #Actualización de la población
    def _actualizar_poblacion(self):
        for i in range (self.NUMERO_POBLACION):
            for j in range(len(self._velocidad[i])):
                self._poblacion[i][j] = self._poblacion[i][j] + self._velocidad[i][j] 
                if self._poblacion[i][j] < self.limite_inferior:
                    self._poblacion[i][j] = self.limite_inferior
                elif self._poblacion[i][j] > self.limite_superior:
                    self._poblacion[i][j] = self.limite_superior
                else:
                    self._poblacion[i][j] = self._poblacion[i][j] 
                    
    #Calcular el nuevo fitness
    def _actualizar_fitness(self):
        self._calculo_fitness()
        for i in range (self.NUMERO_POBLACION):
                if (self._fitness[i] <= self._pbest_fitness[i]):
                    self._pbest_fitness[i] = self._fitness[i]
                    self._pbest[i] = self._poblacion[i]
                    
    def _actualizar_gbest(self):
        self._calculo_gbest_()

    def start(self):
        generacion = 0
        while generacion < self.NUMERO_GENERACION:
            self._actualizar_velocidad()

            self._actualizar_poblacion()

            self._actualizar_fitness()

            self._actualizar_gbest()

            generacion += 1

        
    #imprime el arreglo
    def __str__(self) -> str: 
        return f"""GBEST FITNESS \n {self._gbest_f}\n INDIVIDUO \n{self._gbest_c}"""

if __name__ == '__main__':
    pso = PSO()
    pso.start()
    print(-160) 
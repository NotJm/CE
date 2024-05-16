import numpy as np
import random
from matplotlib import pyplot as plt

#             /$$$$$$                               
#            /$$__  $$                              
#   /$$$$$$ | $$  \__/  /$$$$$$   /$$$$$$  /$$$$$$$ 
#  /$$__  $$| $$$$     /$$__  $$ /$$__  $$| $$__  $$
# | $$$$$$$$| $$_/    | $$  \__/| $$$$$$$$| $$  \ $$
# | $$_____/| $$      | $$      | $$_____/| $$  | $$
# |  $$$$$$$| $$      | $$      |  $$$$$$$| $$  | $$
#  \_______/|__/      |__/       \_______/|__/  |__/
                                                  


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

    MAX = -20
    MIN = 20

    
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

        self.convergence = []
        
    #genera valores aleatorios
    def _generar_individuo(self):
        # Crear un arreglo
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
                
                # TODO: Restricciones
                self._velocidad[i][j] = self._restriccion_reflex_(v2)

                # self._velocidad[i][j] = self._restriccion_random_(v2)
                

    #Actualización de la población
    def _actualizar_poblacion(self):
        for i in range (self.NUMERO_POBLACION):
            for j in range(len(self._velocidad[i])):
                self._poblacion[i][j] = self._poblacion[i][j] + self._velocidad[i][j] 



                self._poblacion[i][j] = self._restriccion_reflex_(self._poblacion[i][j]) 
                
                # self._poblacion[i][j] = self._restriccion_random_(self._poblacion[i][j])
                    
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
         for corrida in range(self.NUM_CORRIDAS):
            # Restablecer población y variables
            self._reset()
            generacion = 0
            while generacion < self.NUMERO_GENERACION:
                self._actualizar_velocidad()

                self._actualizar_poblacion()

                self._actualizar_fitness()

                self._actualizar_gbest()

                print("Generacion:", generacion)
                print("Coordenadas:",self._gbest_c)
                print("Fitness:",self._gbest_f)


                self.convergence.append(self._gbest_f)
                generacion += 1


            self.convergence = sorted(self.convergence, reverse=True)
            self.plot_convergence()
    
    def _restriccion_random_(self , eval):
        if eval > self.MAX or eval < self.MIN:
                    eval = self.MIN + random.uniform(0, 1) * (self.MAX - self.MIN)
        return eval
    
    
    def _restriccion_reflex_(self, eval, lower_limit=-20, upper_limit=20):
        if eval < lower_limit:
            eval = lower_limit + abs(eval - lower_limit)
        elif eval > upper_limit:
            eval = upper_limit - abs(eval - upper_limit)
        return eval
        
    #imprime el arreglo
    def __str__(self) -> str: 
        return f"""GBEST FITNESS \n {self._gbest_f}\n INDIVIDUO \n{self._gbest_c}"""


    def plot_convergence(self):
        # Crear una lista de generaciones
        generaciones = np.arange(1, self.NUMERO_GENERACION + 1)

        # Crear el gráfico
        plt.plot(generaciones, self.convergence, marker='o', linestyle='-')
        plt.title('Convergencia de PSO')
        plt.xlabel('Generación')
        plt.ylabel('Mejor Fitness')
        plt.grid(True)
        plt.show()


     def _reset(self):
        # Restablecer la población, velocidad, fitness, etc.
        self._poblacion = np.zeros((self.NUMERO_POBLACION, 2))
        self._velocidad = np.zeros((self.NUMERO_POBLACION, 2))
        self._fitness = np.zeros(self.NUMERO_POBLACION)
        self._pbest = np.zeros((self.NUMERO_POBLACION, 2))
        self._pbest_fitness = np.zeros(self.NUMERO_POBLACION)
        self._gbest_c = np.zeros(2)
        self._gbest_f = 0

        self._generar_poblacion()
        self._generar_velocidad()
        self._calculo_fitness()
        self._calculo_gbest_()
        
        
if __name__ == '__main__':
    pso = PSO()
    print("""
                                                          
                                                          
PPPPPPPPPPPPPPPPP      SSSSSSSSSSSSSSS      OOOOOOOOO     
P::::::::::::::::P   SS:::::::::::::::S   OO:::::::::OO   
P::::::PPPPPP:::::P S:::::SSSSSS::::::S OO:::::::::::::OO 
PP:::::P     P:::::PS:::::S     SSSSSSSO:::::::OOO:::::::O
  P::::P     P:::::PS:::::S            O::::::O   O::::::O
  P::::P     P:::::PS:::::S            O:::::O     O:::::O
  P::::PPPPPP:::::P  S::::SSSS         O:::::O     O:::::O
  P:::::::::::::PP    SS::::::SSSSS    O:::::O     O:::::O
  P::::PPPPPPPPP        SSS::::::::SS  O:::::O     O:::::O
  P::::P                   SSSSSS::::S O:::::O     O:::::O
  P::::P                        S:::::SO:::::O     O:::::O
  P::::P                        S:::::SO::::::O   O::::::O
PP::::::PP          SSSSSSS     S:::::SO:::::::OOO:::::::O
P::::::::P          S::::::SSSSSS:::::S OO:::::::::::::OO 
P::::::::P          S:::::::::::::::SS    OO:::::::::OO   
PPPPPPPPPP           SSSSSSSSSSSSSSS        OOOOOOOOO     
                                                          
                                                          
                                                          
                                                          
                                                          
                                                          
                                                          
""")
    pso.start()
    print("\n")
    print(pso)

    

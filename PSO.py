import numpy as np
import random
from matplotlib import pyplot as plt
import math

#             /$$$$$$                               
#            /$$__  $$                              
#   /$$$$$$ | $$  \__/  /$$$$$$   /$$$$$$  /$$$$$$$ 
#  /$$__  $$| $$$$     /$$__  $$ /$$__  $$| $$__  $$
# | $$$$$$$$| $$_/    | $$  \__/| $$$$$$$$| $$  \ $$
# | $$_____/| $$      | $$      | $$_____/| $$  | $$
# |  $$$$$$$| $$      | $$      |  $$$$$$$| $$  | $$
#  \_______/|__/      |__/       \_______/|__/  |__/
                                                  
NUMERO_CORRIDAS = 150

class PSO:
    NUMERO_POBLACION = 10
    NUMERO_GENERACION = 1000
    NUMERO_DE_DIMENSIONES = 10

    #numero de individios en la poblacion
    # 10 son las filas y 2 son las columnas
    _poblacion = np.zeros((NUMERO_POBLACION, NUMERO_DE_DIMENSIONES))
    _velocidad = np.zeros((NUMERO_POBLACION, NUMERO_DE_DIMENSIONES))
    _fitness   = np.zeros(NUMERO_POBLACION)

    _gbest_c = np.zeros(NUMERO_DE_DIMENSIONES)  #gbest cordenadas(posicion)
    _gbest_f = 0  #gbest fitness

    _pbest = np.zeros((NUMERO_POBLACION, NUMERO_DE_DIMENSIONES))
    _pbest_fitness = np.zeros(NUMERO_POBLACION)
    
    _data_fitness = []

    MAX = 20
    MIN = -20

    
    W = 0.95
    C1 = 1.4944
    C2 = 1.4944
    F5 = -1000
    F1 = -1400



    # Constructor
    def __init__(self, restriccion: str, function:str):
        # Inicializar restriccion
        self.restriccion = restriccion
        self.function = function
        # Inicializacion de los individuos
        self._generar_individuo()
        # Inicializacion de la poblacion
        self._generar_poblacion()
        # Inicializacion de la velocidad de la poblacion
        self._generar_velocidad()
        # Inicilizacion del fitness
        # ! Calculo de fitness por funcion numero 5
        if self.function == "power":
            self._function_power_different()
        # ! Calculo de fitness por funcion numero 1
        if self.function == "sphere":
            self._function_sphere_()
        # Inicilizacion del gBest
        self._calculo_gbest_()

        self.convergence = []
        
    #genera valores aleatorios
    def _generar_individuo(self):
        # Crear un arreglo
        _list = []
        # Solo dos valores
        for _ in range(self.NUMERO_DE_DIMENSIONES):
            # Generar valores aleatorios flotantes dentro del rango -20 a 20
            _list.append(random.uniform(self.MAX, self.MIN))
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
            
    def calcular_z(self, x):
        # Creo arreglo de z
        z = np.zeros((self.NUMERO_DE_DIMENSIONES))
        # Generar O
        o = self._generar_individuo()
        # Inicio iteración mediante la Dimensión
        for i in range(self.NUMERO_DE_DIMENSIONES):
            # Validación de los límites
            if self.restriccion == "ref" or self.restriccion == "bounce":
                # ! Restriccion reflex
                z[i] = self._restriccion_reflex_(x[i] - o[i])
            elif self.restriccion == "rand":
                # ! Restriccion random
                z[i] = self._restriccion_random_(x[i] - o[i])
                
        # Devuelvo arreglo z
        return z

    def _function_power_different(self):
        for i in range(self.NUMERO_POBLACION):
            # Se extrae el individuo
            _individuo = self._poblacion[i]
            # Variable sumadora
            suma = 0
            # Calcular Z
            z = self.calcular_z(_individuo)
            for j in range(self.NUMERO_DE_DIMENSIONES):
                _z = z[j]
                e = abs(_z) ** (2 + 4 * (j / (self.NUMERO_DE_DIMENSIONES - 1)))
                suma += e
            
            fitness = math.sqrt(suma) - self.F5
        
            self._fitness[i] = fitness 
        
            self._pbest_fitness[i] = fitness 
            
    def _function_sphere_(self):
        for i in range(self.NUMERO_POBLACION):
            _individuo = self._poblacion[i]
            z = self.calcular_z(_individuo)
            for j in range(self.NUMERO_DE_DIMENSIONES):
                _z = z[j]
                suma_cuadrados = np.sum(_z**2)
            
            self._fitness[i] = suma_cuadrados + self.F1
            
            self._pbest_fitness[i] = suma_cuadrados + self.F1
        
    

    # Actualizacion de velocidad            
    def _actualizar_velocidad(self):
        for i in range(self.NUMERO_POBLACION):
            for j in range(len(self._velocidad[i])):
                r1 = random.random()
                r2 = random.random()
                v2 = self.W * self._velocidad[i][j] + self.C1 * r1 * (self._pbest[i][j] - self._velocidad[i][j]) + self.C2 * r2 * (self._gbest_c[j] - self._velocidad[i][j])
                
                if self.restriccion == "ref":
                    # ! Restriccion reflex
                    self._velocidad[i][j] = self._restriccion_reflex_(v2)
                elif self.restriccion == "rand":
                    # ! Restriccion random
                    self._velocidad[i][j] = self._restriccion_random_(v2)
                elif self.restriccion == "bounce":
                    # ! Restriccion bouncy
                    self._velocidad[i][j] = self._restriccion_bouncy(v2)
                

    #Actualización de la población
    def _actualizar_poblacion(self):
        for i in range (self.NUMERO_POBLACION):
            for j in range(len(self._velocidad[i])):
                self._poblacion[i][j] = self._poblacion[i][j] + self._velocidad[i][j] 

                if self.restriccion == "ref":
                    # ! Restriccion reflex
                    self._poblacion[i][j] = self._restriccion_reflex_(self._poblacion[i][j]) 
                elif self.restriccion == "rand":
                    # ! Restriccion random
                    self._poblacion[i][j] = self._restriccion_random_(self._poblacion[i][j])
                elif self.restriccion == "bounce":
                    #! Restriccion bouncy
                    self._poblacion[i][j] = self._restriccion_bouncy(self._poblacion[i][j])
                    
    #Calcular el nuevo fitness
    def _actualizar_fitness(self):
        # ! Calculo de fitness por funcion numero 5
        if self.function == "power":
            self._function_power_different()
        # ! Calculo de fitness por funcion numero 1
        if self.function == "sphere":
            self._function_sphere_()
        
        for i in range (self.NUMERO_POBLACION):
                if (self._fitness[i] <= self._pbest_fitness[i]):
                    self._pbest_fitness[i] = self._fitness[i]
                    self._pbest[i] = self._poblacion[i]
                    
    def _actualizar_gbest(self):
        self._calculo_gbest_()

    def start(self):
        # print("Restriccion", self.restriccion)
        # print("Function", self.function)
        generacion = 0
        while generacion < self.NUMERO_GENERACION:
            # random.seed(generacion)
            self._actualizar_velocidad()

            self._actualizar_poblacion()

            self._actualizar_fitness()

            self._actualizar_gbest()

            generacion += 1

        # Después de completar una ejecución completa del algoritmo,
        # guardar los datos de fitness y luego restablecer todo para la próxima ejecución.
        print(len(self._data_fitness))
        self._data_fitness.append(self._gbest_f)
        print("Mejor Individuo", self._gbest_f)
        self.reset()  # Restablecer la población, velocidades, etc.
    
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

    def _restriccion_bouncy(self, eval):
        return np.clip(eval, self.MAX, self.MIN)
        
    #imprime el arreglo
    def __str__(self) -> str: 
        return f"""GBEST FITNESS \n {self._gbest_f}\n INDIVIDUO \n{self._gbest_c}"""


    # def plot_convergence(self):
    #     # Crear una lista de generaciones
    #     generaciones = np.arange(1, self.NUMERO_GENERACION + 1)

    #     # Crear el gráfico
    #     plt.plot(generaciones, self.convergence, marker='o', linestyle='-')
    #     plt.title('Convergencia de PSO')
    #     plt.xlabel('Generación')
    #     plt.ylabel('Mejor Fitness')
    #     plt.grid(True)
    #     plt.show()


    def reset(self):
        # Restablecer la población, velocidad, fitness, etc.
        self._poblacion = np.zeros((self.NUMERO_POBLACION, self.NUMERO_DE_DIMENSIONES)) 
        self._velocidad = np.zeros((self.NUMERO_POBLACION, self.NUMERO_DE_DIMENSIONES))
        self._fitness = np.zeros(self.NUMERO_POBLACION)
        self._pbest = np.zeros((self.NUMERO_POBLACION, self.NUMERO_DE_DIMENSIONES))
        self._pbest_fitness = np.zeros(self.NUMERO_POBLACION)
        self._gbest_c = np.zeros(self.NUMERO_DE_DIMENSIONES)
        self._gbest_f = 0        

        self._generar_poblacion()
        
        self._generar_velocidad()
        
        # ! Calculo de fitness por funcion numero 5
        if self.function == "power":
            self._function_power_different()
        # ! Calculo de fitness por funcion numero 1
        if self.function == "sphere":
            self._function_sphere_()
        
        self._calculo_gbest_()
        
        
if __name__ == "__main__":
    # Inicializamos las listas para almacenar los datos de fitness de cada experimento
    data_fitness_exp1 = []
    data_fitness_exp2 = []
    data_fitness_exp3 = []
    data_fitness_exp4 = []
    data_fitness_exp5 = []
    data_fitness_exp6 = []
    
    print("REF & POWER")
    for _ in range(25):
        exp1 = PSO(restriccion="ref", function="power")
        exp1.start()
        data_fitness_exp1.extend(exp1._data_fitness)  # Usamos extend en lugar de append
    
    print("RAND & POWER")
    for _ in range(25):
        exp2 = PSO(restriccion="rand", function="power")
        exp2.start()
        data_fitness_exp2.extend(exp2._data_fitness)  # Usamos extend en lugar de append
    
    print("BOUNCE & POWER")  
    for _ in range(25):
        exp3 = PSO(restriccion="bounce", function="power")
        exp3.start()
        data_fitness_exp3.extend(exp3._data_fitness)  # Usamos extend en lugar de append
    
    print("REF & SPHERE")
    for _ in range(25):
        exp4 = PSO(restriccion="ref", function="sphere")
        exp4.start()
        data_fitness_exp4.extend(exp4._data_fitness)  # Usamos extend en lugar de append
    
    print("RAND & SPHERE")
    for _ in range(25):
        exp5 = PSO(restriccion="rand", function="sphere")
        exp5.start()
        data_fitness_exp5.extend(exp5._data_fitness)  # Usamos extend en lugar de append
    
    print("BOUNCE & SPHERE")
    for _ in range(25):
        exp6 = PSO(restriccion="bounce", function="sphere")
        exp6.start()
        data_fitness_exp6.extend(exp6._data_fitness)  # Usamos extend en lugar de append


    
    # Crear 2 filas y 3 columnas de subplots
    fig, axes = plt.subplots(2, 3, figsize=(18, 12))
    
    axes[0, 0].boxplot(data_fitness_exp1, labels=['exp1'])
    axes[0, 0].set_title('Reflaction, Power')
    
    axes[0, 1].boxplot(data_fitness_exp2, labels=['exp2'])
    axes[0, 1].set_title('Random, Power')
    
    axes[0, 2].boxplot(data_fitness_exp3, labels=['exp3'])
    axes[0, 2].set_title('Bounce, Power')
    
    axes[1, 0].boxplot(data_fitness_exp4, labels=['exp4'])
    axes[1, 0].set_title('Reflaction, Sphere')
    
    axes[1, 1].boxplot(data_fitness_exp5, labels=['exp5'])
    axes[1, 1].set_title('Random, Sphere')
    
    axes[1, 2].boxplot(data_fitness_exp6, labels=['exp6'])
    axes[1, 2].set_title('Bounce, Sphere')

    plt.tight_layout()
    plt.show()
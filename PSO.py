import numpy as np
import random
import math
#             /$$$$$$                               
#            /$$__  $$                              
#   /$$$$$$ | $$  \__/  /$$$$$$   /$$$$$$  /$$$$$$$ 
#  /$$__  $$| $$$$     /$$__  $$ /$$__  $$| $$__  $$
# | $$$$$$$$| $$_/    | $$  \__/| $$$$$$$$| $$  \ $$
# | $$_____/| $$      | $$      | $$_____/| $$  | $$
# |  $$$$$$$| $$      | $$      |  $$$$$$$| $$  | $$
#  \_______/|__/      |__/       \_______/|__/  |__/
class PSO:
    NUMERO_POBLACION = 100
    NUMERO_GENERACION = 1000
    NUMERO_DE_DIMENSIONES = 20
    
    #numero de individios en la poblacion
    # 10 son las filas y 2 son las columnas
    _poblacion = np.zeros((NUMERO_POBLACION, NUMERO_DE_DIMENSIONES))
    _velocidad = np.zeros((NUMERO_POBLACION, NUMERO_DE_DIMENSIONES))
    _fitness   = np.zeros(NUMERO_POBLACION)

    _gbest_c = np.zeros(NUMERO_DE_DIMENSIONES)  #gbest cordenadas(posicion)
    _gbest_f = 0  #gbest fitness
    _gbest_v = 0

    _pbest = np.zeros((NUMERO_POBLACION, NUMERO_DE_DIMENSIONES))
    _pbest_fitness = np.zeros(NUMERO_POBLACION)
    
    _data_fitness = []
    _data_violacion = []
    
    _violaciones = 0
    _factibles = []
    _violaciones_individuo = []
    _ultimo_factible = False
    

    MAX = 10
    MIN = 0

    W = 0.95
    C1 = 1.4944
    C2 = 1.4944
    F5 = -1000
    F1 = -1400

    # Constructor
    def __init__(self, limite: str):
        # Inicializar restriccion
        self.limite = limite
        # self.function = function
        # Inicializacion de los individuos
        self._generar_individuo()
        # Inicializacion de la poblacion
        self._generar_poblacion()
        # Inicializacion de la velocidad de la poblacion
        self._generar_velocidad()
        # Inicilizacion del fitness
        self._function_objective()
        # ! Calculo de fitness por funcion numero 5
        # if self.function == "power":
        #     self._function_power_different()
        # ! Calculo de fitness por funcion numero 1
        # if self.function == "sphere":
        #     self._function_sphere_()

        
        # Inicilizacion del gBest
        self._calculo_gbest_()

    def __del__(self):
        print("Destruyendo PSO")
        self._data_fitness.clear()
     
    #* Genera valores aleatorios (NO MOVER)
    def _generar_individuo(self):
        # Crear un arreglo
        _list = []
        # Solo dos valores
        for _ in range(self.NUMERO_DE_DIMENSIONES):
            # Generar valores aleatorios flotantes dentro del rango -20 a 20
            _list.append(random.uniform(self.MAX, self.MIN))
        # Regresa el arreglo como objeto numpy
        return np.array(_list)
    
    #* Genera una poblacion y la almacena en una matriz (NO MOVER)
    def _generar_poblacion(self):
        # Generacion  de la poblacion
        for i in range(self.NUMERO_POBLACION):
            # Se obtiene el individuo
            _individuo = self._generar_individuo()
            # Se añade a la poblacion
            self._poblacion[i] = _individuo

        for i in range(self.NUMERO_POBLACION):
            self._pbest[i] = self._poblacion[i]
    
    #* Generar velocidades (NO MOVER)
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

    #* Actualizcion de pBest (NO MOVER)
    def _actualizar_pbest_(self): 
        for i in range(self.NUMERO_POBLACION):
            if self._fitness[i] < self._pbest_fitness[i]:
                self._pbest[i] = self._poblacion[i]
                self._pbest_fitness[i] = self._fitness[i]

    #* Calculo de gBest (NO MOVER)
    def _calculo_gbest_(self): 
        # Obtener el valor minimo
        index = np.argmin(self._pbest_fitness)
        index_violaciones = np.argmin(self._violaciones_individuo)
        self._gbest_f = self._pbest_fitness[index] 
        self._gbest_c = self._poblacion[index]
        self._gbest_v = self._violaciones_individuo[index_violaciones]

    #* Calculo de fitness (NO MOVER)
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
    
    #* Calculo de Z (NO MOVER)
    def calcular_z(self, x):
        # Creo arreglo de z
        z = np.zeros((self.NUMERO_DE_DIMENSIONES))
        # Generar O
        o = self._generar_individuo()
        # Inicio iteración mediante la Dimensión
        for i in range(self.NUMERO_DE_DIMENSIONES):
            # Validación de los límites
            if self.limite == "ref":
                # ! Limite reflex
                z[i] = self._limite_reflex_(x[i] - o[i])
            elif self.limite == "rand":
                # ! Limite random
                z[i] = self._limite_random_(x[i] - o[i])
            else:
                # ! Limite boundary
                z[i] = self._limite_boudary_(x[i] - o[i])
                
        # Devuelvo arreglo z
        return z

    #* Funcion Power Different (NO MOVER)
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
    
    #* Funcion Sphere (NO MOVER)
    def _function_sphere_(self):
        for i in range(self.NUMERO_POBLACION):
            _individuo = self._poblacion[i]
            z = self.calcular_z(_individuo)
            suma_cuadrados = np.sum(z**2)
            
            fitness = suma_cuadrados + self.F1
            
            
            self._fitness[i] = fitness
            
            self._pbest_fitness[i] = fitness
    
    #* Actualizacion de velocidad (NO MOVER)            
    def _actualizar_velocidad(self):
        for i in range(self.NUMERO_POBLACION):
            for j in range(len(self._velocidad[i])):
                r1 = random.random()
                r2 = random.random()
                v2 = self.W * self._velocidad[i][j] + self.C1 * r1 * (self._pbest[i][j] - self._velocidad[i][j]) + self.C2 * r2 * (self._gbest_c[j] - self._velocidad[i][j])
                
                if self.limite == "ref":
                    # ! Limite reflex
                    self._velocidad[i][j] = self._limite_reflex_(v2)
                elif self.limite == "rand":
                    # ! Limite random
                    self._velocidad[i][j] = self._limite_random_(v2)
                elif self.limite == "bounce":
                    # ! Limite bounary
                    self._velocidad[i][j] = self._limite_boudary_(v2)
    
    # * Actualizacion de gbest
    def _actualizar_gbest(self):
        self._calculo_gbest_()
                          
    #* Actualización de la población (NO MOVER)
    def _actualizar_poblacion(self):
        for i in range (self.NUMERO_POBLACION):
            for j in range(len(self._velocidad[i])):
                self._poblacion[i][j] = self._poblacion[i][j] + self._velocidad[i][j] 

                if self.limite == "ref":
                    # ! Limite reflex
                    self._poblacion[i][j] = self._limite_reflex_(self._poblacion[i][j]) 
                elif self.limite == "rand":
                    # ! Limite random
                    self._poblacion[i][j] = self._limite_random_(self._poblacion[i][j])
                elif self.limite == "bounce":
                    #! Limite bouncy
                    self._poblacion[i][j] = self._limite_boudary_(self._poblacion[i][j])
        
    
    #* Calcular el nuevo fitness
    # TODO: Sistema de evaluacion de factibilidad por reglas de DEB
    def _actualizar_fitness(self):
        # # ! Calculo de fitness por funcion numero 5
        # if self.function == "power":
        #     self._function_power_different()
        # # ! Calculo de fitness por funcion numero 1
        # if self.function == "sphere":
        #     self._function_sphere_()
        # ! Calculo de fitness por funcion objectiva
        self._function_objective()
            
        for i in range (self.NUMERO_POBLACION):            
            if (self._fitness[i] <= self._pbest_fitness[i]):
                self._pbest_fitness[i] = self._fitness[i]
                self._pbest[i] = self._poblacion[i]
        
    
    

    def start(self):
        
        generacion = 0
        while generacion < self.NUMERO_GENERACION:
            self._actualizar_velocidad()

            self._actualizar_poblacion()

            self._actualizar_fitness()

            self._actualizar_gbest()

            generacion += 1

        self._data_fitness.append(self._gbest_f)
        self._data_violacion.append(self._gbest_v)
        
    # ! Manejo de Limites
    
    def _limite_random_(self , eval):
        if eval > self.MAX or eval < self.MIN:
                    eval = self.MIN + random.uniform(0, 1) * (self.MAX - self.MIN)
        return eval
    
    def _limite_reflex_(self, eval, lower_limit=-20, upper_limit=20):
        if eval < lower_limit:
            eval = lower_limit + abs(eval - lower_limit)
        elif eval > upper_limit:
            eval = upper_limit - abs(eval - upper_limit)
        return eval

    def _limite_boudary_(self, eval):
        if self.MIN <= eval <= self.MAX:
            return eval
        elif self.MIN <= eval:
            return self.MIN
        else:
            return self.MAX
    
    # ! Manejo de Restricciones
    
    def _function_objective(self):
        for i in range(self.NUMERO_POBLACION):
            _individuo = self._poblacion[i]
            sum_cos4 = np.sum(np.cos(_individuo)**4)
            prod_cos2 = np.prod(np.cos(_individuo)**2)
            sum_ix2 = np.sum([(i + 1) * _individuo[i]**2 for i in range(len(_individuo))])
 
                      
            f_x = -abs((sum_cos4 - 2 * prod_cos2) / np.sqrt(sum_ix2))
            
            self.calcular_violaciones(_individuo)

            self._violaciones = 0

            self._fitness[i] = f_x
            
            self._pbest_fitness[i] = f_x


        
    def g1 (self, x):
        return 0.75 - np.prod(x) <= 0
    
    def g2(self , x):
        return np.sum(x) -7.5 * self.NUMERO_DE_DIMENSIONES <= 0

    def calcular_violaciones (self , x):
        if self.g1(x): 
            self._violaciones += 1
        if self.g2(x): 
            self._violaciones += 1
        self._violaciones_individuo.append(self._violaciones)

            

    # ! Reinicio
    def reset(self):
        
            
        self._poblacion = np.zeros((self.NUMERO_POBLACION, self.NUMERO_DE_DIMENSIONES))
        self._velocidad = np.zeros((self.NUMERO_POBLACION, self.NUMERO_DE_DIMENSIONES))
        self._fitness = np.zeros(self.NUMERO_POBLACION)
        self._pbest = np.zeros((self.NUMERO_POBLACION, self.NUMERO_DE_DIMENSIONES))
        self._pbest_fitness = np.zeros(self.NUMERO_POBLACION)
        self._gbest_c = np.zeros(self.NUMERO_DE_DIMENSIONES)
        self._gbest_f = 0
        self._generar_poblacion()
        self._generar_velocidad()
        self._calculo_gbest_()
        self._violaciones = 0
        self._factibles = []

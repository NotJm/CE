import numpy as np
from utils.individuo import generar, isValid
from utils.constantes import NUMERO_DE_POBLACIONES, GENERACIONES, SUPERIOR, INFERIOR, CR, F 
from utils.restricciones import suma_violaciones

class DE:
    
    mejor_individuo = []
    mejor_fitness = 0
    mejor_violacion = 0
    
    def __init__(
        self,
        limite,  # Funcion para controlar el espacio de busqueda
        evaluar,  # Funcion para evaluar la funcio objetivo
        restr_func, # Funcion para restringir la funcion objectiva
        g_funcs=[], # Funciones para las restricciones de desigualdad
        h_funcs=[], # Funciones para las restricciones de igualdad
        
    ):
        # Funcion para controlar el espacio de busqueda
        self.limite = limite
        # Funcion para evaluar la funcion objetivo
        self.evaluar = evaluar
        # Funcion para restricciones funcionales
        self.restr_func = restr_func
        # Funciones para las restricciones de desigualdad
        self.g_funcs = g_funcs
        # Funciones para las restricciones de igualdad
        self.h_funcs = h_funcs
        # Generar la poblacion en base a los limites SUPERIORES E INFERIORES
        self.poblacion = generar(INFERIOR, SUPERIOR)
        # Generar arreglo de NUMERO DE POBLACIONES
        self.fitness = np.zeros(NUMERO_DE_POBLACIONES)
        # Genera arreglo de NUMERO DE POBLACIONES
        self.noViolaciones = np.zeros(NUMERO_DE_POBLACIONES)
        # Calcula el fitness en base a la funcion objetivo
        self.calcularAptitud()

    def calcularAptitud(self):
        for index, individuo in enumerate(self.poblacion):
            fitness = self.evaluar(individuo)
            # Guardar fitness de la particula
            self.fitness[index] = fitness 
            # Obtener la suma de violaciones
            total_de_violaciones = suma_violaciones(
                self.g_funcs,
                self.h_funcs,
                individuo
            )
            # Guardar violacioens
            self.noViolaciones[index] = total_de_violaciones
            
    def actualizarPoblacion(self):
        for index in range(NUMERO_DE_POBLACIONES):
            self.poblacion[index] = self.limite(SUPERIOR, INFERIOR, self.poblacion[index])

    def funcionEvolutiva(self):
        for i in range(NUMERO_DE_POBLACIONES):
            
            # Selección de r1, r2, r3
            indices = [idx for idx in range(NUMERO_DE_POBLACIONES) if idx != i]
            r1, r2, r3 = np.random.choice(indices, 3, replace=False)
            
            # Inicialización de mutado y selección aleatoria jrand
            jrand = np.random.randint(0, NUMERO_DE_POBLACIONES)
            mutado = np.zeros(len(self.poblacion[i]))
            
            # Proceso de mutación y cruce
            for j in range(len(self.poblacion[i])):
                if np.random.rand() < CR or j == jrand:
                    mutado[j] = self.poblacion[r1][j] + F * (self.poblacion[r2][j] - self.poblacion[r3][j])
                else:
                    mutado[j] = self.poblacion[i][j]
            # Aplicar límites y evaluar mutado
            mutado_corregido = self.limite(SUPERIOR, INFERIOR, mutado)
            fitness_mutado = self.evaluar(mutado_corregido)
            fitness_ind_actual = self.fitness[i]
            
            # Reemplazo basado en la aptitud
            if fitness_mutado <= fitness_ind_actual:
                self.poblacion[i] = mutado_corregido
                self.fitness[i] = fitness_mutado
        self.actualizarPoblacion()
        self.aplicarDeb()

    def aplicarDeb(self):
        posicion = self.restr_func(self.poblacion, self.fitness, self.noViolaciones)
        self.mejor_individuo = self.poblacion[posicion]
        self.mejor_fitness = self.fitness[posicion]
        self.mejor_violacion = self.noViolaciones[posicion]

    def report(self):
        print("Evo Dif")
        print("Mejor Individuo:", self.mejor_individuo)
        print("Mejor Aptitud (Fitness):", self.mejor_fitness)
        print(
            "No Violaciones:",
            "Sin Violaciones" if self.mejor_violacion == 0 else self.mejor_violacion,
        )
        print("\n")

    def start(self):
        for generacion in range(1, GENERACIONES + 1):
            self.calcularAptitud()
            self.funcionEvolutiva()

    def reset(self):
        self.poblacion = generar(SUPERIOR, INFERIOR)
        self.calcularAptitud()
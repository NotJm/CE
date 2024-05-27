import numpy as np
import random as rd
from utils.constantes import NUMERO_DE_POBLACIONES, GENERACIONES
from utils.restricciones import suma_violaciones, aEsMejorQueB_deb
from utils.Algorithm import Algorithm

class DE(Algorithm):
    F = 0.5  # Factor de mutación
    CR = 0.9  # Tasa de recombinación

    def __init__(
        self,
        limite, # Función para limitar la partícula
        evaluar, # Función para evaluar la partícula
        superior,
        inferior,
        restr_func, # Función para restringir la función objetivo
        g_funcs=[], # Lista de funciones de desigualdad <= 0
        h_funcs=[] # Lista de funciones de igualdad == 0
    ):
        """
        Inicializa el algoritmo de Evolución Diferencial.
        
        Args:
            limite (función): Función para limitar los valores de las partículas.
            evaluar (función): Función para evaluar las partículas.
            restr_func (función): Función para aplicar restricciones a las partículas.
            g_funcs (lista): Lista de funciones de restricciones de desigualdad.
            h_funcs (lista): Lista de funciones de restricciones de igualdad.
        """
        self.limite = limite
        self.evaluar = evaluar
        self.restr_func = restr_func
        self.superior = superior
        self.inferior = inferior
        self.g_funcs = g_funcs
        self.h_funcs = h_funcs

        # Inicialización de la población
        self.poblacion = self.generar(self.inferior, self.superior)
        self.fitness = np.zeros(NUMERO_DE_POBLACIONES)
        self.noViolaciones = np.zeros(NUMERO_DE_POBLACIONES)

        # Variables para almacenar la mejor solución encontrada
        self.gbestIndividuo = []
        self.gbestAptitud = float('inf')
        self.gbestViolacion = float('inf')

        # Cálculo inicial de aptitudes y mejor solución
        self.calcularAptitud()
        self.calcularGbest()

    def calcularAptitud(self):
        """
        Calcula la aptitud y el número de violaciones de restricciones para cada individuo en la población.
        """
        for index, individuo in enumerate(self.poblacion):
            fitness = self.evaluar(individuo)
            self.fitness[index] = fitness
            total_de_violaciones = suma_violaciones(self.g_funcs, self.h_funcs, individuo)
            self.noViolaciones[index] = total_de_violaciones

    def calcularGbest(self):
        """
        Calcula el mejor individuo de la población según las restricciones.
        """
        posicion = self.restr_func(self.poblacion, self.fitness, self.noViolaciones)
        self.gbestIndividuo = self.poblacion[posicion]
        self.gbestAptitud = self.fitness[posicion]
        self.gbestViolacion = self.noViolaciones[posicion]

    def mutacion(self, indice):
        """
        Genera un vector mutante para el individuo dado.

        Args:
            indice (int): Índice del individuo actual.

        Returns:
            np.array: Vector mutante.
        """
        indices = list(range(NUMERO_DE_POBLACIONES))
        indices.remove(indice)
        a, b, c = rd.sample(indices, 3)
        mutante = self.poblacion[a] + self.F * (self.poblacion[b] - self.poblacion[c])
        return np.clip(mutante, self.inferior, self.superior)

    def cruze(self, mutante, indice):
        """
        Realiza la recombinación entre el vector mutante y el individuo actual.

        Args:
            mutante (np.array): Vector mutante.
            indice (int): Índice del individuo actual.

        Returns:
            np.array: Nuevo individuo (hijo).
        """
        hijo = np.copy(self.poblacion[indice])
        for i in range(len(mutante)):
            if rd.random() < self.CR:
                hijo[i] = mutante[i]
        return hijo

    def seleccion(self, hijo, indice):
        """
        Realiza la selección entre el hijo y el individuo actual.

        Args:
            hijo (np.array): Nuevo individuo (hijo).
            indice (int): Índice del individuo actual.
        """
        fitness_hijo = self.evaluar(hijo)
        violaciones_hijo = suma_violaciones(self.g_funcs, self.h_funcs, hijo)
        if aEsMejorQueB_deb(self.fitness[indice], self.noViolaciones[indice], fitness_hijo, violaciones_hijo) == False:
            self.poblacion[indice] = hijo
            self.fitness[indice] = fitness_hijo
            self.noViolaciones[indice] = violaciones_hijo

    def start(self):
        """
        Ejecuta el proceso de Evolución Diferencial.
        """
        for generacion in range(GENERACIONES):
            for i in range(NUMERO_DE_POBLACIONES):
                mutante = self.mutacion(i)
                hijo = self.cruze(mutante, i)
                self.seleccion(hijo, i)
            self.calcularGbest()

    def report(self):
        """
        Imprime el reporte final con la mejor solución encontrada.
        """
        print("DE Reporte")
        print("Solución Óptima")
        print("Individuo:", self.gbestIndividuo)
        print("Aptitud (Fitness):", self.gbestAptitud)
        print("Num Violaciones:", self.gbestViolacion)

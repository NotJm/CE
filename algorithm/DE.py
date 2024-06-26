from utils.constantes import SIZE_POBLATION, GENERATIONS
from core.restricciones import Restricciones
from core.algoritmo import Algoritmo
from tqdm import tqdm
import numpy as np


class DE(Algoritmo):
    # Poblacion
    poblacion = []
    # Fitness de los individuos de la poblacion
    fitness = np.zeros(SIZE_POBLATION)
    # Numero de infracciones que ocasiono un individuo de la poblacion
    noViolaciones = np.zeros(SIZE_POBLATION)

    # Factor de mutacion
    F = 0.7
    # Tasa de recombinacion
    CR = 0.9

    def __init__(
        self,
        limite,  # Funcion para limitar la poblacion
        evaluar,  # Funcion para evaluar la poblacion
        superior,  # Limite Superior de la poblacion
        inferior,  # Limite inferior de la poblacion
        restriccion_de_funcion,  # Funcion para restringir la funcion objectiva
        g_funcs=[],  # Lista de funciones de desigualdad
        h_funcs=[],  # Lista de funciones de igualdad
    ):
        # Funcion limite a ocupar
        self.limite = limite
        # Funcion objetiva para obtener el fitness
        self.evaluar = evaluar
        # Limites superiores e inferiores
        self.superior = superior
        self.inferior = inferior
        # Funcion para restricciones funcionales
        self.restriccion_de_funcion = restriccion_de_funcion
        # Lista de restricciones de desigualdad
        self.g_funcs = g_funcs
        # Lista de restricciones de igualdad
        self.h_funcs = h_funcs

        # Creacion aleatoria de la poblacion
        self.poblacion = self.generar(self.superior, self.inferior)

        # Calculo de fitness y suma de violaciones
        self.calcularFitnessYSumaDeViolaciones()

        self.obtenerGbestPoblacion0()
        

    # Calculo del fitness para cada individuo de la poblacion
    # y calcular la suma de violaciones que tuvo el individuo
    def calcularFitnessYSumaDeViolaciones(self):
        # Calculo del fitness para cada particula
        for index, individuo in enumerate(self.poblacion):
            # Obtener el fitness
            fitness = self.evaluar(individuo)
            # Guardar fitness de la poblacion
            self.fitness[index] = fitness
            # Obtener la suma de violaciones

            total_de_violaciones = Restricciones.suma_violaciones(
                self.g_funcs, self.h_funcs, individuo
            )
            self.noViolaciones[index] = total_de_violaciones

    # Operador de mutacion
    def mutacionDeIndividuo(self, idx):
        # Crear una lista de índices excluyendo a idx
        indices = np.arange(len(self.poblacion))
        indices = np.delete(indices, idx)

        # Selecciona tres índices al azar
        r1, r2, r3 = np.random.choice(indices, 3, replace=False)

        # Selecciona los individuos correspondientes
        X_r1 = self.poblacion[r1]
        X_r2 = self.poblacion[r2]
        X_r3 = self.poblacion[r3]

        # Genera el individuo mutado siguiendo la ecuación correcta
        mutado = X_r1 + self.F * (X_r2 - X_r3)

        # Regresar individuo mutado
        return mutado

    # Operador de cruzar
    def cruzeDeIndividuos(self, target, mutante):
        D = len(target)
        trial = np.copy(target)
        j_rand = np.random.randint(D)

        for j in range(D):
            if np.random.rand() < self.CR or j == j_rand:
                trial[j] = mutante[j]

        return trial

    # Operador de seleccion
    def seleccionDeIndividuos(self, idx, trial):
        trial_fitness = self.evaluar(trial)
        trial_violaciones = Restricciones.suma_violaciones(
            self.g_funcs, self.h_funcs, trial
        )

        current_fitness = self.fitness[idx]
        current_violaciones = self.noViolaciones[idx]

        # Verificar si el individuo de prueba es mejor que el actual
        if not self.restriccion_de_funcion(
            current_fitness, current_violaciones, trial_fitness, trial_violaciones
        ):
            self.fitness[idx] = trial_fitness
            self.noViolaciones[idx] = trial_violaciones
            self.poblacion[idx] = trial
    
    def obtenerGbestPoblacion0(self):
        # Mejor posicion en la generacion 0
        self.posicionInicial = 0

        # Mejor aptitud de la partícula
        self.gbestFitness = self.fitness[0]
        # Mejor violación de la partícula <= 0
        self.gbestViolacion = self.noViolaciones[0]
        # Mejor partícula de la generación
        self.gbestIndividuo = self.poblacion[0]
        
        self.actualizarPosicionGbestDePoblacion()
                        
    def actualizarPosicionGbestDePoblacion(self):
        for x in range(SIZE_POBLATION):

            current_fitness = self.fitness[x]
            current_violacion = self.noViolaciones[x]

            if not self.restriccion_de_funcion(
                self.gbestFitness,
                self.gbestViolacion,
                current_fitness,
                current_violacion,
            ):
                self.gbestFitness = current_fitness
                self.gbestViolacion = current_violacion
                self.gbestParticula = self.poblacion[x]

    def reporte(self):
        print("================================")
        print("Solución Óptima")
        print("Individuo:", self.gbestIndividuo)
        print("Aptitud (Fitness):", self.gbestFitness)
        print("Num Violaciones:", self.gbestViolacion)
        print("================================")

    # Funcion principal para ejecutar el algoritmo
    def run(self):
        for _ in tqdm(range(GENERATIONS), desc="Evolucionando"):
            for i in range(SIZE_POBLATION):
                objetivo = self.poblacion[i]
                mutante = self.mutacionDeIndividuo(i)
                prueba = self.cruzeDeIndividuos(objetivo, mutante)
                prueba = self.limite(self.superior, self.inferior, prueba)
                self.seleccionDeIndividuos(i, prueba)
                
            self.actualizarPosicionGbestDePoblacion()

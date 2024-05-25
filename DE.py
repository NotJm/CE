import numpy as np
from utils.individuo import generar, isValid, NP, GENERACIONES
from utils.limites import boundary, reflex, random
from utils.restricciones import g01, g02, evaluar

class DE:
    
    def __init__(self, limite, evaluar, g_funcs=[], h_funcs=[], CR=0.9, F=0.5):
        self.limite = limite
        self.evaluar = evaluar
        self.g_funcs = g_funcs
        self.h_funcs = h_funcs
        self.CR = CR
        self.F = F
        self.poblacion = generar(self.inferior, self.superior)
        self.fitness = np.zeros(NP)
        self.noViolaciones = np.zeros(NP)
        self.calcularAptitud()
    
    def calcularAptitud(self):
        for x in range(NP):
            evaluacion = self.evaluar(self.poblacion[x])
            self.fitness[x] = evaluacion["fitness"]
            self.noViolaciones[x] = evaluacion["noViolaciones"]
    
    def mutacion(self, indice):
        r1, r2, r3 = np.random.choice(NP, 3, replace=False)
        while indice in [r1, r2, r3]:
            r1, r2, r3 = np.random.choice(NP, 3, replace=False)
        mutado = np.copy(self.poblacion[indice])
        jrand = np.random.randint(0, len(mutado))
        for j in range(len(mutado)):
            if np.random.rand() < self.CR or j == jrand:
                mutado[j] = self.poblacion[r1][j] + self.F * (self.poblacion[r2][j] - self.poblacion[r3][j])
        return mutado

    def cruz(self, vector_objetivo, vector_mutante):
        hijo = np.copy(vector_objetivo)
        jrand = np.random.randint(0, len(vector_objetivo))
        for j in range(len(vector_objetivo)):
            if np.random.rand() < self.CR or j == jrand:
                hijo[j] = vector_mutante[j]
        return hijo

    def seleccion(self):
        nueva_poblacion = []
        for i in range(NP):
            vector_mutante = self.mutacion(i)
            vector_hijo = self.cruz(self.poblacion[i], vector_mutante)
            evaluacion_hijo = self.evaluar(vector_hijo)
            if evaluacion_hijo["fitness"] < self.fitness[i]:
                nueva_poblacion.append(vector_hijo)
                self.fitness[i] = evaluacion_hijo["fitness"]
                self.noViolaciones[i] = evaluacion_hijo["noViolaciones"]
            else:
                nueva_poblacion.append(self.poblacion[i])
        self.poblacion = np.array(nueva_poblacion)
    
    def actualizarPoblacion(self):
        self.seleccion()
        for i in range(NP):
            if self.limite == "reflex":
                self.poblacion[i] = reflex(self.superior, self.inferior, self.poblacion[i])
            elif self.limite == "random":
                self.poblacion[i] = random(self.superior, self.inferior, self.poblacion[i])
            elif self.limite == "boundary":
                self.poblacion[i] = boundary(self.superior, self.inferior, self.poblacion[i])

    def report(self, generacion:int = 0):
        print(f"DE Reporte - Generación {generacion}")
        mejor_indice = np.argmin(self.fitness)
        mejor_individuo = self.poblacion[mejor_indice]
        mejor_fitness = self.fitness[mejor_indice]
        mejor_violacion = self.noViolaciones[mejor_indice]
        print("Mejor Individuo:", mejor_individuo)
        print("Mejor Aptitud (Fitness):", mejor_fitness)
        print("No Violaciones:", "Sin Violaciones" if mejor_violacion == 0 else mejor_violacion)
        print("Valido:", isValid(self.superior, self.inferior, mejor_individuo))
        print("\n")
        
    def start(self):
        for generacion in range(1, GENERACIONES + 1):
            self.actualizarPoblacion()
            self.calcularAptitud()
            self.report(generacion)

    def reset(self):
        self.poblacion = generar(self.inferior, self.superior)
        self.calcularAptitud()

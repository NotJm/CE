# DE.py
import numpy as np
from scipy.optimize import differential_evolution
from Restricciones import Restricciones

class DifferentialEvolutionOptimizer:
    def __init__(self, problem, size_population, generations, limit_correction):
        self.problem = problem
        self.size_population = size_population
        self.generations = generations
        self.limit_correction = limit_correction
        self.superior = np.array(problem.SUPERIOR)
        self.inferior = np.array(problem.INFERIOR)
    
    def objetivo(self, x):
        x_corregido = self.limit_correction(self.superior, self.inferior, x)
        fitness = self.problem.fitness(x_corregido)
        violaciones = Restricciones.suma_violaciones(self.problem.rest_g, [], x_corregido)
        return fitness, violaciones
    
    def deb_selection(self, population):
        fitness = np.array([self.problem.fitness(ind) for ind in population])
        violaciones = np.array([Restricciones.suma_violaciones(self.problem.rest_g, [], ind) for ind in population])
        
        best_idx = 0
        for i in range(1, len(population)):
            if Restricciones.aEsMejorQueB_deb(fitness[i], violaciones[i], fitness[best_idx], violaciones[best_idx]):
                best_idx = i
                
        return best_idx, fitness, violaciones

    def optimize(self):
        bounds = list(zip(self.inferior, self.superior))

        def deb_objetivo(x):
            fitness, violaciones = self.objetivo(x)
            return fitness + violaciones  # Usamos una combinación para scipy.optimize

        result = differential_evolution(
            deb_objetivo,
            bounds=bounds,
            strategy='best1bin',
            maxiter=self.generations,
            popsize=self.size_population // len(bounds),
            tol=0.01,
            mutation=(0.5, 1),
            recombination=0.9,
            polish=True,
            disp=True,
            updating='deferred'  # Permite la corrección de límites
        )

        result.x = self.limit_correction(self.superior, self.inferior, result.x)

        # Selección DEB para obtener el mejor individuo final
        best_idx, fitness_final, violaciones_final = self.deb_selection(result.population)
        best_individual = result.population[best_idx]
        best_fitness = fitness_final[best_idx]
        best_violaciones = violaciones_final[best_idx]

        reporte(result.population, fitness_final, violaciones_final)

        return best_individual, best_fitness, best_violaciones

def reporte(poblacion, fitness, noViolaciones):
    poblacion = np.array(poblacion)
    fitness = np.array(fitness)
    noViolaciones = np.array(noViolaciones)

    best_idx = np.argmin(fitness)
    
    print("================================")
    print("Solución Óptima")
    print("Individuo:", poblacion[best_idx])
    print("Aptitud (Fitness):", fitness[best_idx])
    print("Num Violaciones:", noViolaciones[best_idx])
    print("================================")
    
    print("================================")
    print("Detalles de Todos los Individuos")
    for idx, (ind, fit, viol) in enumerate(zip(poblacion, fitness, noViolaciones)):
        print(f"Individuo {idx+1}:")
        print("  Valores:", ind)
        print("  Aptitud (Fitness):", fit)
        print("  Num Violaciones:", viol)
    print("================================")

def Ev_Diferencial_Con_SciPy(problem, size_population, generations, limit_correction):
    optimizer = DifferentialEvolutionOptimizer(problem, size_population, generations, limit_correction)
    best_individual, best_fitness, best_violaciones = optimizer.optimize()
    return best_individual, best_fitness, best_violaciones

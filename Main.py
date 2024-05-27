from algorithm.PSO import PSO

from progress.bar import Bar

from core.Limites import Limite
from core.Restricciones import Restricciones

from utils.correcion_de_velocidad import dba
from utils.cec2006problems import CEC2006_G02


ITERATIONS = 25
individuo = []
aptitud = []
violaciones = []

problema = CEC2006_G02()


def run():
    
    with Bar("Procesando", max=ITERATIONS) as bar:

        for _ in range(ITERATIONS):
            pso = PSO(
                Limite.reflex,  # Restriccion de limites
                problema.fitness,  # Problema a evaluar
                problema.SUPERIOR, # Límites superiores del individuo
                problema.INFERIOR, # Límites inferiores del individuo
                Restricciones.aEsMejorQueB_deb,  # Restriccion de problema
                dba,  # Una estrategia de actualizacion de velocidad,
                problema.rest_g, # Son restricciones de desigualdad para el problema,
                problema.rest_h, # Son restricciones de igualdad para el problema,
            )
            
            pso.optimizar()
            individuo.append(pso.gbestParticula)
            aptitud.append(pso.gbestAptitud)
            violaciones.append(pso.gbestViolacion)
            bar.next()

    print("Reporte general")
    for i, ind, apt, vio in zip(ITERATIONS ,individuo, aptitud, violaciones):
        print(f"Individuo de la ejecucion {i}:", ind)
        print("Aptitud (Fitness):", apt)
        print("Violaciones:", vio)


def main():
    run()


if __name__ == "__main__":
    main()

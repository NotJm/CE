from algorithm.PSO import PSO   
from algorithm.DE import DE
from progress.bar import Bar
from core.Limites import Limite
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
            de = DE(
                Limite.reflex,
                problema.fitness,
                problema.SUPERIOR,
                problema.INFERIOR,
                deb,
                problema.rest_g,
                problema.rest_h
            )
            
            de.start()
            individuo.append(de.gbestIndividuo)
            aptitud.append(de.gbestAptitud)
            violaciones.append(de.gbestViolacion)   
            
            # pso = PSO(
            #     Limite.reflex,  # Restriccion de limites
            #     problema.fitness,  # Problema a evaluar
            #     problema.SUPERIOR, # Límites superiores del individuo
            #     problema.INFERIOR, # Límites inferiores del individuo
            #     deb,  # Restriccion de problema
            #     dba,  # Una estrategia de actualizacion de velocidad,
            #     problema.rest_g, # Son restricciones de desigualdad para el problema,
            #     problema.rest_h, # Son restricciones de igualdad para el problema,
            # )
            
            # pso.start()
            # individuo.append(pso.gbestParticula)
            # aptitud.append(pso.gbestAptitud)
            # violaciones.append(pso.gbestViolacion)
            bar.next()

    print("Reporte general")
    for ind, apt, vio in zip(individuo, aptitud, violaciones):
        print("Individuo:", ind)
        print("Aptitud (Fitness):", apt)
        print("Violaciones:", vio)


def main():
    run()


if __name__ == "__main__":
    main()

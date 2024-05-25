from PSO import PSO
from progress.bar import Bar
from utils.limites import boundary, reflex, random
from utils.velocidad import dba
from utils.cec2006problems import CEC2006_g02, CEC2006_G01, CEC2006_G03
from utils.restricciones import deb

ITERATIONS = 25
individuo = []
aptitud = []
violaciones = []


def run():

    with Bar("Procesando", max=ITERATIONS) as bar:

        for _ in range(ITERATIONS):
            pso = PSO(
                reflex,  # Restriccion de limites
                CEC2006_g02.CEC2006_g02_aptitud,  # Problema a evaluar
                deb,  # Restriccion de problema
                dba,  # Una estrategia de actualizacion de velocidad
                [CEC2006_g02.CEC2006_g02_g1, CEC2006_g02.CEC2006_g02_g2] # Son restricciones para el problema,
            )

            pso.start()
            individuo.append(pso.gbestIndviduo)
            aptitud.append(pso.gbestAptitud)
            violaciones.append(pso.gbestViolacion)
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

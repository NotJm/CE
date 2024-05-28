# Algoritmos evolutivos
from algorithm.PSO import PSO
from algorithm.DEv2 import DE
# Limites y restricciones
from core.Limites import Limite
from core.Restricciones import Restricciones

# Estrategias de velocidad
from utils.correcion_de_velocidad import dba

# Funciones objetivas
from problems.cec2006problems import CEC2006_G01, CEC2006_G02, CEC2006_G03


ITERATIONS = 25
individuo = []
aptitud = []
violaciones = []

problema = CEC2006_G02()


def main():
    for i in range(1, ITERATIONS + 1):
        print(f"Ejecucion: {i}")
        de = DE(
            Limite.reflex,
            problema.fitness,
            problema.SUPERIOR,
            problema.INFERIOR,
            Restricciones.aEsMejorQueB_deb,
            problema.rest_g,
            problema.rest_h
        )
        de.run()   


if __name__ == "__main__":
    main()

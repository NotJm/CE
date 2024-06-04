# Algoritmos evolutivos
from algorithm.PSO import PSO
from algorithm.DE import DE
# Limites y restricciones
from core.limites import Limite
from core.restricciones import Restricciones

# Estrategias de velocidad
from utils.correcion_de_velocidad import dba
from utils.constantes import ITERATIONS

#Generar reporte CSV 
from utils.csv import mejor_solucion_csv

# Funciones objetivas
from problems.cec2006problems import (
    CEC2006_G01,
    CEC2006_G02,
    CEC2006_G03,
    CEC2006_G04,
    CEC2006_G05,
    
)

from problems.cec2020problems import CEC2020_RC01, CEC2020_RC02

from problems.cec2022problems import CEC2022_ZakharovF, CEC2022_RosenbrockF, SUPERIOR, INFERIOR



problema = CEC2006_G01()


def main():
    for i in range(1, ITERATIONS + 1):
        print(f"Ejecucion: {i}")
        pso = PSO(
            Limite.attract,  # Restriccion de limites
            problema.fitness,  # Problema a evaluar
            problema.SUPERIOR,  # Límites superiores del individuo
            problema.INFERIOR,  # Límites inferiores del individuo
            Restricciones.aEsMejorQueB_deb,  # Restriccion de problema
            dba,  # Una estrategia de actualizacion de velocidad,
            problema.rest_g,  # Son restricciones de desigualdad para el problema,
            problema.rest_h,  # Son restricciones de igualdad para el problema,
        )
        # Optimizacion
        pso.optimizar()
        pso.reporte()
        # de = DE (
        #     Limite.reflex,
        #     problema.fitness,
        #     problema.SUPERIOR,
        #     problema.INFERIOR,
        #     Restricciones.aEsMejorQueB_deb,
        #     problema.rest_g,
        #     problema.rest_h,
        # )
        # de.run()
        # de.reporte()

if __name__ == "__main__":
    main()

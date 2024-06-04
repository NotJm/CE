from utils.constantes import SIZE_POBLATION, GENERATIONS
from core.restricciones import Restricciones
from core.algoritmo import Algoritmo
from core.limites import Limite
from utils.logging import configuracionDeLoggin
from tqdm import tqdm
import numpy as np
import random as rd

class PSO(Algoritmo):
    # Particulas
    particulas = []
    # Velocidad de las particulas
    velocidad = []
    # Valor de aptitud de cada particula
    fitness = np.zeros(SIZE_POBLATION)
    # Valor de numero de violaciones por particula
    noViolaciones = np.zeros(SIZE_POBLATION)

    # Memoria de la mejor posicion de la particula
    pbest = []
    # Memoria del valor de la mejor aptitud de una particula de sus poblacion
    pbestFitness = []
    # Memoria del mejor numero de violaciones que tuvo la particula
    pbestViolaciones = []

    # Mejor aptitud de la particula
    gbestAptitud = 0
    # Mejor violacion de la particula <= 0
    gbestViolacion = 0
    # Mejor particula de la generacion
    gbestParticula = []
    # Mejor velocidad de la particula
    gbestVelocidad = []    

    def __init__(
        self,
        limite,  # Funcion para limitar la particula
        evaluar,  # Funcion para evaluar la particula
        superior,  # Limite Superior de la particulas
        inferior,  # Limite Inferior de la particulas
        restriccion_de_funcion,  # Funcion para restringir la funcion objectiva
        correcion_de_velocidad,  # Funcion de Estrategia de actualizacion de velocidad
        g_funcs=[],  # Lista de funciones de desigualdad <= 0
        h_funcs=[],  # Lista de funciones de igualdad == 0
        W = 0.729,
        C1 = 1.49445,
        C2 = 1.49445
    ):
        # Configuracion de loggin 
        self.logging = configuracionDeLoggin("pso_reporte.log")
        
        # Configuracion de PSO
        
        self.W = W # Factor de inercia
    
        self.C1 = C1  #Coeficiente aceleracion cognitiva
    
        self.C2 = C2 # Coeficiente aceleracion social
                
        # Funcion limite a ocupar
        self.limite = limite
        # Funcion aptitud que se va evaluar
        self.evaluar = evaluar
        # Limites superiores e inferiores
        self.superior = superior
        self.inferior = inferior
        # Funcion para restricciones funcionales
        self.restriccion_de_funcion = restriccion_de_funcion
        # Lista de funciones de restricciones de desigualdad
        self.g_funcs = g_funcs
        # Lista de funciones de restricciones de igualdad
        self.h_funcs = h_funcs
        # Estrategia para actualizar la velocidad
        self.act_vel = correcion_de_velocidad
        # Solo para la generacion para 0
        # Inicializacion de particulas (poblacion) con vectores de posicion y velocidad
        self.particulas = self.generar(self.inferior, self.superior)
        self.velocidad = self.generar(self.inferior, self.superior)
        # Calculo de la aptitud (fitness) para cada particula (individuo)
        self.calcularFitnessYSumaDeViolaciones()
        # El primer pbest es inicial
        self.pbest = np.copy(self.particulas)
        # El primer pbesfitness es inicial
        self.pbestFitness = np.copy(self.fitness)
        # Memoria de violaciones que tuvo la particuka
        self.pbestViolaciones = np.copy(self.noViolaciones)
        # Obtener el mejor de la generacion 0
        self.obtenerGbestPoblacion0()
        
     
        

    # Calculo de la aptitud (fitness) para cada particula (individuo)
    # Y Calcular la suma de violaciones que tuvo la particula
    def calcularFitnessYSumaDeViolaciones(self):
        
        # Calculo del fitness para cada particula
        for index, particula in enumerate(self.particulas):
            # Obtener el fitness
            fitness = self.evaluar(particula)
            # Guardar fitness de la particula
            self.fitness[index] = fitness
            # Obtener la suma de violaciones
            total_de_violaciones = Restricciones.suma_violaciones(
                self.g_funcs, self.h_funcs, particula
            )
            
            # Guardar violacioens
            self.noViolaciones[index] = total_de_violaciones

    # Metodo para actualizar la mejor poscion que obtuvo de las particulas
    def actualizarPbest(self):
        for index in range(SIZE_POBLATION):
            # Si el número de violaciones coincide con el anterior
            if not self.restriccion_de_funcion(
                self.pbestFitness[index],
                self.pbestViolaciones[index],
                self.fitness[index],
                self.noViolaciones[index],
            ):
                # Actualizacion de pbest
                self.pbest[index] = np.copy(self.particulas[index])
                self.pbestFitness[index] = self.fitness[index]
                self.pbestViolaciones[index] = self.noViolaciones[index]

    def actualizarVelocidad(self):
        for index in range(SIZE_POBLATION):
            for jndex in range(len(self.velocidad[index])):
                r1 = rd.uniform(0, 1)
                r2 = rd.uniform(0, 1)
                actVelocidad = (
                    self.W * self.velocidad[index][jndex]
                    + self.C1
                    * r1
                    * (self.pbest[index][jndex] - self.velocidad[index][jndex])
                    + self.C2
                    * r2
                    * (self.gbestParticula[jndex] - self.velocidad[index][jndex])
                )
                self.velocidad[index][jndex] = actVelocidad

    def obtenerGbestPoblacion0(self):
        posInicialGbest = 0
        self.gbestParticula = self.particulas[posInicialGbest]
        self.gbestAptitud = self.fitness[posInicialGbest]
        self.gbestViolacion = self.noViolaciones[posInicialGbest]
        self.actualizarPosicionGbestDePoblacion()

    def actualizarPosicionGbestDePoblacion(self):
        for x in range(SIZE_POBLATION):

            current_fitness = self.fitness[x]
            current_violacion = self.noViolaciones[x]

            if not self.restriccion_de_funcion(
                self.gbestAptitud,
                self.gbestViolacion,
                current_fitness,
                current_violacion,
            ):
                self.gbestAptitud = current_fitness
                self.gbestViolacion = current_violacion
                self.gbestParticula = self.particulas[x]

    def actualizarPosicion(self):
        for index in range(SIZE_POBLATION):
            for jndex in range(len(self.velocidad[index])):
                self.particulas[index][jndex] = (
                    self.particulas[index][jndex] + self.velocidad[index][jndex]
                )

    def restriccionLimites(self):
        for index in range(SIZE_POBLATION):
            if not self.isValid(self.superior, self.inferior, self.particulas[index]):
                # self.particulas[index] = self.limite(
                #     self.superior, self.inferior, self.particulas[index]
                # )
                self.particulas[index] = Limite.restriccion_ajuste_aptitud(
                    self.superior, self.inferior, self.particulas[index], self.evaluar
                )
                self.velocidad[index] = self.act_vel(self.velocidad[index])

    def reporte(self):
        # * Mensaje de Log para el reporte
        self.logging.debug("SOLUCION OPTIMA:")
        self.logging.debug(f"Mejor posicion de la particula:{self.gbestParticula}")
        self.logging.debug(f"Mejor fitness de la particula:{self.gbestAptitud}")
        self.logging.debug(f"Numero de Infracciones: {self.gbestViolacion}")
        
        print("================================")
        print("Reporte PSO")
        print("SOLUCION OPTIMA")
        print(f"Mejor posicion de la particula: {self.gbestParticula}")
        print(f"Mejor fitness de la particula: {self.gbestAptitud}")
        print(f"Minimo numero de infracciones: {self.gbestViolacion}")
        print("================================")

    def optimizar(self):
        generacion = 1
        with tqdm(
            total=GENERATIONS,
            desc="Optimizando",
            unit="iter",
            bar_format="{l_bar}{bar}| {n_fmt}/{total_fmt} [{elapsed}<{remaining}]",
        ) as bar:
            while generacion <= GENERATIONS:
                self.actualizarVelocidad()
                self.actualizarPosicion()
                self.restriccionLimites()
                self.calcularFitnessYSumaDeViolaciones()
                self.actualizarPbest()
                self.actualizarPosicionGbestDePoblacion()
                bar.update(1)
                generacion += 1
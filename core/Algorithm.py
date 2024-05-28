from utils.constantes import SIZE_POBLATION
import numpy as np
import random as rd


class Algorithm:
    
    # Metodo general para generar individuos segun los rangos superiores e inferiores 
    def generar_individuo(self, superior: list, inferior: list) -> np.array:
        # Genera los valores del individuo segun las dimensiones y dentro de los limites superior e inferior
        individuo = [
            rd.uniform(sup, inf) for sup, inf in zip(superior, inferior)
        ]
        return np.array(individuo)
    
    # Esta funcion puede generar poblaciones y tambien es utilizada para generar velocidades en PSO 
    def generar(self, inferior:list, superior:list) -> np.array:
        # Se crea una lista de poblacion
        poblacion=[]

        # Genera la poblacion de acuerdo al numero de individuos especificados
        for _ in range(SIZE_POBLATION):
            poblacion.append(self.generar_individuo(superior, inferior))
        return np.array(poblacion)
        
    # Metodo para validar un individuo
    def isValid(self, superior: list, inferior: list, x: list) -> bool:
        for sup, x, inf in zip(superior, x, inferior):
            if not (inf <= x <= sup):
                return False
        return True
    
    

    
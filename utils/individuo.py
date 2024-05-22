import numpy as np
import random as rd

# NUMERO DE POBLACIONES
NP = 100
# NUMERO DE GENERACIONES
GENERACIONES = 1000


#FUNCIÓN GENERAL PARA GENERAR INDIVIDUOS SEGÚN LOS RANGOS SUPERIORES E INFERIORES DADOS
def generar_individuo(superior: list, inferior: list) -> np.array:
    #ANTES DE GENERAR EL INDIVIDUO, EVALUA QUE LOS LIMITES TENGAN LA MISMA LONGITUD
    if len(superior) != len(inferior):
        raise ValueError("Longitud de los arreglos es diferente")

    #GENERA LOS VALORES DEL INDIVIDUO, SEGÚN LAS DIMENSIONES Y DENTRO DE LOS LÍMITES SUPERIORES E INFERIORES
    individuo = [
        rd.uniform(sup, inf) for sup, inf in zip(superior, inferior)
    ]
    return np.array(individuo)

#FUNCIÓN GENERAL PARA EVALUAR LA VALIDEZ DEL INDIVIDUO GENERADO, VERIFICANDO QUE NO TENGA VALORES FUERA DE RANGO
def isValid(superior: list, inferior: list, individuo: list) -> bool:    
    #EVALÚA QUE TODOS LOS ARRAYS TENGAN LAS MISMAS DIMENSIONES
    if len(individuo) != len(superior) or len(individuo) != len(inferior):
        raise ValueError("Longitud de los arreglos es diferente")
    
    #SI ENCUENTRA UN VALOR FUERA DE RANGO, SE TOMA COMO UN INDIVIDUO NO VÁLIDO
    for sup, ind, inf in zip(superior, individuo, inferior):
        if not (inf <= ind <= sup):
            return False
    return True

# Esta funcion puede generar poblaciones y tambien es utilizada para generar velocidades en PSO 
def generar(inferiores:list, superiores:list) -> np.array:
    poblacion=[]

    #GENERA LA POBLACIÓN DE ACUERDO AL NÚMERO DE INDIVIDUOS ESPECIFICADOS
    for _ in range(NP):
        poblacion.append(generar_individuo(inferiores,superiores))
    return np.array(poblacion)
    

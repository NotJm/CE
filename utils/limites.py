import numpy as np
import random as rd

#METODO BOUNDARY PARA MANEJAR RESTRICCIONES DE LÍMITES DENTRO DE LOS VALORES DE UN INDIVIDUO
def boundary(superior: list, inferior: list, individuo: np.array) -> np.array:
    #EVALÚA QUE TODOS LOS ARRAYS TENGAN LAS MISMAS DIMENSIONES
    if len(individuo) != len(superior) or len(individuo) != len(inferior):
        raise ValueError("Los arreglos de límites inferiores, superiores y el individuo deben ser iguales en longitud")
    
    individuo_corregido = np.copy(individuo)
    
    #SE HACE UN RECORRIDO POR CADA UNO DE LOS VALORES EVALUANDO SI ESTAN DENTRO DE RANGOS
    for i in range(len(individuo)):
        #SI ES MENOR AL INFERIOR, DIRECTAMENTE PONE EL LÍMITE INFERIOR
        if individuo[i] < inferior[i]:
            individuo_corregido[i] = inferior[i]
        #SI ES MAYOR AL SUPERIOR, DIRECTAMENTE PONE EL LÍMITE SUPERIOR
        elif individuo[i] > superior[i]:
            individuo_corregido[i] = superior[i]
    
    return individuo_corregido

#METODO DE REFLEXIÓN PARA MANEJAR RESTRICCIONES DE LÍMITES DENTRO DE LOS VALORES DE UN INDIVIDUO
def reflex(superior: list, inferior: list, individuo: np.array) -> np.array:
    # EVALÚA QUE TODOS LOS ARRAYS TENGAN LAS MISMAS DIMENSIONES
    if len(individuo) != len(superior) or len(individuo) != len(inferior):
        raise ValueError("Los arreglos de límites inferiores, superiores y el individuo deben ser iguales en longitud")

    individuo_corregido = []
    # SE HACE UN RECORRIDO POR CADA UNO DE LOS VALORES EVALUANDO SI ESTAN DENTRO DE RANGOS
    for ind, inf, sup in zip(individuo, inferior, superior):
        # SI EL VALOR ES MENOR AL INFERIOR,
        if ind < inf:
            # REFLEJA EL VALOR AL INTERIOR DEL RANGO
            corregido = inf + (inf - ind)
            # SI EL VALOR REFLEJADO EindividuoCEDE EL LÍMITE SUPERIOR, AJUSTA AL LÍMITE SUPERIOR
            if corregido > sup:
                corregido = sup
        # SI EL VALOR ES MAYOR AL SUPERIOR,
        elif ind > sup:
            # REFLEJA EL VALOR AL INTERIOR DEL RANGO
            corregido = sup - (ind - sup)
            # SI EL VALOR REFLEJADO EindividuoCEDE EL LÍMITE INFERIOR, AJUSTA AL LÍMITE INFERIOR
            if corregido < inf:
                corregido = inf
        else:
            # SI EL VALOR ESTÁ DENTRO DE LOS LÍMITES, NO HACE FALTA CORRECCIÓN
            corregido = ind
        # AÑADE EL VALOR CORREGIDO A LA LISTA
        individuo_corregido.append(corregido)
    
    # CONVIERTE LA LISTA DE VALORES CORREGIDOS A UN ARRAY DE NUMPY Y LO RETORNA
    return np.array(individuo_corregido)

#METODO RANDOM PARA MANEJAR RESTRICCIONES DE LÍMITES DENTRO DE LOS VALORES DE UN INDIVIDUO
def random(superior:list, inferior:list, individuo:np.array) -> np.array:
    # EVALÚA QUE TODOS LOS ARRAYS TENGAN LAS MISMAS DIMENSIONES
    if len(individuo) != len(superior) or len(individuo) != len(inferior):
        raise ValueError("Los arreglos de límites inferiores, superiores y el individuo deben ser iguales en longitud")

    individuo_corregido = []
    
    # RECORRE CADA VALOR DEL INDIVIDUO JUNTO CON SUS CORRESPONDIENTES LÍMITES INFERIOR Y SUPERIOR
    for sup, ind, inf in zip(superior, individuo, inferior):
        # SI EL VALOR ESTÁ FUERA DE LOS LÍMITES, SE GENERA UNO NUEVO DENTRO DEL RANGO
        if ind > sup or ind < inf:
            # SE GENERA UN NUEVO VALOR ALEATORIO DENTRO DEL RANGO [inf, sup]
            ind = inf + rd.uniform(0, 1) * (sup - inf)
            individuo_corregido.append(ind)
        else:
            # SI EL VALOR ESTÁ DENTRO DEL RANGO, SE MANTIENE TAL CUAL
            individuo_corregido.append(ind)
        
    # CONVIERTE LA LISTA DE VALORES CORREGIDOS A UN ARRAY DE NUMPY Y LO RETORNA
    return np.array(individuo_corregido)

#METODO EVOLUTIONARY PARA MANEJAR RESTRICCIONES DE LÍMITES DENTRO DE LOS VALORES DE UN INDIVIDUO
def evolutionary(superior:list, inferior:list, individuo:np.array, bestInd:np.array) -> np.array:
    
    if len(individuo) != len(superior) or len(individuo) != len(inferior) or len(individuo) != len(bestInd):
        raise ValueError("Los arreglos de límites inferiores, superiores, el individuo y el bestIndividuo deben ser iguales en longitud")
    
    alpha = rd.random()
    beta = rd.random()
    
    individuo_corregido = []
    
    for sup, inf, ind, best in zip(superior, inferior, individuo, bestInd):
        # Si el componente está dentro de los límites, se mantiene igual
        if ind >= inf and ind <= sup:
            individuo_corregido.append(ind)
        # Si el componente es menor que el límite inferior, se ajusta hacia él
        elif ind < inf:
            new_component = alpha * inf + (1 - alpha) * best
            individuo_corregido.append(new_component)
        # Si el componente es mayor que el límite superior, se ajusta hacia él
        else:
            new_component = beta * sup + (1 - beta) * best
            individuo_corregido.append(new_component)
    
    # CONVIERTE LA LISTA DE VALORES CORREGIDOS A UN ARRAY DE NUMPY Y LO RETORNA
    return np.array(individuo_corregido)
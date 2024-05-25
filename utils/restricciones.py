import numpy as np


def suma_violaciones(g_funcs, h_funcs, x):
    # Calcular la suma de max(0, g_j(x))^2
    suma_desigualdad = sum(max(0, g(x)) ** 2 for g in g_funcs)

    # Calcular la suma de |h_k(x)|
    suma_igualdad = sum(abs(h(x)) for h in h_funcs)

    # Suma total de violaciones de restricciones
    suma_violaciones = suma_desigualdad + suma_igualdad

    return round(suma_violaciones)

def aEsMejorQueB_deb(a_fitness, a_violaciones, b_fitness, b_violaciones) ->bool:
        # Regla 1: Entre dos soluciones factibles, se elige la de menor valor en la función objetivo.
        if a_violaciones == 0 and b_violaciones == 0:
            if a_fitness <= b_fitness:
                return True
            else:
                return False
         # Regla 3: Entre dos soluciones infactibles se elige el menor valor en la funcion objectivo
        elif a_violaciones != 0 and b_violaciones != 0:
            if a_violaciones <= b_violaciones:
                return True
            else:
                return False
        elif a_violaciones == 0 and b_violaciones != 0:
            return  True
        else:
            return False


def deb(poblacion, fitness, violaciones):
    best_fitness = fitness[0]
    best_violacion = violaciones[0]
    best_posicion = 0

    for x in range(1, len(poblacion)):

        current_fitness = fitness[x]
        current_violacion = violaciones[x]
        
        if aEsMejorQueB_deb(best_fitness, best_violacion, current_fitness, current_violacion) == False:
            best_fitness = current_fitness
            best_violacion = current_violacion
            best_posicion = x
        

            
    return best_posicion

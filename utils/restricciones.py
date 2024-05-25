import numpy as np

def suma_violaciones(g_funcs, h_funcs, x):
    # Calcular la suma de max(0, g_j(x))^2
    suma_desigualdad = sum(max(0, g(x))**2 for g in g_funcs)
    
    # Calcular la suma de |h_k(x)|
    suma_igualdad = sum(abs(h(x)) for h in h_funcs)
    
    # Suma total de violaciones de restricciones
    suma_violaciones = suma_desigualdad + suma_igualdad
    
    return suma_violaciones

def deb(ind1, ind2):
    # Extraer fitness y número de violaciones de cada individuo
    fit1, viol1 = ind1[1], ind1[2]
    fit2, viol2 = ind2[1], ind2[2]
    
    # Regla 1: Entre dos soluciones factibles, se elige la de menor valor en la función objetivo.
    if viol1 == 0 and viol2 == 0:
        # Verifica si fit1 realmente es menor que fit2
        return ind1 if fit1 < fit2 else ind2
    
    # Regla 2: Entre una solución factible y una infactible, se elige la factible.
    if viol1 == 0 and viol2 != 0:
        return ind1
    if viol1 != 0 and viol2 == 0:
        return ind2
    
    # Regla 3: Entre dos soluciones infactibles, se elige la que tenga menor suma de violaciones.
    return ind1 if viol1 < viol2 else ind2


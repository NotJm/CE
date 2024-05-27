class Restricciones:
    @staticmethod
    # Metodo para obtener el total de violaciones
    def suma_violaciones(g_funcs:list, h_funcs:list, x) -> float:
        # Calcular la suma de desigualdades
        suma_desigualdad = sum(max(0, g(x)) ** 2 for g in g_funcs)

        # Calcular la suma de |h_k(x)|
        suma_igualdad = sum(abs(h(x)) for h in h_funcs)

        # Suma total de violaciones de restricciones
        suma_violaciones = suma_desigualdad + suma_igualdad

        return suma_violaciones
    
    @staticmethod
    # Metodo para obtener el mejor individuo en base al as reglas de DEB
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

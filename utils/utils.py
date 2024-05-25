import numpy as np

class CEC2006_g02:
    @staticmethod
    def CEC2006_g02_aptitud(individuo):
        sum_cos4 = np.sum(np.cos(individuo)**4)
        prod_cos2 = np.prod(np.cos(individuo)**2)
        sum_ix2 = np.sum((np.arange(1, len(individuo) + 1) * individuo**2))
        f_x = -abs((sum_cos4 - 2 * prod_cos2) / np.sqrt(sum_ix2))
        return f_x

    @staticmethod
    def CEC2006_g02_g1(x):  # restriccion 1 de desigualdad <= 0
        product_x = np.prod(x)
        result = 0.75 - product_x
        return result

    @staticmethod
    def CEC2006_g02_g2(x):  # restriccion 2 de desigualdad <= 0
        sum_x = np.sum(x)
        n = len(x)
        result = sum_x - 7.5 * n
        return result

# Función para verificar si un individuo viola alguna restricción
def violate_constraint(x):
    g1 = CEC2006_g02.CEC2006_g02_g1(x)
    g2 = CEC2006_g02.CEC2006_g02_g2(x)
    return g1 > 0 or g2 > 0

# Función para actualizar el pbest considerando restricciones
def update_pbest_with_constraints(position, pbest_position, pbest_value, objective_function):
    current_value = objective_function(position)
    if not violate_constraint(position):  # Si no viola ninguna restricción
        if current_value <= pbest_value:
            return position, current_value
        else:
            return pbest_position, pbest_value
    else:  # Si viola restricciones, siempre se mantiene el pbest actual
        return pbest_position, pbest_value

# Ejemplo de uso
current_position = np.array([1.0, 2.0, 3.0])
pbest_position = np.array([1.5, 2.5, 3.5])
pbest_value = CEC2006_g02.CEC2006_g02_aptitud(pbest_position)

new_pbest_position, new_pbest_value = update_pbest_with_constraints(current_position, pbest_position, pbest_value, CEC2006_g02.CEC2006_g02_aptitud)

print("Nueva mejor posición personal conocida:", new_pbest_position)
print("Nuevo valor de la función objetivo:", new_pbest_value)
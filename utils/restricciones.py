import numpy as np

# NUMERO DE DIMENSIONES
DIM = 20

g01 = lambda individuo : [
            2*individuo[0] + 2*individuo[1] + individuo[9] + individuo[10] - 10 <=0 ,
            2*individuo[0] + 2*individuo[2] + individuo[9] + individuo[11] - 10 <= 0,
            2*individuo[1] + 2*individuo[2] + individuo[10] + individuo[11] - 10 <= 0,
            -8*individuo[0] + individuo[9] <= 0,
            -8*individuo[1] + individuo[10] <= 0,
            -8*individuo[2] + individuo[11] <= 0,
            -2*individuo[3] - individuo[4] + individuo[9] <= 0,
            -2*individuo[5] - individuo[6] + individuo[10] <= 0,
            -2*individuo[7] - individuo[8] + individuo[11] <= 0
        ]

g02 = lambda individuo, DIM : [
    0.75 - np.prod(individuo) <= 0,
    np.sum(individuo) - 7.5 * DIM  <= 0
]

def aptitud(poblacion, funcion_a_evaluar, restriccion) -> np.array:
        aptitud = []
        for ind in poblacion:
            _aptitud = funcion_a_evaluar(ind, restriccion)
            aptitud.append(_aptitud["fitness"])
        return np.array(aptitud)

def evaluar(individuo: np.array, restriccion) -> dict:
    
    # Calculo de la evaluacion
    sum_cos4 = np.sum(np.cos(individuo)**4)
    prod_cos2 = np.prod(np.cos(individuo)**2)
    sum_ix2 = np.sum((np.arange(1, len(individuo) + 1) * individuo**2))
    f_x = -abs((sum_cos4 - 2 * prod_cos2) / np.sqrt(sum_ix2))
    # Calculo de restricciones
    evaluacion_de_restriccion = restriccion(individuo, DIM)
    # Numero de violaciones
    violaciones = calcular_violaciones(evaluacion_de_restriccion)
    # Regresar tupla con el numero de violaciones y la evaluacion del fitness
    return {
        "fitness": f_x,
        "noViolaciones": violaciones,
    } 

def calcular_violaciones(evaluacion:list) -> int:
    return sum(not r for r in evaluacion)

# ind =  np.array([5.042501248669893, 4.903689764627512, 5.175878512792987, 6.3567532710437415, 6.338648390703745, 8.633279060085732, 5.98341658374363, 7.903441780999399, 6.905131730783916, 8.914427685999197, 4.326850911813325, 6.744178835543046, 1.5450765973702796, 5.2620806382948615, 6.350606837124625, 3.2951566461112103, 9.168816371841658, 5.619434423271179, 3.7363566031325837, 2.9019936095073016])
# data_evaluation = evaluar(ind, g02)
# print(data_evaluation)
# print(np.prod(ind))
# print(0.75 - np.prod(ind))
# print(np.sum(ind) - 7.5 * DIM)
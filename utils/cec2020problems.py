import numpy as np
from Problem import Problem, ProblemType

# Problema 01
class CEC2006_G01(Problem):
    
    SUPERIOR = [1,1,1,1,1,1,1,1,1,100,100,100,1]
    INFERIOR = [0,0,0,0,0,0,0,0,0,0,0,0,0]

    def __init__(self):
        rest_g = [
            CEC2006_G01.cec2006_g01_g1,
            CEC2006_G01.cec2006_g01_g2,
            CEC2006_G01.cec2006_g01_g3,
            CEC2006_G01.cec2006_g01_g4,
            CEC2006_G01.cec2006_g01_g5,
            CEC2006_G01.cec2006_g01_g6,
            CEC2006_G01.cec2006_g01_g7,
            CEC2006_G01.cec2006_g01_g8,
            CEC2006_G01.cec2006_g01_g9
        ]
        super().__init__(ProblemType.CONSTRAINED, CEC2006_G01.SUPERIOR, CEC2006_G01.INFERIOR, rest_g, [])
    
    def fitness(self, individuo: np.array) -> float:
        sum1 = np.sum(individuo[0:4])
        sum2 = np.sum(individuo[0:4]**2)
        sum3 = np.sum(individuo[4:13])
        f_x = 5 * sum1 - 5 * sum2 - sum3
        return f_x

    @staticmethod
    def cec2006_g01_g1(x):
        return 2 * x[0] + 2 * x[1] + x[9] + x[10] - 10  # restriccion 1 de desigualdad <= 0
    
    @staticmethod
    def cec2006_g01_g2(x):
        return 2 * x[0] + 2 * x[2] + x[9] + x[11] - 10  # restriccion 2 de desigualdad <= 0
    
    @staticmethod
    def cec2006_g01_g3(x):
        return 2 * x[1] + 2 * x[2] + x[10] + x[11] - 10 # restriccion 3 de desigualdad <= 0
    
    @staticmethod
    def cec2006_g01_g4(x):
        return -8 * x[0] + x[9] # restriccion 4 de desigualdad <= 0
    
    @staticmethod
    def cec2006_g01_g5(x):
        return -8 * x[1] + x[10] # restriccion 5 de desigualdad <= 0
    
    @staticmethod
    def cec2006_g01_g6(x):
        return -8 * x[2] + x[11] # restriccion 6 de desigualdad <= 0
    
    @staticmethod              
    def cec2006_g01_g7(x):
        return -2 * x[3] - x[4] + x[9] #restriccion 7 de desigualdad <= 0

    @staticmethod
    def cec2006_g01_g8(x):
        return -2 * x[5] - x[6] + x[10] # restriccion 8 de desigualdad <= 0

    @staticmethod
    def cec2006_g01_g9(x):
        return -2 * x[7] - x[8] + x[11] # restriccion 9 de desigualdad <= 0
    


#Notas: x es un arrelo de tamaño t= 13 y 0 ≤ xi ≤ 1(i = 1,...,9),0 ≤ xi ≤ 100(i = 10,11,12) 

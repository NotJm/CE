import numpy as np
from .Problem import Problem, ProblemType

# Problema 01
class CEC2020_RC01(Problem):
    
    # WITH BOUNDS:
    
    # 0 ≤ x1 ≤ 10, 0 ≤ x2 ≤ 200, 0 ≤ x3 ≤ 100, 0 ≤ x4 ≤ 200,
    # 1000 ≤ x5 ≤ 2000000, 0 ≤ x6 ≤ 600, 100 ≤ x7 ≤ 600, 100 ≤ x8 ≤ 600,
    # 100 ≤ x9 ≤ 900.
    
    SUPERIOR = np.array([10,200,100,200,2000000,600,600,600,900])
    INFERIOR = np.array([0,0,0,0,1000,0,100,100,100])

    def __init__(self):
        rest_h = [
            CEC2020_RC01.CEC2020_RC01_h1,
            CEC2020_RC01.CEC2020_RC01_h2,
            CEC2020_RC01.CEC2020_RC01_h3,
            CEC2020_RC01.CEC2020_RC01_h4,
            CEC2020_RC01.CEC2020_RC01_h5,
            CEC2020_RC01.CEC2020_RC01_h6,
            CEC2020_RC01.CEC2020_RC01_h7,
            CEC2020_RC01.CEC2020_RC01_h8,
        ]
        super().__init__(ProblemType.CONSTRAINED, CEC2020_RC01.SUPERIOR, CEC2020_RC01.INFERIOR, [],  rest_h)
    
    def fitness(self, individuo: np.array) -> float:
        f_x = 35 * individuo[0]**0.6 + 35 * individuo[1]**0.6
        return f_x

    @staticmethod
    def CEC2020_RC01_h1(x):
        return 200 * x[0] * x[3] - x[2]  # restriccion 1 de igualdad = 0
    
    @staticmethod
    def CEC2020_RC01_h2(x):
        return 200 * x[1] * x[5] - x[4]  # restriccion 2 de igualdad = 0
    
    @staticmethod
    def CEC2020_RC01_h3(x):
        return x[2] - 10000 * (x[6] - 100)  # restriccion 3 de igualdad = 0
    
    @staticmethod
    def CEC2020_RC01_h4(x):
        return x[4] - 10000 * (300 - x[6])  # restriccion 4 de igualdad = 0
    
    @staticmethod
    def CEC2020_RC01_h5(x):
        return x[2] - 10000 * (600 - x[7]) # restriccion 5 de igualdad = 0
    
    @staticmethod
    def CEC2020_RC01_h6(x):
        return x[4] - 10000 * (900 - x[8]) # restriccion 6 de igualdad = 0
    
    @staticmethod              
    def CEC2020_RC01_h7(x):
        return x[3] * np.log(x[7] - 100) - x[3] * np.log(600 - x[6]) - x[7] + x[6] + 500 #restriccion 7 de igualdad = 0

    @staticmethod
    def CEC2020_RC01_h8(x):
        return x[5] * np.log(x[8] - x[6]) - x[5] * np.log(600) - x[8] + x[6] + 600 # restriccion 8 de igualdad = 0

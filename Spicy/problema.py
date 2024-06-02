# problemas.py
import numpy as np

class Problema:
    def __init__(self, superior, inferior, rest_g):
        self.SUPERIOR = np.array(superior)
        self.INFERIOR = np.array(inferior)
        self.rest_g = rest_g

    def fitness(self, individuo: np.array) -> float:
        raise NotImplementedError("La función de fitness debe ser implementada por la subclase.")

class CEC2006_G01(Problema):
    def __init__(self):
        superior = [1, 1, 1, 1, 1, 1, 1, 1, 1, 100, 100, 100, 1]
        inferior = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        rest_g = [
            self.cec2006_g01_g1,
            self.cec2006_g01_g2,
            self.cec2006_g01_g3,
            self.cec2006_g01_g4,
            self.cec2006_g01_g5,
            self.cec2006_g01_g6,
            self.cec2006_g01_g7,
            self.cec2006_g01_g8,
            self.cec2006_g01_g9
        ]
        super().__init__(superior, inferior, rest_g)

    def fitness(self, individuo: np.array) -> float:
        sum1 = np.sum(individuo[0:4])
        sum2 = np.sum(individuo[0:4]**2)
        sum3 = np.sum(individuo[4:13])
        f_x = 5 * sum1 - 5 * sum2 - sum3
        return f_x

    @staticmethod
    def cec2006_g01_g1(x):
        return 2 * x[0] + 2 * x[1] + x[9] + x[10] - 10
    
    @staticmethod
    def cec2006_g01_g2(x):
        return 2 * x[0] + 2 * x[2] + x[9] + x[11] - 10
    
    @staticmethod
    def cec2006_g01_g3(x):
        return 2 * x[1] + 2 * x[2] + x[10] + x[11] - 10
    
    @staticmethod
    def cec2006_g01_g4(x):
        return -8 * x[0] + x[9]
    
    @staticmethod
    def cec2006_g01_g5(x):
        return -8 * x[1] + x[10]
    
    @staticmethod
    def cec2006_g01_g6(x):
        return -8 * x[2] + x[11]
    
    @staticmethod              
    def cec2006_g01_g7(x):
        return -2 * x[3] - x[4] + x[9]

    @staticmethod
    def cec2006_g01_g8(x):
        return -2 * x[5] - x[6] + x[10]

    @staticmethod
    def cec2006_g01_g9(x):
        return -2 * x[7] - x[8] + x[11]

# Puedes agregar otros problemas definiendo otras subclases similares a CEC2006_G01

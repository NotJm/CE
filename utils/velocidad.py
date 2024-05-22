import numpy as np
import random as rd
L = -0.3

def dba(velocidad: np.array) -> np.array:
    return np.array([ v * L for v in velocidad])

def rba(velocidad: np.array) -> np.array:
    R = rd.uniform(0, 1)
    return np.array([ v * R for v in velocidad])
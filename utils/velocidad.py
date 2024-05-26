import numpy as np
import random as rd


def dba(velocidad: np.array) -> np.array:
    L = -0.3
    return np.array([ v * L for v in velocidad])

def rba(velocidad: np.array) -> np.array:
    R = rd.uniform(0, 1)
    return np.array([ v * R for v in velocidad])

def aze(velocidad: np.array) -> np.array:
    return np.array([ v * 0 for v in velocidad])

def adj(new_position: np.array, previous_position: np.array) -> np.array:
    velocity = new_position - previous_position
    return velocity
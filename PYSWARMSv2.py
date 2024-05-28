from problems.cec2006problems import CEC2006_G01
from core.Restricciones import Restricciones
from pyswarms.utils.plotters import plot_cost_history
from pyswarms.utils.functions import single_obj as fx
import matplotlib.pyplot as plt
import numpy as np
import random as rd
import pyswarms as ps

problema = CEC2006_G01()

bounds = (problema.SUPERIOR, problema.INFERIOR)

options = {'c1': 1.4944, 'c2': 1.4944, 'w': 0.95}

NP = 100
dimensions = 13

optimizer = ps.single.GlobalBestPSO(
    n_particles=NP,
    dimensions=dimensions,
    options=options,
    bounds=bounds,
    bh_strategy="reflective"
)

fitness, pos = optimizer.optimize(problema.fitness, iters=25)
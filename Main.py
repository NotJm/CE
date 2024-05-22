from PSO import PSO
from progress.bar import Bar
import numpy as np
import time
import os

if __name__ == '__main__':
    pso = PSO("boundary")
    iterations = 25   
    ind = [] 
    apt = []
    vio = []
    with Bar('Procesando', max=iterations) as bar:
        for i in range(iterations):
            pso.start()
            ind.append(pso.gbestIndviduo)
            apt.append(pso.gbestAptitud)
            vio.append(pso.gbestIndVio)
            pso.reset()
            bar.next()

    for i, a, v in zip(ind, apt, vio):
        print("Individuo:", i)
        print("Aptitud:", a)
        print("Violaciones:", v)#
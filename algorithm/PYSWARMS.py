# Import modules
import numpy as np

# Import PySwarms
import pyswarms as ps
from pyswarms.utils.functions import single_obj as fx

# Import problems
from cec2006problems import *

# Set-up bounds
upper = np.array([1, 1, 1, 1, 1, 1, 1, 1, 1, 100, 100, 100, 1])
lower = np.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0])


# Set-up hyperparameters
options = {'c1': 1.4944, 'c2': 1.4944   , 'w':0.95}

bounds = (
    upper,
    lower
)

# Call instance of PSO
optimizer = ps.single.GlobalBestPSO(
    n_particles=100,
    dimensions=13, 
    options=options,
    bounds=bounds,
    bh_strategy="reflective",
    )



# Perform optimization
cost, pos = optimizer.optimize(fx.sphere, iters=1000)
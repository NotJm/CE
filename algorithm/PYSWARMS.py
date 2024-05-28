import numpy as np
import pyswarms as ps
from pyswarms.utils.functions import single_obj as fx


# Definir los límites
lower = np.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0])
upper = np.array([1, 1, 1, 1, 1, 1, 1, 1, 1, 100, 100, 100, 1])

# Configurar los hiperparámetros
options = {'c1': 1.4944, 'c2': 1.4944, 'w': 0.95}

# Establecer los límites
bounds = (lower, upper)

# Crear instancia del optimizador PSO con límites personalizados
optimizer = ps.single.GlobalBestPSO(
    n_particles=100,
    dimensions=13,
    options=options,
    bounds=bounds,
    bh_strategy="reflective"
)

# Ejecutar la optimización para minimizar la función de esfera
cost, pos = optimizer.optimize(fx.sphere, iters=1000)

print("Mejor costo encontrado:", cost)
print("Mejor posición encontrada:", pos)

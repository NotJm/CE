from matplotlib import pyplot as plt
from PSO import PSO
import csv

def plot_power(data_fitness_exp1, data_fitness_exp2, data_fitness_exp3):
    plt.figure(figsize=(6, 6))
    plt.boxplot([data_fitness_exp1, data_fitness_exp2, data_fitness_exp3], labels=['Reflexion', 'Random', 'Boundary'])
    plt.title('Function Power Difference')
    plt.ylabel('Fitness')
    plt.xlabel('Limit Type')
    plt.grid(True)
    plt.show()

def plot_sphere(data_fitness_exp4, data_fitness_exp5, data_fitness_exp6):
    plt.figure(figsize=(6, 6))
    plt.boxplot([data_fitness_exp4, data_fitness_exp5, data_fitness_exp6], labels=['Reflexion', 'Random', 'Boundary'])
    plt.title('Sphere Function')
    plt.ylabel('Fitness')
    plt.xlabel('Limit Type')
    plt.grid(True)
    plt.show()

def crear_csv(ref, boundary):
    import csv
    
    with open('psoBoundary.csv', 'w', newline='') as csvfile:
        writer = csv.writer(csvfile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        
        # Escribir encabezados para la tabla Boundary
        writer.writerow(["Boundary Table"])
        writer.writerow(["No", "Aptitud", "Factible"])
        for i, (fitness, violacion) in enumerate(boundary):
            writer.writerow([i + 1, fitness, 0   if violacion else 1])
        
    with open('psoRefleccion.csv', 'w', newline='') as csvfile:
        writer = csv.writer(csvfile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        
        # Escribir encabezados para la tabla Reflección
        writer.writerow(["Reflección Table"])
        writer.writerow(["No", "Aptitud", "Factible"])
        for i, (fitness, violacion) in enumerate(ref):
            writer.writerow([i + 1, fitness, 0 if violacion else 1])

def boundary() -> list:
    pso_boundary_data_fitness = []
    print("Boundary Limit")
    pso_boundary = PSO(limite="bounce")
    for _ in range(25):
        pso_boundary.start()
        pso_boundary.reset() 
    pso_boundary_data_fitness = pso_boundary._data_fitness
    results = []
    for j in range(len(pso_boundary_data_fitness)):
        fitness = pso_boundary_data_fitness[j]
        violacion = False if pso_boundary._violaciones_individuo[j] > 0 else True
        print(f"Fitness Numero {j}: {fitness}, {violacion}")
        results.append((fitness, violacion))
        
    return results
    
def ref() -> list:
    pso_ref_data_fitness = []
    print("Reflextion Limit")
    pso_ref = PSO(limite="ref")
    for _ in range(25):
        pso_ref.start()
        pso_ref.reset()
    
    pso_ref_data_fitness = pso_ref._data_fitness
    results = []
    for i in range(len(pso_ref_data_fitness)):
        fitness = pso_ref_data_fitness[i]
        violacion = False if pso_ref._violaciones_individuo[i] > 0 else True
        print(f"Fitness Numero {i}: {fitness}, {violacion}")
        results.append((fitness, violacion))
    
        
    return results

if __name__ == "__main__":  
    data_ref = ref()
    data_boundary = boundary()
    crear_csv(data_ref, data_boundary)
"""
# Inicializamos las listas para almacenar los datos de fitness de cada experimento
    manager = Manager()
    data_fitness_exp1 = manager.list()
    data_fitness_exp2 = manager.list()
    data_fitness_exp3 = manager.list()
    data_fitness_exp4 = manager.list()
    data_fitness_exp5 = manager.list()
    data_fitness_exp6 = manager.list()
    
    print("REF & POWER")
    for _ in range(25):
        exp1 = PSO(limite="ref", function="power")
        exp1.start()
        data_fitness_exp1.extend(exp1._data_fitness)  # Usamos extend en lugar de append
    
    print("RAND & POWER")
    for _ in range(25):
        exp2 = PSO(limite="rand", function="power")
        exp2.start()
        data_fitness_exp2.extend(exp2._data_fitness)  # Usamos extend en lugar de append
    
    print("BOUNCE & POWER")  
    for _ in range(25):
        exp3 = PSO(limite="bounce", function="power")
        exp3.start()
        data_fitness_exp3.extend(exp3._data_fitness)  # Usamos extend en lugar de append
    
    print("REF & SPHERE")
    for _ in range(25):
        exp4 = PSO(limite="ref", function="sphere")
        exp4.start()
        data_fitness_exp4.extend(exp4._data_fitness)  # Usamos extend en lugar de append
    
    print("RAND & SPHERE")
    for _ in range(25):
        exp5 = PSO(limite="rand", function="sphere")
        exp5.start()
        data_fitness_exp5.extend(exp5._data_fitness)  # Usamos extend en lugar de append
    
    print("BOUNCE & SPHERE")
    for _ in range(25):
        exp6 = PSO(limite="bounce", function="sphere")
        exp6.start()
        data_fitness_exp6.extend(exp6._data_fitness)  # Usamos extend en lugar de append

    power_process = Process(target=plot_power, args=(data_fitness_exp1, data_fitness_exp2, data_fitness_exp3))
    sphere_process = Process(target=plot_sphere, args=(data_fitness_exp4, data_fitness_exp5, data_fitness_exp6))
    
    power_process.start()
    sphere_process.start()
    
    power_process.join()
    sphere_process.join()
    
    
    
"""
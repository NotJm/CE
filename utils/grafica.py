import matplotlib.pyplot as plt

def plot_convergence(individuo):
    
    generations = [gen for gen, fit in individuo]
    fitness_values = [fit for gen, fit in individuo]

    plt.figure(figsize=(10, 6))
    plt.plot(generations, fitness_values, marker='o', linestyle='-', color='b')
    plt.title('Convergence Graph')
    plt.xlabel('Generation')
    plt.ylabel('Fitness Value')
    plt.grid(True)
    plt.show()
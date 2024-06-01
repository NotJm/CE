from problema import CEC2006_G01
from DE import Ev_Diferencial_Con_SciPy
from constantes import SIZE_POBLATION, GENERATIONS
from Limites import Limite  # Importamos los métodos de corrección de límites desde el módulo correspondiente

def main():
    # Selecciona el problema
    problema = CEC2006_G01()
    
    # Selecciona el método de corrección de límites (puedes cambiar 'reflex' por 'random' o cualquier otro)
    metodo_limite = Limite.reflex
    
    best_individual, best_fitness, best_violaciones = Ev_Diferencial_Con_SciPy(problema, SIZE_POBLATION, GENERATIONS, metodo_limite)
    print("Resultado:", best_individual)
    print("Fitness:", best_fitness)
    print("Violaciones:", best_violaciones)

if __name__ == "__main__":
    main()

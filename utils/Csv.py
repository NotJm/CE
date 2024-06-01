import csv 
import os

# Función para guardar los resultados óptimos en un CSV, agregando nuevas filas
def mejor_solucion_csv(gbestParticula, gbestAptitud, gbestViolacion, filename):
    # Verificar si el archivo ya existe
    file_exists = os.path.isfile(filename)
    
    with open(filename, mode='a', newline='') as file:
        writer = csv.writer(file)
        # Escribir los encabezados solo si el archivo no existe
        if not file_exists:
            writer.writerow(["Mejor Posicion de la Particula", "Fitness de la Particula", "Minimo Numero de Infracciones"])
        # Escribir los resultados
        writer.writerow([gbestParticula, gbestAptitud, gbestViolacion])
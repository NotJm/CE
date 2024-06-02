import numpy as np
import random as rd
class Limite:
    @staticmethod
    # Metodo boundary para manejar restriccion de limites de individuo
    def boundary(superior: list, inferior: list, individuo: np.array) -> np.array:
        individuo_corregido = np.copy(individuo)

        for i in range(len(individuo)):
            if individuo[i] < inferior[i]:
                individuo_corregido[i] = inferior[i]
            elif individuo[i] > superior[i]:
                individuo_corregido[i] = superior[i]

        return individuo_corregido

    @staticmethod
    # Metodo de reflex para manejar restricciones  de limites dentro de los valores de un individuo
    def reflex(superior, inferior, individuo) -> np.array:
        range_width = superior - inferior
        individuo_corregido = np.copy(individuo)

        for j in range(len(individuo)):
            if individuo_corregido[j] < inferior[j]:
                individuo_corregido[j] = (
                    inferior[j]
                    + (inferior[j] - individuo_corregido[j]) % range_width[j]
                )
            elif individuo_corregido[j] > superior[j]:
                individuo_corregido[j] = (
                    superior[j]
                    - (individuo_corregido[j] - superior[j]) % range_width[j]
                )

        return individuo_corregido

    @staticmethod
    # Metodo random para manejar restricciones de limites dentro de los valores de un individuo
    def random(superior: list, inferior: list, individuo: np.array) -> np.array:
        individuo_corregido = []

        for sup, ind, inf in zip(superior, individuo, inferior):
            if ind > sup or ind < inf:
                ind = inf + rd.uniform(0, 1) * (sup - inf)
                individuo_corregido.append(ind)
            else:
                individuo_corregido.append(ind)

        return np.array(individuo_corregido)

    @staticmethod
    # Metodo evolutionary para manejar restricciones de limites dentro de los valores de un individuo
    def evolutionary(
        superior: list, inferior: list, individuo: np.array, bestInd: np.array
    ) -> np.array:

        alpha = rd.random()
        beta = rd.random()

        individuo_corregido = []

        for sup, inf, ind, best in zip(superior, inferior, individuo, bestInd):
            if ind >= inf and ind <= sup:
                individuo_corregido.append(ind)
            elif ind < inf:
                new_component = alpha * inf + (1 - alpha) * best
                individuo_corregido.append(new_component)
            else:
                new_component = beta * sup + (1 - beta) * best
                individuo_corregido.append(new_component)

        return np.array(individuo_corregido)

    # Metodo wrapping para maenjar restricciones de limites dentro de los valores de un individuo
    def wrapping(superior, inferior, individuo) -> np.array:
        range_width = abs(superior - inferior)
        individuo_corregido = np.copy(individuo)

        for i in range(len(individuo)):
            if individuo_corregido[i] < inferior[i]:
                individuo_corregido[i] = (
                    superior[i] - (inferior[i] - individuo_corregido[i]) % range_width[i]
                )
            elif individuo_corregido[i] > superior[i]:
                individuo_corregido[i] = (
                    inferior[i] + (individuo_corregido[i] - superior[i]) % range_width[i]
                )
                
        return individuo_corregido

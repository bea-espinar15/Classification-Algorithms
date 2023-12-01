
#
#   CLASE ALGORITMO LLOYD
#   ---------------------
#   Clase que implementa el algoritmo de Lloyd.
#   Actúa como clase estática, sin atributos.
#

import numpy as np
import Utilities


class Lloyd:

    # Calcula la distancia euclídea entre dos vectores
    @staticmethod
    def dist(x, c):
        return np.linalg.norm(x - c)

    # Comprueba si se cumple el criterio de finalización
    @staticmethod
    def check_tolerance(old, new):
        for i in range(len(old)):
            if Lloyd.dist(new[i], old[i]) >= Utilities.LLOYD_EPS:
                return False
        return True

    # Calcula el centro (el índice*) más próximo a la muestra x[j] de entre
    # los disponibles en c[]
    @staticmethod
    def closest_centroid(j, x, c):
        closest = -1
        min_dist = float('inf')
        for i in range(len(c)):
            dist = Lloyd.dist(x[j], c[i])**2
            if dist < min_dist:
                min_dist = dist
                closest = i
        return closest

    # Método que ejecuta el algoritmo:
    # · Entrada -> <muestras>
    # · Salida -> <centros_obtenidos, nº_iteraciones_ejecutadas>
    @staticmethod
    def execute(data_set, data_ver):

        # Unir los dos vectores de muestras
        data = data_set + data_ver
        # Inicializar n y c
        n = len(data)
        c = 2
        # Inicializar centros
        old = np.empty(c, dtype=object)
        new = np.empty(c, dtype=object)
        for i in range(c):
            v = Utilities.INI_CENTROIDS[i]
            v_array = np.empty(len(v), dtype=float)
            for j in range(len(v)):
                v_array[j] = v[j]
            old[i] = v_array

        # Bucle:
        num_iter = 1
        while True:
            for j in range(n):
                # Calcular y actualizar el centro más próximo
                i = Lloyd.closest_centroid(j, data, old)
                new[i] = old[i] + Utilities.LLOYD_GAMMA * (data[j] - old[i])
            # Mientras que la diferencia de alguno de los centros sea >= tolerancia
            # y no hayamos sobrepasado el nº max de iteraciones
            if Lloyd.check_tolerance(old, new) or num_iter >= Utilities.LLOYD_KMAX:
                break
            else:
                old = new
                num_iter += 1

        return new, num_iter

    # Método que clasifica un ejemplo:
    # · Entrada: <centros_obtenidos, ejemplo>
    # · Acciones: enviar los cálculos a la vista
    # · Salida: <clase>
    @staticmethod
    def classify(view, centroids, example):
        data = []
        sol = -1
        # Calculamos centro más cercano
        min_dist = float('inf')
        for i in range(len(centroids)):
            # Calcular distancia
            dist = Lloyd.dist(example, centroids[i]) ** 2
            data.append([centroids[i], dist])
            if dist < min_dist:
                min_dist = dist
                sol = i
        if sol == 0:
            class_sol = "Iris-setosa"
        else:
            class_sol = "Iris-versicolor"
        # Imprimir info
        view.draw_info(example, sol, min_dist, class_sol, data)
        return class_sol

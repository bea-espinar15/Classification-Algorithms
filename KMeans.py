
#
#   CLASE ALGORITMO K-MEDIAS BORROSO
#   --------------------------------
#   Clase que implementa el algoritmo K-Medias borroso.
#   Actúa como clase estática, sin atributos.
#

import numpy as np
import Utilities


class KMeans:

    # Calcula la distancia euclídea entre dos vectores
    @staticmethod
    def dist(x, v):
        return np.linalg.norm(x - v)

    # Comprueba si se cumple el criterio de finalización
    @staticmethod
    def check_tolerance(old, new):
        for i in range(len(old)):
            if KMeans.dist(new[i], old[i]) >= Utilities.KMEANS_EPS:
                return False
        return True

    # Calcula el nuevo centro i a partir de la matriz de grados
    # de pertenencia y las muestras
    @staticmethod
    def update_centroid(i, u, x):
        num_value = np.zeros(len(x[0]), dtype=float)
        den_value = 0
        for j in range(len(x)):
            num_value += pow(u[i, j], Utilities.KMEANS_B) * x[j]
            den_value += pow(u[i, j], Utilities.KMEANS_B)
        return num_value / den_value

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

        # Bucle
        num_iter = 1
        while True:
            # Calcular matriz de grados de pertenencia
            u = np.empty((c, n), dtype=object)
            acc = np.zeros(n, dtype=float)
            for i in range(c-1):
                for j in range(n):
                    # Calcular numerador
                    num_value = pow(1 / (KMeans.dist(data[j], old[i])**2), 1 / (Utilities.KMEANS_B - 1))
                    # Calcular denominador
                    den_value = 0
                    for r in range(c):
                        den_value += pow(1 / (KMeans.dist(data[j], old[r])**2), 1 / (Utilities.KMEANS_B - 1))
                    # Calculamos grado de pertenencia
                    u[i, j] = num_value / den_value
                    acc[j] += u[i, j]
            # La última fila es la suma de las anteriores
            for j in range(n):
                u[c-1][j] = 1 - acc[j]
            # Actualizar centros
            for i in range(c):
                new[i] = KMeans.update_centroid(i, u, data)
            # Iteramos mientras que la diferencia de alguno de los centros sea >= tolerancia
            if KMeans.check_tolerance(old, new):
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
        max_degree = 0
        for i in range(len(centroids)):
            # Calcular distancia
            dist = KMeans.dist(example, centroids[i])**2
            # Calcular grado pertenencia
            # Numerador
            num_value = pow(1 / (KMeans.dist(example, centroids[i]) ** 2), 1 / (Utilities.KMEANS_B - 1))
            # Calcular denominador
            den_value = 0
            for r in range(len(centroids)):
                den_value += pow(1 / (KMeans.dist(example, centroids[r]) ** 2), 1 / (Utilities.KMEANS_B - 1))
            max_degree = max(max_degree, num_value / den_value)
            data.append([centroids[i], dist, num_value / den_value])
            if dist < min_dist:
                min_dist = dist
                sol = i
        if sol == 0: class_sol = "Iris-setosa"
        else: class_sol = "Iris-versicolor"
        # Imprimir info
        data.append(max_degree)
        view.draw_info(example, sol, min_dist, class_sol, data)
        return class_sol

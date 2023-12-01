
#
#   CLASE ALGORITMO BAYES
#   ---------------------
#   Clase que implementa el algoritmo de Bayes.
#   Actúa como clase estática, sin atributos.
#

import numpy as np


class Bayes:

    # Calcula la media de una clase, que tiene las muestras <x[]>
    @staticmethod
    def calc_mean(x):
        acc = np.zeros(len(x[0]))
        for d in x:
            acc = acc + d
        return (1 / len(x)) * acc

    # Calcula la matriz de covarianza de la clase que tiene las muestras <x[]>
    # y tiene como media <m>
    @staticmethod
    def calc_matrix(x, m):
        dims = len(x[0])
        acc = np.zeros((dims, dims), dtype=float)
        for d in x:
            subs = (d - m).reshape((4, 1))  # Convertimos de vector a matriz
            acc += subs @ subs.transpose()
        return (1 / len(x)) * acc

    # Método que ejecuta el algoritmo:
    # · Entrada -> <muestra_clase1, muestra_clase2>
    # · Salida -> <medias, matrices_covarianza>
    @staticmethod
    def execute(data_set, data_ver):
        # Media set
        m1 = Bayes.calc_mean(data_set)
        # Media ver
        m2 = Bayes.calc_mean(data_ver)
        # Matriz set
        c1 = Bayes.calc_matrix(data_set, m1)
        # Matriz ver
        c2 = Bayes.calc_matrix(data_ver, m2)
        m = [m1, m2]
        c = [c1, c2]
        return m, c

    # Método que clasifica un ejemplo:
    # · Entrada: <medias, matrices_covarianza, ejemplo>
    # · Acciones: enviar los cálculos a la vista
    # · Salida: <clase>
    @staticmethod
    def classify(view, means, matrices, example):
        data = []
        sol = -1
        # Calculamos centro más cercano
        min_dist = float('inf')
        for i in range(len(means)):
            aux = example - means[i]
            # (x-m) * inversa(c) * (x-m)^t
            dist = aux @ np.linalg.inv(matrices[i])
            dist = dist @ aux.copy().transpose()
            data.append([means[i], matrices[i], aux, dist])
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

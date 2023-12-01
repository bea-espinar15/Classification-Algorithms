
#
#   CLASE MAIN
#   ----------
#   Clase que inicia la aplicación y lee los datos de entrada
#

import numpy as np
from MainWindow import MainWindow


# Crea un array numpy a partir del array []
def create_array(m):
    size = len(m)
    data = np.empty(size, dtype=float)
    for i in range(size):
        data[i] = m[i]
    return data


# Lee el ejemplo del fichero pasado por parámetro
def read_example(file):
    example_file = open(file, 'r')
    example_file = example_file.read()
    example = []
    while ',' in example_file:
        example.append(example_file.split(',', 1)[0])
        example_file = example_file.split(',', 1)[1]
    return create_array(example)


def main():

    # Leer datos del fichero
    data_file = open('input_files/Iris2Clases.txt', 'r')
    lines = data_file.readlines()
    data_set = []
    data_ver = []
    for line in lines:
        line = line.strip()
        aux = []
        while ',' in line:
            aux.append(line.split(',', 1)[0])
            line = line.split(',', 1)[1]
        class_data = line.strip()
        if class_data == "Iris-setosa":
            data_set.append(create_array(aux))
        else:
            data_ver.append(create_array(aux))

    # Leer ejemplos
    examples = [read_example('input_files/TestIris01.txt'),
                read_example('input_files/TestIris02.txt'),
                read_example('input_files/TestIris03.txt')]

    # Iniciamos la aplicación
    MainWindow(data_set, data_ver, examples)


main()

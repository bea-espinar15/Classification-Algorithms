
#
#   CLASE VISTA ALGORITMOS
#   ----------------------
#   Clase que dibuja el panel derecho en función del algoritmo a
#   ejecutar. Atributos:
#   · alg = algoritmo que se va a ejecutar y que define el contenido del panel
#   · data_set = matriz de los datos de entrada correspondientes a Iris-setosa
#   · data_ver = matriz de los datos de entrada correspondientes a Iris-versicolor
#   · examples = array de los 3 ejemplos a clasificar
#   · centroids = centros obtenidos por el algoritmo (None si es Bayes)
#   · means = medias obtenidas por el algoritmo (None si no es Bayes)
#   · matrices = matrices de covarianza obtenidas por el algoritmo (None si no es Bayes)
#
#   · frame = frame padre donde se dibuja este panel
#   · content_frame = frame donde se imprime el algoritmo
#   · params_frame = frame donde se escriben los parámetros iniciales en función del algoritmo
#   · centroids_frame = frame donde se escriben los centros obtenidos por K-medias/Lloyd
#   · means_frame = frame donde se escriben las medias obtenidas por Bayes
#   · matrix_frame = frame donde se escriben las matrices de covarianza
#   · examples_frame = frame donde se clasifican los ejemplos
#   · check_frame = frame donde se coloca el calculus_frame
#   · calculus_frame = frame donde se muestra los cálculos realizados para clasificar
#
#   · execute_button = botón para ejecutar el algoritmo
#   · iter_label = label donde se escriben las iteraciones realizadas por K-medias/Lloyd
#   · example_button1, 2 y 3 = botones para clasificar cada uno de los ejemplos
#   · example_class_label1, 2 y 3 = labels donde se escribe la clase a la que pertenece cada ejemplo
#

import numpy as np
import tkinter as tk
import Utilities
from KMeans import KMeans
from Lloyd import Lloyd
from Bayes import Bayes


class AlgorithmView:

    # Constructor:
    def __init__(self, frame, alg, data_set, data_ver, examples):
        self.alg = alg
        self.data_set = data_set
        self.data_ver = data_ver
        self.examples = examples
        self.centroids = None
        self.means = None
        self.matrices = None

        self.frame = frame
        self.content_frame = None
        self.params_frame = None
        self.centroids_frame = None
        self.means_frame = None
        self.matrix_frame = None
        self.examples_frame = None
        self.check_frame = None
        self.calculus_frame = None

        self.execute_button = None
        self.iter_label = None
        self.example_button1 = None
        self.example_class_label1 = None
        self.example_button2 = None
        self.example_class_label2 = None
        self.example_button3 = None
        self.example_class_label3 = None

        self.init_gui()

    # Métodos privados:

    # ----- Métodos para generar texto -----

    # Crea texto de label para un ejemplo
    @staticmethod
    def create_text(example):
        text = " "
        for e in example:
            text = text + str(e) + " | "
        return text[:-2]

    # Convierte un vector en texto ajustando 2 decimales
    @staticmethod
    def create_coord(coord):
        text = "("
        for i in coord:
            text += "{:.2f}, ".format(i)
        return text[:-2] + ")"

    # Crea texto de cálculos en clasificación Bayes para la clase index
    def text_bayes(self, index, data):
        text_info = str(index) + ". Siendo\n"
        text_info = text_info + "M" + str(index) + " = " + self.create_coord(data[0]) + '\n'
        text_info = text_info + "C" + str(index) + " = " + np.array2string(data[1].copy().round(3), separator=', ')
        text_info = text_info + "\n\nXk - M" + str(index) + " = " + self.create_coord(data[2]) + '\n'
        text_info = text_info + "Dm(Xk, M" + str(index) + "/C" + str(index) + ") = (Xk - M" + str(index)
        text_info = text_info + ") * I * (Xk - M" + str(index) + ")^t = " + "{:.3f}".format(data[3])
        return text_info

    # Crea texto de cálculos de distancias
    def text_dist(self, index, example, data):
        text_info = "· ||Xk - V" + str(index) + "||^2 =\n= ||" + self.create_coord(example) + " - "
        text_info = text_info + self.create_coord(data[0]) + "||^2 =\n= " + "{:.3f}".format(data[1]) + '\n'
        return text_info

    # ----- Métodos para imprimir resultados -----

    # Imprime los resultados del algoritmo de Bayes
    def print_bayes(self):
        # ------- MEDIAS -------
        means_labels = []
        for i in range(len(self.means)):
            mean_text = "M" + str(i + 1) + " = " + AlgorithmView.create_coord(self.means[i])
            means_labels.append(tk.Label(self.means_frame, bg=self.means_frame["bg"], text=mean_text,
                                         font=Utilities.FONT_BIGGER))
            means_labels[i].grid(row=0, column=i, padx=20, pady=5)
        # ------- MATRICES DE COVARIANZA -------
        matrix_labels = []
        for i in range(len(self.matrices)):
            matrix_text = "C" + str(i + 1) + " = " + np.array2string(self.matrices[i].copy().round(3),
                                                                     separator=', ')
            matrix_labels.append(tk.Label(self.matrix_frame, bg=self.matrix_frame["bg"], text=matrix_text,
                                          font=Utilities.FONT_BIGGER))
            matrix_labels[i].grid(row=0, column=i, padx=20, pady=5)

    # Imprime los resultados del algoritmo de K-medias/Lloyd
    def print_general(self, num_iter):
        # ------- CENTROS -------
        center_labels = []
        for i in range(len(self.centroids)):
            center_text = "V" + str(i + 1) + " = " + AlgorithmView.create_coord(self.centroids[i])
            center_labels.append(tk.Label(self.centroids_frame, bg=self.centroids_frame["bg"], text=center_text,font=Utilities.FONT_BIGGER))
            center_labels[i].grid(row=i, column=0, padx=20)
        # ------- NUM ITERACIONES -------
        self.iter_label.config(text=str(num_iter))

    # ----- Métodos para funcionalidad botones -----

    # Funcionalidad clasificar el ejemplo i
    def classify(self, i):
        self.calculus_frame.destroy()
        self.create_calculus()
        # Clasificar ejemplo
        if self.alg == "Bayes":
            sol_class = Bayes.classify(self, self.means, self.matrices, self.examples[i])
        elif self.alg == "Lloyd":
            sol_class = Lloyd.classify(self, self.centroids, self.examples[i])
        else:  # K-Medias
            sol_class = KMeans.classify(self, self.centroids, self.examples[i])
        # Activar/desactivar botones de clasificación
        if i == 0:
            self.example_button1.config(state="disabled", bg=Utilities.GRAY)
            self.example_button2.config(state="normal", bg=Utilities.BLUE)
            self.example_button3.config(state="normal", bg=Utilities.BLUE)
            self.example_class_label1.config(text=sol_class)
            self.example_class_label2.config(text="")
            self.example_class_label3.config(text="")
        elif i == 1:
            self.example_button1.config(state="normal", bg=Utilities.BLUE)
            self.example_button2.config(state="disabled", bg=Utilities.GRAY)
            self.example_button3.config(state="normal", bg=Utilities.BLUE)
            self.example_class_label1.config(text="")
            self.example_class_label2.config(text=sol_class)
            self.example_class_label3.config(text="")
        else:
            self.example_button1.config(state="normal", bg=Utilities.BLUE)
            self.example_button2.config(state="normal", bg=Utilities.BLUE)
            self.example_button3.config(state="disabled", bg=Utilities.GRAY)
            self.example_class_label1.config(text="")
            self.example_class_label2.config(text="")
            self.example_class_label3.config(text=sol_class)

    # Funcionalidad ejecutar algoritmo
    def execute(self):
        # Desactivar botón ejecutar
        self.execute_button.config(state="disabled")
        # Ejecutar algoritmo e imprimir resultados
        if self.alg == "Bayes":
            self.means, self.matrices = Bayes.execute(self.data_set, self.data_ver)
            self.print_bayes()
            pass
        elif self.alg == "Lloyd":
            self.centroids, num_iter = Lloyd.execute(self.data_set, self.data_ver)
            self.print_general(num_iter)
        else:  # K-Medias
            self.centroids, num_iter = KMeans.execute(self.data_set, self.data_ver)
            self.print_general(num_iter)
        # Activar botones clasificación
        self.example_button1.config(state="normal", bg=Utilities.BLUE)
        self.example_button2.config(state="normal", bg=Utilities.BLUE)
        self.example_button3.config(state="normal", bg=Utilities.BLUE)

    # ----- Métodos para crear elementos comunes -----

    # Crear frame de los cálculos
    def create_calculus(self):
        self.calculus_frame = tk.Frame(self.check_frame, bg=self.check_frame["bg"])
        self.calculus_frame.pack(side=tk.TOP, expand=False, fill=tk.Y, pady=10)

    # Crear botón ejecutar
    def create_button(self, frame):
        self.execute_button = tk.Button(frame, text="EJECUTAR", width=10, height=2, font=Utilities.FONT_BUTTON,
                                        bg=Utilities.LIGHT_BLUE, command=self.execute)
        self.execute_button.pack(side=tk.TOP, pady=10, anchor="w")
        self.execute_button.config(bd=3, relief=tk.GROOVE)

    # Rellena el frame de un ejemplo, indicado en ex_index
    def fill_frame(self, frame, ex_index):
        # Ejemplo
        text = AlgorithmView.create_text(self.examples[ex_index])
        label = tk.Label(frame, text=text, font=Utilities.FONT_TEXT)
        label.config(highlightthickness=2, highlightbackground=Utilities.BLACK, bd=2, bg=frame["bg"])
        label.pack(side=tk.LEFT, padx=10, pady=5, anchor="w")
        # Botón
        button = tk.Button(frame, text="", width=2, height=1, bg=Utilities.GRAY,
                           command=lambda: self.classify(ex_index))
        button.pack(side=tk.LEFT)
        button.config(bd=2, relief=tk.GROOVE, state="disabled")
        # Clase
        class_label = tk.Label(frame, font=Utilities.FONT_TEXT, width=18)
        class_label.config(highlightthickness=2, highlightbackground=Utilities.BLACK, bd=2, bg=frame["bg"])
        class_label.pack(side=tk.LEFT, padx=10, pady=5, anchor="w")
        return button, class_label

    # Panel ejemplos:
    def create_examples(self):
        # Ejemplo 1
        example1_frame = tk.Frame(self.examples_frame, bg=self.examples_frame["bg"])
        example1_frame.pack(side=tk.TOP, expand=False, fill=tk.BOTH, padx=10, pady=10)
        self.example_button1, self.example_class_label1 = self.fill_frame(example1_frame, 0)
        # Ejemplo 2
        example2_frame = tk.Frame(self.examples_frame, bg=self.examples_frame["bg"])
        example2_frame.pack(side=tk.TOP, expand=False, fill=tk.BOTH, padx=10)
        self.example_button2, self.example_class_label2 = self.fill_frame(example2_frame, 1)
        # Ejemplo 3
        example3_frame = tk.Frame(self.examples_frame, bg=self.examples_frame["bg"])
        example3_frame.pack(side=tk.TOP, expand=False, fill=tk.BOTH, padx=10, pady=10)
        self.example_button3, self.example_class_label3 = self.fill_frame(example3_frame, 2)

    # ----- BAYES -----

    # Rellena el panel para el algoritmo de Bayes
    def create_bayes_view(self):
        # -------- Botón ejecutar ----------
        button_frame = tk.Frame(self.content_frame, bg=self.content_frame["bg"])
        button_frame.pack(side=tk.TOP, expand=False, fill=tk.BOTH)
        # Botón
        self.create_button(button_frame)
        # -------- Medias ----------
        means_general_frame = tk.Frame(self.content_frame, bg=self.content_frame["bg"], highlightthickness=5,
                                    highlightbackground=Utilities.LIGHT_BLUE)
        means_general_frame.pack(side=tk.TOP, expand=False, fill=tk.X, pady=10)
        # Título
        means_title_label = tk.Label(means_general_frame, text="Medias obtenidas",
                                          bg=means_general_frame["bg"], font=Utilities.FONT_SUBTITLE)
        means_title_label.pack(side=tk.TOP, padx=20, pady=10, anchor="w")
        # Contenido
        self.means_frame = tk.Frame(means_general_frame, bg=means_general_frame["bg"], height=35)
        self.means_frame.pack(side=tk.TOP, anchor="w")
        # Borde inferior
        empty_frame = tk.Frame(means_general_frame, bg=means_general_frame["bg"], height=15)
        empty_frame.pack(side=tk.TOP, expand=False, fill=tk.X)
        # -------- Matrices de covarianza ----------
        matrix_general_frame = tk.Frame(self.content_frame, bg=self.content_frame["bg"], highlightthickness=5,
                                     highlightbackground=Utilities.LIGHT_BLUE)
        matrix_general_frame.pack(side=tk.TOP, expand=True, fill=tk.BOTH, pady=10)
        # Título
        matrix_title_label = tk.Label(matrix_general_frame, text="Matrices de covarianza",
                                     bg=matrix_general_frame["bg"], font=Utilities.FONT_SUBTITLE)
        matrix_title_label.pack(side=tk.TOP, padx=20, pady=10, anchor="w")
        # Contenido
        self.matrix_frame = tk.Frame(matrix_general_frame, bg=matrix_general_frame["bg"])
        self.matrix_frame.pack(side=tk.TOP, anchor="w")

    # ----- K-MEDIAS O LLOYD -----

    # Imprime los parámetros iniciales para el algoritmo de Lloyd
    def lloyd_params(self):
        # Tolerancia
        tolerance = "Tolerancia = " + str(Utilities.LLOYD_EPS)
        tolerance_label = tk.Label(self.params_frame, text=tolerance, font=Utilities.FONT_BIGGER,
                                   bg=self.params_frame["bg"])
        tolerance_label.grid(row=0, column=0, sticky="w")
        # Máximo iteraciones
        kmax = "Número máximo de iteraciones = " + str(Utilities.LLOYD_KMAX)
        kmax_label = tk.Label(self.params_frame, text=kmax, font=Utilities.FONT_BIGGER,
                               bg=self.params_frame["bg"])
        kmax_label.grid(row=1, column=0, pady=5)
        # Razón de aprendizaje
        gamma = "Razón de aprendizaje = " + str(Utilities.LLOYD_GAMMA)
        gamma_label = tk.Label(self.params_frame, text=gamma, font=Utilities.FONT_BIGGER,
                              bg=self.params_frame["bg"])
        gamma_label.grid(row=2, column=0, sticky="w")
        # Centro 1
        centroid1 = "V1 = " + AlgorithmView.create_coord(Utilities.INI_CENTROIDS[0])
        centroid1_label = tk.Label(self.params_frame, text=centroid1, font=Utilities.FONT_BIGGER,
                                   bg=self.params_frame["bg"])
        centroid1_label.grid(row=0, column=1, padx=60)
        # Centro 2
        centroid2 = "V2 = " + AlgorithmView.create_coord(Utilities.INI_CENTROIDS[1])
        centroid2_label = tk.Label(self.params_frame, text=centroid2, font=Utilities.FONT_BIGGER,
                                   bg=self.params_frame["bg"])
        centroid2_label.grid(row=1, column=1, pady=5, padx=60)

    # Imprime los parámetros iniciales para el algoritmo de K-medias borroso
    def kmeans_params(self):
        # Tolerancia
        tolerance = "Tolerancia = " + str(Utilities.KMEANS_EPS)
        tolerance_label = tk.Label(self.params_frame, text=tolerance, font=Utilities.FONT_BIGGER,
                                   bg=self.params_frame["bg"])
        tolerance_label.grid(row=0, column=0, sticky="w")
        # Peso exponencial
        weigh = "Peso exponencial = " + str(Utilities.KMEANS_B)
        weigh_label = tk.Label(self.params_frame, text=weigh, font=Utilities.FONT_BIGGER,
                               bg=self.params_frame["bg"])
        weigh_label.grid(row=1, column=0, pady=5)
        # Centro 1
        centroid1 = "V1 = " + AlgorithmView.create_coord(Utilities.INI_CENTROIDS[0])
        centroid1_label = tk.Label(self.params_frame, text=centroid1, font=Utilities.FONT_BIGGER,
                                   bg=self.params_frame["bg"])
        centroid1_label.grid(row=0, column=1, padx=60)
        # Centro 2
        centroid2 = "V2 = " + AlgorithmView.create_coord(Utilities.INI_CENTROIDS[1])
        centroid2_label = tk.Label(self.params_frame, text=centroid2, font=Utilities.FONT_BIGGER,
                                   bg=self.params_frame["bg"])
        centroid2_label.grid(row=1, column=1, pady=5, padx=60)

    # Rellena el panel para el algoritmo K-Medias o Lloyd
    def create_general_view(self):
        # -------- Parámetros iniciales ----------
        ini_params_frame = tk.Frame(self.content_frame, bg=self.content_frame["bg"], highlightthickness=5,
                                         highlightbackground=Utilities.LIGHT_BLUE)
        ini_params_frame.pack(side=tk.TOP, expand=False, fill=tk.X, pady=10)
        # Título
        ini_params_title_label = tk.Label(ini_params_frame, text="Parámetros iniciales",
                                          bg=ini_params_frame["bg"], font=Utilities.FONT_SUBTITLE)
        ini_params_title_label.pack(side=tk.TOP, padx=20, pady=10, anchor="w")
        # Contenido
        self.params_frame = tk.Frame(ini_params_frame, bg=ini_params_frame["bg"])
        self.params_frame.pack(side=tk.TOP, expand=False, fill=tk.X, padx=20, pady=10)
        if self.alg == "Lloyd": self.lloyd_params()
        else: self.kmeans_params()
        # -------- Botón ejecutar ----------
        button_frame = tk.Frame(self.content_frame, bg=self.content_frame["bg"])
        button_frame.pack(side=tk.TOP, expand=False, fill=tk.BOTH)
        # Botón
        self.create_button(button_frame)
        # -------- Resultado ----------
        sol_frame = tk.Frame(self.content_frame, bg=self.content_frame["bg"])
        sol_frame.pack(side=tk.TOP, expand=True, fill=tk.BOTH, pady=10)
        # --- Centros ---
        centroids_general_frame = tk.Frame(sol_frame, bg=self.content_frame["bg"], highlightthickness=5,
                                   highlightbackground=Utilities.LIGHT_BLUE)
        centroids_general_frame.pack(side=tk.LEFT, expand=True, fill=tk.BOTH, anchor="w")
        # Título
        centroids_title_label = tk.Label(centroids_general_frame, text="Centros obtenidos",
                                         bg=centroids_general_frame["bg"], font=Utilities.FONT_SUBTITLE)
        centroids_title_label.pack(side=tk.TOP, padx=20, pady=10, anchor="w")
        # Centros
        self.centroids_frame = tk.Frame(centroids_general_frame, bg=centroids_general_frame["bg"])
        self.centroids_frame.pack(side=tk.TOP, pady=10, anchor="w")
        # --- Iteraciones ---
        iter_frame = tk.Frame(sol_frame, bg=self.content_frame["bg"], highlightthickness=5, height=50,
                              highlightbackground=Utilities.LIGHT_BLUE, width=200)
        iter_frame.pack(side=tk.LEFT, padx=60, anchor="ne")
        # Título
        iter_title_label = tk.Label(iter_frame, text="Iteraciones realizadas:",
                                    bg=iter_frame["bg"], font=Utilities.FONT_TEXT_BOLD)
        iter_title_label.pack(side=tk.LEFT, padx=5, pady=10, anchor="w")
        # Centros
        self.iter_label = tk.Label(iter_frame, bg=iter_frame["bg"], font=Utilities.FONT_TEXT)
        self.iter_label.pack(side=tk.LEFT, pady=10, anchor="w")
        # Borde izquierdo
        empty_frame = tk.Frame(iter_frame, bg=iter_frame["bg"], width=10)
        empty_frame.pack(side=tk.LEFT, expand=False, fill=tk.Y)

    # ----- Principal -----

    # Método principal: inicializa la GUI
    def init_gui(self):

        # Label título
        title_label = tk.Label(self.frame, text=self.alg, font=Utilities.FONT_TITLE)
        title_label.config(highlightthickness=0, bd=0, bg=self.frame["bg"])
        title_label.pack(side=tk.TOP, padx=20, pady=30, anchor="w")

        # Panel central
        center_frame = tk.Frame(self.frame, bg=self.frame["bg"])
        center_frame.pack(side=tk.TOP, expand=True, fill=tk.BOTH)
        # Panel algoritmo
        alg_frame = tk.Frame(center_frame, bg=center_frame["bg"])
        alg_frame.pack(side=tk.LEFT, expand=True, fill=tk.BOTH, padx=20, pady=10)
        # Panel contenido
        self.content_frame = tk.Frame(alg_frame, bg=alg_frame["bg"])
        self.content_frame.pack(side=tk.TOP, expand=True, fill=tk.BOTH)
        if self.alg == "Bayes": self.create_bayes_view()
        else: self.create_general_view()
        # Panel clasificación
        self.examples_frame = tk.Frame(alg_frame, bg=alg_frame["bg"], highlightthickness=5,
                                       highlightbackground=Utilities.LIGHT_BLUE)
        self.examples_frame.pack(side=tk.TOP, expand=False, fill=tk.BOTH, pady=10)
        examples_label = tk.Label(self.examples_frame, text="Clasificación", font=Utilities.FONT_SUBTITLE)
        examples_label.config(highlightthickness=0, bd=0, bg=self.examples_frame["bg"])
        examples_label.pack(side=tk.TOP, padx=20, pady=10, anchor="w")
        self.create_examples()

        # Panel comprobación
        self.check_frame = tk.Frame(center_frame, bg=center_frame["bg"], highlightthickness=5,
                               highlightbackground=Utilities.LIGHT_BLUE)
        self.check_frame.pack(side=tk.LEFT, expand=False, fill=tk.Y, padx=20, pady=20)
        # Label subtítulo
        calculus_label = tk.Label(self.check_frame, text="Cálculo de pertenencia", font=Utilities.FONT_SUBTITLE)
        calculus_label.config(highlightthickness=0, bd=0, bg=self.check_frame["bg"])
        calculus_label.pack(side=tk.TOP, padx=40, pady=10, anchor="w")
        # Contenido
        self.create_calculus()

        # Borde inferior
        empty_frame = tk.Frame(self.frame, bg=self.frame["bg"], height=70)
        empty_frame.pack(side=tk.TOP, expand=False, fill=tk.X)

    # Métodos públicos:

    # Imprime los cálculos realizados para clasificar el ejemplo
    def draw_info(self, example, i_sol, dist_sol, class_sol, data):
        # Crear texto
        text_info = "Xk = " + self.create_coord(example) + "\n\nCalculamos distancias:\n"
        # Bayes
        if self.alg == "Bayes":
            for i in range(len(data)):
                text_info = text_info + self.text_bayes(i+1, data[i]) + '\n\n'
        # Lloyd o K-Medias
        else:
            for i in range(2):
                text_info = text_info + self.text_dist(i+1, example, data[i])
        text_info = text_info + "\n-> Menor distancia a V" + str(i_sol+1) + " (" + "{:.3f}".format(dist_sol) + ") => Xk pertenece a " + class_sol
        if self.alg == "K-medias borroso":
            text_info = text_info + "\n\nCálculo grados pertenencia:\n"
            for i in range(len(data)-1):
                text_info = text_info + "- P(V" + str(i+1) + "/Xk) = " + "{:.3f}".format(data[i][2]) + '\n'
            text_info = text_info + "\n-> Mayor grado de pertenencia (" + "{:.3f}".format(data[-1]) + ") a la clase " + str(i_sol+1)
            text_info = text_info + "\n=> Xk pertenece a " + class_sol

        # Crear label
        label = tk.Label(self.calculus_frame, bg=self.calculus_frame["bg"], text=text_info, font=Utilities.FONT_TEXT, justify="left")
        label.pack(side=tk.TOP, padx=10)

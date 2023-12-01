
#
#   CLASE MAIN WINDOW
#   -----------------
#   Clase que dibuja la interfaz principal. Atributos:
#   · data_set = matriz de los datos de entrada correspondientes a Iris-setosa
#   · data_ver = matriz de los datos de entrada correspondientes a Iris-versicolor
#   · examples = array de los 3 ejemplos a clasificar
#   · main_window = ventana principal, objeto raíz de la GUI
#   · main_frame = frame principal de la aplicación
#   · content_frame = frame del contenido, compuesto por left_frame y right_frame
#   · right_frame = frame dinámico que depende del algoritmo a ejecutar
#

import tkinter as tk
import Utilities
from Table import Table
from AlgorithmView import AlgorithmView


class MainWindow:

    # Constructor:
    def __init__(self, data_set, data_ver, examples):
        self.data_set = data_set
        self.data_ver = data_ver
        self.examples = examples

        self.main_window = tk.Tk()
        self.main_frame = None
        self.content_frame = None
        self.right_frame = None

        self.init_gui()

    # Métodos privados:

    # Crea el frame derecho de 0
    def create_right_frame(self):
        self.right_frame = tk.Frame(self.content_frame, bg=self.content_frame["bg"])
        self.right_frame.pack(side=tk.LEFT, expand=True, fill=tk.BOTH, padx=40)

    # Funcionalidad botones:
    # ----------------------
    def button(self, alg):
        self.right_frame.destroy()
        self.create_right_frame()
        AlgorithmView(self.right_frame, alg, self.data_set, self.data_ver, self.examples)

    # Pintar paneles:
    # ---------------

    # Inicializar (pintar) el header
    def init_header(self):
        header_frame = tk.Frame(self.main_frame, height=80, bg=Utilities.LIGHT_BLUE)
        header_frame.pack(fill=tk.X)
        # Label título
        title_label = tk.Label(header_frame, text="Métodos de Clasificación", font=Utilities.FONT_HEADER)
        title_label.config(highlightthickness=0, bd=0, bg=header_frame["bg"])
        title_label.pack(pady=20)

    # Inicializar (pintar) el panel de contenido principal
    def init_content(self):
        self.content_frame = tk.Frame(self.main_frame, bg=Utilities.WHITE)
        self.content_frame.pack(expand=True, fill=tk.BOTH)

        # -------------- LEFT -------------
        left_frame = tk.Frame(self.content_frame, bg=self.content_frame["bg"])
        left_frame.pack(side=tk.LEFT, expand=False, fill=tk.BOTH)
        # Label título
        label_input_frame = tk.Frame(left_frame, bg=left_frame["bg"])
        label_input_frame.pack(side=tk.TOP, expand=False, fill=tk.BOTH)
        input_label = tk.Label(label_input_frame, text="Datos de entrada", font=Utilities.FONT_SUBTITLE)
        input_label.config(highlightthickness=0, bd=0, bg=label_input_frame["bg"])
        input_label.pack(pady=30)
        # Tabla Iris-Setosa
        table1_frame = tk.Frame(left_frame, bg=left_frame["bg"], highlightthickness=2, highlightbackground=Utilities.BLACK)
        table1_frame.configure(borderwidth=1, relief="solid")
        table1_frame.pack(side=tk.TOP, expand=False, fill=tk.BOTH, padx=60)
        Table("Iris-setosa", self.data_set, table1_frame)
        # Tabla Iris-Versicolor
        table2_frame = tk.Frame(left_frame, bg=left_frame["bg"], highlightthickness=2, highlightbackground=Utilities.BLACK)
        table2_frame.configure(borderwidth=1, relief="solid")
        table2_frame.pack(side=tk.TOP, expand=False, fill=tk.BOTH, padx=60, pady=20)
        Table("Iris-versicolor", self.data_ver, table2_frame)
        # Botones
        buttons_frame = tk.Frame(left_frame, bg=left_frame["bg"])
        buttons_frame.pack(side=tk.TOP, expand=True, fill=tk.BOTH, padx=60, pady=20)
        # Botón Bayes
        bayes_button = tk.Button(buttons_frame, text="BAYES", width=10, height=2, font=Utilities.FONT_BUTTON,
                                 bg=Utilities.LIGHT_BLUE, command=lambda: self.button("Bayes"))
        bayes_button.place(x=50, y=0)
        bayes_button.config(bd=3, relief=tk.GROOVE)
        # Botón Lloyd
        lloyd_button = tk.Button(buttons_frame, text="LLOYD", width=10, height=2, font=Utilities.FONT_BUTTON,
                                 bg=Utilities.LIGHT_BLUE, command=lambda: self.button("Lloyd"))
        lloyd_button.place(x=240, y=0)
        lloyd_button.config(bd=3, relief=tk.GROOVE)
        # Botón K-Means
        kmeans_button = tk.Button(buttons_frame, text="K-MEDIAS", width=12, height=2, font=Utilities.FONT_BUTTON,
                                  bg=Utilities.LIGHT_BLUE, command=lambda: self.button("K-medias borroso"))
        kmeans_button.place(x=140, y=100)
        kmeans_button.config(bd=3, relief=tk.GROOVE)
        kmeans_button.config(bd=3, relief=tk.GROOVE)
        # Borde del panel
        border = tk.Frame(self.content_frame, height=2, bg=Utilities.GRAY)
        border.pack(side=tk.LEFT, fill=tk.Y)

        # -------------- RIGHT -------------
        self.create_right_frame()

    def init_gui(self):
        self.main_window.title("Métodos de Clasificación")
        self.main_window.geometry(Utilities.DIM)

        # -------------- MAIN ----------------
        self.main_frame = tk.Frame(self.main_window, highlightthickness=2, highlightbackground=Utilities.BLACK)
        self.main_frame.pack(expand=True, fill=tk.BOTH)

        # -------------- HEADER --------------
        self.init_header()
        # Borde frame
        header_border = tk.Frame(self.main_frame, height=2, bg=Utilities.GRAY)
        header_border.pack(fill=tk.X, side=tk.TOP)

        # -------------- CONTENT -------------
        self.init_content()

        self.main_window.mainloop()


#
#   CLASE TABLA
#   -----------
#   Clase que dibuja la tabla de datos de entrada. Atributos:
#   · title = título de la tabla, correspondiente al nombre de la clase
#   · data = datos de la tabla (ejemplos)
#   · frame = frame donde se dibuja la tabla
#


import tkinter as tk
import Utilities


class Table:

    # Constructor:
    def __init__(self, title, data, table_frame):
        self.title = title
        self.data = data
        self.frame = table_frame
        self.init_gui()

    # Métodos privados:

    # Dibuja la tabla
    def init_gui(self):
        # Título de la tabla
        title_frame = tk.Frame(self.frame, bg=Utilities.LIGHT_BLUE)
        title_frame.pack(side=tk.TOP, expand=True, fill=tk.X)
        title = tk.Label(title_frame, text=self.title, font=Utilities.FONT_BUTTON, bg=title_frame["bg"])
        title.pack(pady=5)
        # Borde del frame
        bottom_border = tk.Frame(title_frame, height=2, bg=Utilities.BLACK)
        bottom_border.pack(fill="x")

        # Tabla
        table_frame = tk.Frame(self.frame, bg=self.frame["bg"])
        table_frame.pack(side=tk.TOP, expand=False)
        # Scrollbar
        canvas = tk.Canvas(table_frame, borderwidth=0, highlightthickness=0, bg=table_frame["bg"], height=220)
        data_frame = tk.Frame(canvas, bg=self.frame["bg"])
        scrollbar = tk.Scrollbar(table_frame, orient="vertical", command=canvas.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y, padx=5)
        canvas.configure(yscrollcommand=scrollbar.set)
        canvas.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        # Asociamos frame y scrollbar al canvas
        data_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.create_window((0, 0), window=data_frame, anchor="nw")

        rows = len(self.data)
        cols = len(self.data[0])

        # Pintar valores de la tabla
        for i in range(rows):
            for j in range(cols):
                e = tk.Entry(data_frame, width=13, font=Utilities.FONT_TEXT, justify=tk.CENTER, bg=Utilities.WHITE)
                e.grid(row=i, column=j, sticky="nsew")
                e.insert(tk.END, self.data[i][j])

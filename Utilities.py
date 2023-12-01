
#
#   CLASE UTILITIES
#   ---------------
#   En esta clase se definen constantes utilizadas por el resto de clases
#

# Dimensión de la pantalla
DIM = "1800x800"

# Colores
WHITE = '#FFFFFF'
BLACK = '#000000'
LIGHT_BLUE = '#CAF0F8'
BLUE = '#90E0EF'
GRAY = '#C3C3C3'

# Fuentes de letra
FONT_HEADER = ("consolas", 20)
FONT_TITLE = ("consolas", 30, "underline")
FONT_SUBTITLE = ("consolas", 20, "underline")
FONT_BUTTON = ("consolas", 15)
FONT_TEXT = ("consolas", 10)
FONT_TEXT_BOLD = ("consolas", 10, "bold")
FONT_BIGGER = ("consolas", 13)

# Parámetros iniciales de los algoritmos
INI_CENTROIDS = [[4.6, 3.0, 4.0, 0.0],
                 [6.8, 3.4, 4.6, 0.7]]
KMEANS_EPS = 0.01
KMEANS_B = 2
LLOYD_EPS = 1E-10
LLOYD_KMAX = 10
LLOYD_GAMMA = 0.1

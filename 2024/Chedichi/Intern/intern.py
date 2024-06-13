from PIL import Image
import numpy as np

imagen = Image.open("images/intern.png")
imagen_array = np.array(imagen)

imagen_invertida = Image.eval(imagen, lambda x: 255 - x)

imagen_invertida.save("images/inversed.png")
imagen_invertida.show()

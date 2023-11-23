
import PIL
from PIL import Image
from tkinter.filedialog import *
fl=askopenfilenames()
img = Image.open(fl[0])
img.save("temp/result.jpg", "JPEG", optimize = True, quality = 90)

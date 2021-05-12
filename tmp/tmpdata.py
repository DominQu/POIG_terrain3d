import rasterio
from PIL import Image
import numpy as np

FILE = r'POIG_terrain3d/tmp/Pomorze.tif'
FILEPNG = r'POIG_terrain3d/tmp/randommap.png'

def geotiff_load(filepath=FILE):
    
    img = rasterio.open(filepath)
    img = img.read(1)
    data = np.array(img, dtype=np.float32)
    return data[1000:1070, 900:970]

def png_load(filepath=FILEPNG):
    img = Image.open(filepath)
    data = np.array(img, dtype=np.float32)
    return data[0:100,0:100]

def simple_data():

    data = np.empty((100, 100), dtype=np.float32)
    for i in range(100):
        for j in range(100):
            data[i, j] = (i+j**2)/100
    return data
if __name__ == "__main__":
    img1 = png_load()
    img2 = geotiff_load()
    img3 = simple_data()
    print(img1.shape)
''' module: datareader
    function: read GeoTif file and convert it to numpy array,
'''
import rasterio
from PIL import Image
import numpy as np

def geotiff_load(filepath):
    
    img = rasterio.open(filepath)
    img = img.read(1)
    data = np.array(img, dtype=np.float32)
    data = data/2
    return data

def png_load(filepath):
    img = Image.open(filepath)
    data = np.array(img, dtype=np.float32)
    return data

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
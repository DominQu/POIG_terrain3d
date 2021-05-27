''' module: datareader
    function: load heightmaps and convert them to numpy arrays
'''
import rasterio
from PIL import Image
import numpy as np

def geotiff_load(filepath):
    '''
        Load geotiff file and scale it
        :return ndarray
    '''
    
    img = rasterio.open(filepath)
    img = img.read(1)
    data = np.array(img, dtype=np.float32)
    data = data/2
    return data

def png_load(filepath):
    '''
        Load png file
        :return ndarray
    '''
    img = Image.open(filepath)
    data = np.array(img, dtype=np.float32)
    return data

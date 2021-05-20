''' module: terrain
    function: generate height map,
              apply texture,
              control lighting
    methods: __init__
             generate_terrain
             apply_texture
             set_light
'''
import sys
sys.path.insert(0, '/home/dominik/GitDir/POIG_terrain3d/tmp')
from tmpdata import *

from panda3d.core import GeomVertexFormat
from panda3d.core import GeomVertexData
from panda3d.core import Geom
from panda3d.core import GeomVertexWriter
from panda3d.core import GeomTriangles
from panda3d.core import GeomNode
from panda3d.core import DirectionalLight, PointLight, Spotlight, PerspectiveLens
from panda3d.core import AmbientLight
from panda3d.core import TextureStage
from panda3d.core import LVector3
from panda3d.core import WindowProperties

import numpy as np
import logging

logging.basicConfig(format='%(asctime)s %(message)s', datefmt='%I:%M:%S')

VERTEXMUL = 10

class Terrain():
     
    def __init__(self, parent, terraintype):

        self.parent = parent

        self.demfiles = {
            "mountain": r'dems/agri-small-dem.tif',
            "canyon": r'dems/canyon.png'
        }

        if terraintype == "mountain":
            self.data = geotiff_load(self.demfiles[terraintype])
        elif terraintype == "canyon":
            self.data = png_load(self.demfiles[terraintype])

        self.maxheight = self.data.max()
        self.camera = self.data[0,0]
        self.numrows = self.data.size
        self.datax = self.data.shape[0]
        self.datay = self.data.shape[1]

    def create_terrain(self):
        '''Load height data, create 3D graphics elements, return geometry node'''
        
        logging.warning('start terrain creation')
        self.format = GeomVertexFormat.get_v3n3cpt2()
        self.format = GeomVertexFormat.registerFormat(self.format)

        self.vdata = GeomVertexData('terrain', self.format, Geom.UHStatic)
        self.vdata.setNumRows(self.numrows)

        self.vertex = GeomVertexWriter(self.vdata, 'vertex')
        self.normal = GeomVertexWriter(self.vdata, 'normal')
        self.color = GeomVertexWriter(self.vdata, 'color')
        self.texcoord = GeomVertexWriter(self.vdata, 'texcoord')
        
        self.prim = GeomTriangles(Geom.UHStatic)

        logging.warning('creating veritces')
        #create vertices
        for i in range(self.datax):
            for j in range(self.datay):
                self.vertex.addData3(VERTEXMUL*i, VERTEXMUL*j, self.data[i,j])
                self.texcoord.addData2(i/self.datax, j/self.datay)
                self.color.addData4(1,1,1,1)
        logging.warning('finish creating vertices, start calculating normal vectors')
        #calculate normal vectors for each vertex
        for i in range(self.datax - 1):
            for j in range(self.datay - 1):
                self.normal.addData3(self.calc_normal(startpoint = [i,j,self.data[i,j]], pointa = [i+1,j,self.data[i,j]],pointb = [i,j+1,self.data[i,j]]))
                if j == self.datay - 2:
                    self.normal.addData3(self.calc_normal(startpoint = [i,j,self.data[i,j]], pointa = [i+1,j,self.data[i,j]],pointb = [i,j+1,self.data[i,j]]))
                if i == self.datax - 2:
                    self.normal.addData3(self.calc_normal(startpoint = [i,j,self.data[i,j]], pointa = [i+1,j,self.data[i,j]],pointb = [i,j+1,self.data[i,j]]))

        logging.warning('finish calculating normal vectors')

        #create triangle primitives

        for i in range(self.datax - 1):
            for j in range(self.datay - 1):
                
                index = j + i * self.datay

                self.prim.addVertices(index, index + self.datay, index + self.datay + 1)
                self.prim.addVertices(index, index + self.datay + 1, index + 1)

        logging.warning('after for loops')

        self.geom = Geom(self.vdata)

        self.geom.addPrimitive(self.prim)

        node = GeomNode('gnode')
        node.addGeom(self.geom)

        return node

    def calc_normal(self, startpoint, pointa, pointb):
        '''Calculate normal vector for a given point and normalize it'''

        vector_a = np.array([pointa[0] - startpoint[0],pointa[1] - startpoint[1],pointa[2] - startpoint[2]])
        vector_b = np.array([pointb[0] - startpoint[0],pointb[1] - startpoint[1],pointb[2] - startpoint[2]])
        x = vector_a[1]*vector_b[2] - vector_a[2]*vector_b[1]
        y = vector_a[2]*vector_b[0] - vector_a[0]*vector_b[2]
        z = vector_a[0]*vector_b[1] - vector_a[1]*vector_b[0]
        vector = LVector3(x,y,z)
        vector.normalize()
        return vector

if __name__ == "__main__":
    from direct.showbase.ShowBase import ShowBase

    class App(ShowBase):

        def __init__(self):

            ShowBase.__init__(self)
            self.terrain = Terrain(self.render, "mountain")
            terrain_node = self.terrain.create_terrain()
            self.terrainNodePath = self.render.attachNewNode(terrain_node)

    app = App()
    app.run()
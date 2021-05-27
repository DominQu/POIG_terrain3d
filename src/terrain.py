''' module: terrain
    function: generate height map
    methods: __init__
             generate_terrain
             calc_normal
'''
from datareader import *

from panda3d.core import GeomVertexFormat
from panda3d.core import GeomVertexData
from panda3d.core import Geom
from panda3d.core import GeomVertexWriter
from panda3d.core import GeomTriangles
from panda3d.core import GeomNode
from panda3d.core import LVector3

import numpy as np
import logging

logging.basicConfig(format='%(asctime)s %(message)s', datefmt='%I:%M:%S')

VERTEXMUL = 10   # Distance between vertices

class Terrain():
     
    def __init__(self, terraintype):

        self.demfiles = {
            "mountain": r'dems/agri-small-dem.tif',
            "canyon": r'dems/canyon.png'
        }

        if terraintype == "mountain":
            self.data = geotiff_load(self.demfiles[terraintype])
        elif terraintype == "canyon":
            self.data = png_load(self.demfiles[terraintype])

        self.maxheight = self.data.max()
        self.numrows = self.data.size
        self.datax = self.data.shape[0]    #number of elements on 0th axis of the data ndarray
        self.datay = self.data.shape[1]    #number of elements on 1st axis of the data ndarray

    def create_terrain(self):
        '''
            Create 3D graphics elements
            :return node
        '''
        
        # Panda3D specific code for primitive generation
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
                # special case for last row and last column
                if j == self.datay - 2:
                    self.normal.addData3(self.calc_normal(startpoint = [i,j,self.data[i,j]], pointa = [i+1,j,self.data[i,j]],pointb = [i,j+1,self.data[i,j]]))
                if i == self.datax - 2:
                    self.normal.addData3(self.calc_normal(startpoint = [i,j,self.data[i,j]], pointa = [i+1,j,self.data[i,j]],pointb = [i,j+1,self.data[i,j]]))

        logging.warning('finish calculating normal vectors, start creating primitives')

        #create triangle primitives

        for i in range(self.datax - 1):
            for j in range(self.datay - 1):
                
                index = j + i * self.datay

                self.prim.addVertices(index, index + self.datay, index + self.datay + 1)
                self.prim.addVertices(index, index + self.datay + 1, index + 1)

        logging.warning('adding primitives to the geometry object')

        self.geom = Geom(self.vdata)
        self.geom.addPrimitive(self.prim)

        node = GeomNode('gnode')
        node.addGeom(self.geom)

        logging.warning('terrain generated')

        return node

    def calc_normal(self, startpoint, pointa, pointb):
        '''
        Calculate normal vector for a given point and normalize it
        :arguments startpoint - corner of a triangle in relative to which the normal vector is calculated
                   pointa - different corner of the same triangle
                   pointb - the last corner of a triangle
        :return LVector3
        '''

        vector_a = np.array([pointa[0] - startpoint[0],pointa[1] - startpoint[1],pointa[2] - startpoint[2]])
        vector_b = np.array([pointb[0] - startpoint[0],pointb[1] - startpoint[1],pointb[2] - startpoint[2]])
        
        # vector cross product
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
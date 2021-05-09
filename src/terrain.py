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

class Terrain():
     
    def __init__(self, parent):

        self.parent = parent
        self.data = geotiff_load()
        self.camera = self.data[0,0]
        self.numrows = self.data.size
        self.datax = self.data.shape[0]
        self.datay = self.data.shape[1]
        # print(f"datax {self.datax} datay {self.datay} dateexample {self.data[34,34]}")

    def create_terrain(self):
        '''Load height data, create 3D graphics elements, return geometry node'''
        self.format = GeomVertexFormat.get_v3n3cpt2()
        self.format = GeomVertexFormat.registerFormat(self.format)

        self.vdata = GeomVertexData('terrain', self.format, Geom.UHStatic)
        self.vdata.setNumRows(self.numrows)

        self.vertex = GeomVertexWriter(self.vdata, 'vertex')
        self.normal = GeomVertexWriter(self.vdata, 'normal')
        self.color = GeomVertexWriter(self.vdata, 'color')
        self.texcoord = GeomVertexWriter(self.vdata, 'texcoord')

        #create vertices
        for i in range(self.datax):
            for j in range(self.datay):
                self.vertex.addData3(i, j, self.data[i,j])
                self.texcoord.addData2(i/self.datax, j/self.datay)
                self.color.addData4(1,1,1,1)
        #calculate normal vectors for each vertex
        for i in range(self.datax - 1):
            for j in range(self.datay - 1):
                self.normal.addData3(self.calc_normal(startpoint = [i,j,self.data[i,j]], pointa = [i+1,j,self.data[i,j]],pointb = [i,j+1,self.data[i,j]]))
                if j == self.datay - 2:
                    self.normal.addData3(self.calc_normal(startpoint = [i,j,self.data[i,j]], pointa = [i+1,j,self.data[i,j]],pointb = [i,j+1,self.data[i,j]]))
                if i == self.datax - 2:
                    self.normal.addData3(self.calc_normal(startpoint = [i,j,self.data[i,j]], pointa = [i+1,j,self.data[i,j]],pointb = [i,j+1,self.data[i,j]]))

        #create triangle primitives
        self.triangles = []

        for i in range(self.datax - 1):
            for j in range(self.datay - 1):
                index = j + i * self.datay

                prim1 = GeomTriangles(Geom.UHStatic)
                prim1.addVertices(index, index + self.datay, index + self.datay + 1)

                prim2 = GeomTriangles(Geom.UHStatic)
                prim2.addVertices(index, index + self.datay + 1, index + 1)

                self.triangles.append(prim1)
                self.triangles.append(prim2)

        self.geom = Geom(self.vdata)

        for i in range((self.datax - 1) * (self.datay - 1) * 2):
            self.geom.addPrimitive(self.triangles[i])

        node = GeomNode('gnode')
        node.addGeom(self.geom)

        return node

    def calc_normal(self, startpoint, pointa, pointb):
        '''Calculate normal vector for a given point and normalize it'''

        vector_a = [pointa[0] - startpoint[0],pointa[1] - startpoint[1],pointa[2] - startpoint[2]]
        vector_b = [pointb[0] - startpoint[0],pointb[1] - startpoint[1],pointb[2] - startpoint[2]]
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

            self.disableMouse()
            
            self.terrain = Terrain(self.render)
            terrain_node = self.terrain.create_terrain()

            terrain_nodePath = self.render.attachNewNode(terrain_node)
            self.camera.setPos(50,-150,self.terrain.camera + 150)
            self.camera.setHpr(0,-40,0)

            # terrain_nodePath.setTexture(ts, texture)
            # texture = self.loader.loadTexture('maps/envir-ground.jpg')
            # ts = TextureStage('ts')

            #enable mouse movement
            self.oobe()

            #set point light
            plight2 = PointLight('plight2')
            plight2.setColor((0.2, 0.8, 0.2, 1))
            plnp2 = self.render.attachNewNode(plight2)
            plnp2.setPos(100, 350, 250)
            self.render.setLight(plnp2)

            self.render.setShaderAuto()


            # print(f"terrain pos {terrain_nodePath.getPos()}")
            # terrain_nodePath.setPos(-30,200,0)          
            # print(f"terrain pos {terrain_nodePath.getPos()}")

            # print(f"camera pos {self.camera.getPos()}")
            # print(f"camera z {self.terrain.camera}")  

    if __name__ == '__main__':
        app = App()
        app.run()
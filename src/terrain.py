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
import time

logging.basicConfig(format='%(asctime)s %(message)s', datefmt='%I:%M:%S')
logging.warning('dziala')

VERTEXMUL = 4

class Terrain():
     
    def __init__(self, parent):

        self.parent = parent
        self.data = png_load()
        self.camera = self.data[0,0]
        self.numrows = self.data.size
        self.datax = self.data.shape[0]
        self.datay = self.data.shape[1]
        # print(f"datax {self.datax} datay {self.datay} dateexample {self.data[34,34]}")

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

    logging.info('start programu')

    class App(ShowBase):

        def __init__(self):

            ShowBase.__init__(self)

            w, h = 1800, 1200

            props = WindowProperties()
            props.setSize(w,h)
            base.win.requestProperties(props)

            self.disableMouse()
            
            self.terrain = Terrain(self.render)
            terrain_node = self.terrain.create_terrain()

            terrain_nodePath = self.render.attachNewNode(terrain_node)
            self.camera.setPos(300,-1000,self.terrain.camera + 600)
            self.camera.setHpr(0,-30,0)

            ts = TextureStage('ts')
            texture = self.loader.loadTexture('tmp/randommap.png')
            # terrain_nodePath.setTexture(ts, texture)

            #enable mouse movement
            self.oobe()

            # terrain_nodePath.setDepthOffset(1)

            # Create Ambient Light
            ambientLight = AmbientLight('ambientLight')
            ambientLight.setColor((0.2, 0.2, 0.2, 1))
            ambientLightNP = self.render.attachNewNode(ambientLight)
            self.render.setLight(ambientLightNP)

            # Directional light 01
            directionalLight = DirectionalLight('directionalLight')
            directionalLight.setColor((0.8, 0.8, 0.8, 1))
            directionalLight.setShadowCaster(True)
            directionalLightNP = render.attachNewNode(directionalLight)
            # This light is facing backwards, towards the camera.
            directionalLightNP.setHpr(180,-40, 0)
            # render.setLight(directionalLightNP)

            # # Directional light 02
            # directionalLight = DirectionalLight('directionalLight')
            # directionalLight.setColor((0.2, 0.2, 0.8, 1))
            # directionalLightNP = render.attachNewNode(directionalLight)
            # # This light is facing forwards, away from the camera.
            # directionalLightNP.setHpr(0, -40, 0)
            # render.setLight(directionalLightNP)


            dlight = DirectionalLight('dlight')
            # dlight.setColor((1.,0.4,1.,1.))
            dn = self.render.attachNewNode(dlight)
            dn.setHpr(0,-45,0)
            # dn.lookAt(terrain_nodePath)
            # self.render.setLight(dn)

            lens = PerspectiveLens()
            lens.setFov(60)

            slight = Spotlight('slight')
            slight.setColor((1,1,1,1))
            slight.setLens(lens)
            # slight.setShadowCaster(True)
            sn = self.render.attachNewNode(slight)
            sn.lookAt(terrain_nodePath)
            sn.setPos(3000, -50, 350)
            sn.setHpr(-10,-20,0)
            self.render.setLight(sn)

            #set point light
            plight2 = PointLight('plight2')
            plight2.attenuation = (1,0,0)

            plight2.setColor((0.2, 0.8, 0.2, 1))
            plnp2 = self.render.attachNewNode(plight2)
            plnp2.setPos(-100, -100, 500)
            self.render.setLight(plnp2)


            plight = PointLight('plight')
            plight.setColor((0.2, 0.8, 0.2, 1))
            plnp = self.render.attachNewNode(plight)
            plnp.setPos(1000, 1000, 200)
            # self.render.setLight(plnp)

            self.render.setShaderAuto()


            print(f"terrain pos {terrain_nodePath.getPos()}")
            terrain_nodePath.setPos(-30,200,0)          
            print(f"terrain pos {terrain_nodePath.getPos()}")

            print(f"camera pos {self.camera.getPos()}")
            print(f"camera z {self.terrain.camera}")  

    if __name__ == '__main__':
        app = App()
        app.run()
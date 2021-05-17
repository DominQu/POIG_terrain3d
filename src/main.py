''' module: main
    function: create App class,
              combine functions from submodules
'''
from direct.showbase.ShowBase import ShowBase
from direct.gui.DirectGui import *
from panda3d.core import WindowProperties
import sys
sys.path.insert(0, '/home/dominik/GitDir/POIG_terrain3d/src')
from terrain import *


class App(ShowBase):

    def __init__(self):

        ShowBase.__init__(self)

        self.ControlInit()
        self.ParamInit()
        self.MainMenu()

    def ControlInit(self):
        self.disableMouse()

    def ParamInit(self):
        self.font = self.loader.loadFont("fonts/Anton-Regular.ttf")
        self.buttonfont = self.loader.loadFont("fonts/VeraMono.ttf")
        self.buttonImages = (
                             self.loader.loadTexture("UI/button_normal.png"),
                             self.loader.loadTexture("UI/button_pressed.png"),
                             self.loader.loadTexture("UI/button_highlighted.png"),
                             self.loader.loadTexture("UI/button_disabled.png")
                            )
        
    def MainMenu(self):

        self.titleMenuBackdrop = DirectFrame(frameColor = (0, 0.2, 0, 1),
                                             frameSize = (-1, 1, -1, 1),
                                             parent = self.render2d)

        self.titlemenu = DirectFrame(frameColor = (1,0,1,0))

        title = DirectLabel(text = "2to3Dvis",
                            scale = 0.1,
                            pos = (0,0,0.4),
                            relief = None,
                            parent = self.titlemenu,
                            text_font = self.font,
                            text_fg = (1, 1, 1, 1),
                            frameColor = (0,0,0,0))

        label1 = DirectLabel(text = "Wybierz teren:",
                            scale = 0.06,
                            pos = (0,0,0.1),
                            relief = None,
                            parent = self.titlemenu,
                            text_font = self.font,
                            text_fg = (1, 1, 1, 1),
                            frameColor = (0,0,0,0))

        button1 = DirectButton(text="Góra",
                               command = self.Mountain,
                               pos = (0,0,-0.1),
                               parent = self.titlemenu,
                               scale = 0.1,
                               text_font = self.buttonfont,
                               frameTexture = self.buttonImages,
                               frameSize = (-4,4,-1,1),
                               text_scale = 0.8,
                               text_fg = (1,1,1,1),
                               relief = DGG.FLAT,
                               text_pos = (0,-0.3))

        button2 = DirectButton(text="Kanion",
                               command= self.Canyon,
                               pos = (0,0,-0.4),
                               parent = self.titlemenu,
                               scale = 0.1,
                               text_font = self.buttonfont,
                               frameTexture = self.buttonImages,
                               frameSize = (-4,4,-1,1),
                               text_scale = 0.8,
                               text_fg = (1,1,1,1),
                               relief = DGG.FLAT,
                               text_pos = (0,-0.3))

    def Mountain(self):
        
        self.titlemenu.hide()

        self.mountainmenu = DirectFrame(frameColor = (1,0,1,0))

        label = DirectLabel(text = "Wybierz teksturę:",
                            scale = 0.06,
                            pos = (0,0,0.3),
                            relief = None,
                            parent = self.mountainmenu,
                            text_font = self.font,
                            text_fg = (1, 1, 1, 1),
                            frameColor = (0,0,0,0))

        button1 = DirectButton(text="Ziemia",
                               command = self.Light,
                               extraArgs = ["mountain", "ziemia", self.mountainmenu],
                               pos = (0,0,0.1),
                               parent = self.mountainmenu,
                               scale = 0.1,
                               text_font = self.buttonfont,
                               frameTexture = self.buttonImages,
                               frameSize = (-4,4,-1,1),
                               text_scale = 0.8,
                               text_fg = (1,1,1,1),
                               relief = DGG.FLAT,
                               text_pos = (0,-0.3))

        button2 = DirectButton(text="Księżyc",
                               command= self.Light,
                               extraArgs = ["mountain", "ksiezyc", self.mountainmenu],
                               pos = (0,0,-0.2),
                               parent = self.mountainmenu,
                               scale = 0.1,
                               text_font = self.buttonfont,
                               frameTexture = self.buttonImages,
                               frameSize = (-4,4,-1,1),
                               text_scale = 0.8,
                               text_fg = (1,1,1,1),
                               relief = DGG.FLAT,
                               text_pos = (0,-0.3))
    def Canyon(self):
        
        self.titlemenu.hide()

        self.canyonmenu = DirectFrame(frameColor = (1,0,1,0))

        label = DirectLabel(text = "Wybierz teksturę:",
                            scale = 0.06,
                            pos = (0,0,0.3),
                            relief = None,
                            parent = self.canyonmenu,
                            text_font = self.font,
                            text_fg = (1, 1, 1, 1),
                            frameColor = (0,0,0,0))

        button1 = DirectButton(text="Rzeka",
                               command = self.Light,
                               extraArgs = ["canyon", "rzeka", self.canyonmenu],
                               pos = (0,0,0.1),
                               parent = self.canyonmenu,
                               scale = 0.1,
                               text_font = self.buttonfont,
                               frameTexture = self.buttonImages,
                               frameSize = (-4,4,-1,1),
                               text_scale = 0.8,
                               text_fg = (1,1,1,1),
                               relief = DGG.FLAT,
                               text_pos = (0,-0.3))

        button2 = DirectButton(text="Pustynia",
                               command= self.Light,
                               extraArgs = ["canyon", "pustynia", self.canyonmenu],
                               pos = (0,0,-0.2),
                               parent = self.canyonmenu,
                               scale = 0.1,
                               text_font = self.buttonfont,
                               frameTexture = self.buttonImages,
                               frameSize = (-4,4,-1,1),
                               text_scale = 0.8,
                               text_fg = (1,1,1,1),
                               relief = DGG.FLAT,
                               text_pos = (0,-0.3))

    def Light(self, terrain, texture, submenu):
        self.StartApp(terrain, texture, submenu)

    def StartApp(self, terrain, texture, submenu):
        submenu.hide()
        self.titleMenuBackdrop.hide()

        w, h = 1800, 1200

        props = WindowProperties()
        props.setSize(w,h)
        base.win.requestProperties(props)
        
        terrain = Terrain(self.render)
        terrain_node = terrain.create_terrain()
        self.terrainNodePath = self.render.attachNewNode(terrain_node)

        self.SetCamera()
        self.SetTexture()
        self.SetLights()

    def SetCamera(self):
        pass

    def SetTexture(self):
        pass

    def SetLights(self):
        pass


if __name__ == '__main__':
    app = App()
    app.run()
''' module: main
    function: create App class,
              combine functions from submodules
'''
from direct.showbase.ShowBase import ShowBase
from direct.gui.DirectGui import *
from panda3d.core import DirectionalLight, PointLight, Spotlight, PerspectiveLens
from panda3d.core import AmbientLight
from panda3d.core import TextureStage
from panda3d.core import WindowProperties
from panda3d.core import Vec3
from terrain import *


class App(ShowBase):

    def __init__(self):

        ShowBase.__init__(self)

        self.ParamInit()
        self.MainMenu()
        self.AlwaysOnScreen()
        self.OnScreenMenu()
        self.KeyboardUpdate()
        self.updateTask = taskMgr.add(self.update, "update")

    def KeyboardUpdate(self):

        self.accept("w", self.UpdateKeymap, ["forward", True])
        self.accept("w-up", self.UpdateKeymap, ["forward", False])
        self.accept("s", self.UpdateKeymap, ["back", True])
        self.accept("s-up", self.UpdateKeymap, ["back", False])
        self.accept("a", self.UpdateKeymap, ["left", True])
        self.accept("a-up", self.UpdateKeymap, ["left", False])
        self.accept("d", self.UpdateKeymap, ["right", True])
        self.accept("d-up", self.UpdateKeymap, ["right", False])
        self.accept("q", self.UpdateKeymap, ["up", True])
        self.accept("q-up", self.UpdateKeymap, ["up", False])
        self.accept("e", self.UpdateKeymap, ["down", True])
        self.accept("e-up", self.UpdateKeymap, ["down", False])
        self.accept("arrow_left", self.UpdateKeymap, ["tiltleft", True])
        self.accept("arrow_left-up", self.UpdateKeymap, ["tiltleft", False])
        self.accept("arrow_right", self.UpdateKeymap, ["tiltright", True])
        self.accept("arrow_right-up", self.UpdateKeymap, ["tiltright", False])
        self.accept("arrow_up", self.UpdateKeymap, ["tiltup", True])
        self.accept("arrow_up-up", self.UpdateKeymap, ["tiltup", False])
        self.accept("arrow_down", self.UpdateKeymap, ["tiltdown", True])
        self.accept("arrow_down-up", self.UpdateKeymap, ["tiltdown", False])
    
    def update(self, task):

        dt = globalClock.getDt()

        if self.keymap["forward"]:
            self.camera.setPos(self.camera.getPos() + Vec3(0, 1000.0*dt, 0))
        if self.keymap["back"]:
            self.camera.setPos(self.camera.getPos() + Vec3(0, -1000.0*dt, 0))
        if self.keymap["left"]:
            self.camera.setPos(self.camera.getPos() + Vec3(-1000.0*dt, 0, 0))
        if self.keymap["right"]:
            self.camera.setPos(self.camera.getPos() + Vec3(1000.0*dt, 0, 0))
        if self.keymap["up"]:
            self.camera.setPos(self.camera.getPos() + Vec3(0, 0, 1000.0*dt))
        if self.keymap["down"]:
            self.camera.setPos(self.camera.getPos() + Vec3(0, 0, -1000.0*dt))
        if self.keymap["tiltleft"]:
            self.camera.setHpr(self.camera.getHpr() + Vec3(20*dt, 0, 0))
        if self.keymap["tiltright"]:
            self.camera.setHpr(self.camera.getHpr() + Vec3(-20*dt, 0, 0))
        if self.keymap["tiltup"]:
            self.camera.setHpr(self.camera.getHpr() + Vec3(0, 20*dt, 0))
        if self.keymap["tiltdown"]:
            self.camera.setHpr(self.camera.getHpr() + Vec3(0, -20*dt, 0))
        return task.cont

    def UpdateKeymap(self, direction, newstate):
        self.keymap[direction] = newstate

    def ParamInit(self):
       
        self.disableMouse()
        self.font = self.loader.loadFont("fonts/Anton-Regular.ttf")
        self.buttonfont = self.loader.loadFont("fonts/VeraMono.ttf")
        self.buttonImages = (
            self.loader.loadTexture("UI/button_normal.png"),
            self.loader.loadTexture("UI/button_pressed.png"),
            self.loader.loadTexture("UI/button_highlighted.png"),
            self.loader.loadTexture("UI/button_disabled.png")
        )
        self.w = 2200
        self.h = 1200
        self.x = 200
        self.y = 100
        self.camerapos = {
            "mountain": Vec3(400,-4100,3675),
            "canyon":Vec3(500,-4500,2700)
        }
        self.camerahpr = {
            "mountain": Vec3(-20,-20,0),
            "canyon":Vec3(-21,-20,0)
        }
        self.texturefiles = {
            "earth": 'textures/agri-small-autumn.jpg',
            "moon": 'textures/agri-small-winter.jpg',
            "river": 'textures/river.png',
            "desert": 'textures/desert.png'
        }
        self.heightmaps = {
            "mountain": 'dems/mountain.png',
            "canyon": 'dems/canyon.png'
        }
        self.keymap = {
            "forward": False,
            "back": False,
            "right": False,
            "left": False,
            "up": False,
            "down": False,
            "tiltleft": False,
            "tiltright": False,
            "tiltup": False,
            "tiltdown": False
        }
        self.mountain = False
        self.canyon = False
        
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

        button3 = DirectButton(text="Wyjście",
                               command= self.finalizeExit,
                               pos = (0,0,-0.7),
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

        self.mountain = True

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
                               extraArgs = ["mountain", "earth", self.mountainmenu],
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
                               extraArgs = ["mountain", "moon", self.mountainmenu],
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

        button2 = DirectButton(text="Powrót",
                               command= self.Restart,
                               extraArgs = ["mountain"],
                               pos = (0,0,-0.5),
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

        self.canyon = True

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
                               extraArgs = ["canyon", "river", self.canyonmenu],
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
                               extraArgs = ["canyon", "desert", self.canyonmenu],
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

        button3 = DirectButton(text="Powrót",
                               command= self.Restart,
                               extraArgs = ["canyon"],
                               pos = (0,0,-0.5),
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

    def StartApp(self, terraintype, texture, submenu):
        
        submenu.hide()
        self.titleMenuBackdrop.hide()

        self.props = WindowProperties()
        self.props.setSize(self.w,self.h)
        self.props.setOrigin(self.x, self.y)
        base.win.requestProperties(self.props)
        
        self.terrain = Terrain(self.render, terraintype)
        terrain_node = self.terrain.create_terrain()
        self.terrainNodePath = self.render.attachNewNode(terrain_node)

        self._SetCamera(terraintype)
        self._SetTexture(texture)
        self._SetLights()
        self.alwaysframe.show()
        self.dialog.show()

    def _SetCamera(self, terraintype):

        self.camera.setPos(self.camerapos[terraintype])
        self.camera.setHpr(self.camerahpr[terraintype])

    def _SetTexture(self, texture):
        
        ts = TextureStage('ts')
        tx = self.loader.loadTexture(self.texturefiles[texture])
        self.terrainNodePath.setTexture(ts, tx)

    def _SetLights(self):
        
        ambientLight = AmbientLight('ambientLight')
        ambientLight.setColor((0.4, 0.4, 0.4, 1))
        ambientLightNP = self.render.attachNewNode(ambientLight)
        self.render.setLight(ambientLightNP)

        plight = PointLight('plight')
        plight.setColor((0.8, 0.8, 0.8, 1))
        plnp = self.render.attachNewNode(plight)
        plnp.setPos(self.terrain.datax*10/2, 500, self.terrain.maxheight+1000)
        self.render.setLight(plnp)

        lens = PerspectiveLens()
        lens.setFov(60)

        slight = Spotlight('slight')
        slight.setColor((1,1,1,1))
        slight.setLens(lens)
        slight.setShadowCaster(True)
        sn = self.render.attachNewNode(slight)
        sn.lookAt(self.terrainNodePath)
        sn.setPos(self.terrain.datax*10/2,-2000, self.terrain.maxheight+500)
        sn.setHpr(0,-20,0)
        self.render.setLight(sn)

        self.render.setShaderAuto()

    def AlwaysOnScreen(self):
        
        self.alwaysframe = DirectFrame(
            frameColor = (0,0,0,0),
            frameSize = (-1,1,-1,1)
        )
        button1 = DirectButton(text="Menu",
                               command = self.ToggleOnScreenMenu,
                               pos = (-1.7,0,0.9),
                               parent = self.alwaysframe,
                               scale = 0.05,
                               text_font = self.buttonfont,
                               frameTexture = self.buttonImages,
                               frameSize = (-2,2,-1,1),
                               text_scale = 0.8,
                               text_fg = (1,1,1,1),
                               relief = DGG.FLAT,
                               text_pos = (0,-0.3))

        self.dialog = OkDialog(parent= self.alwaysframe,
                               text= "Sterowanie:\nW - do przodu\nS - do tyłu  \nA - w lewo   \nD - w prawo  \nQ - w górę\nE - w dół\nStrzałka góra/dół - pochyl w górę/dół  \nStrzałka lewo/prawo - obrót w lewo/prawo",
                               command = self.HideDialog,
                               text_font = self.buttonfont,
                               text_fg = (1, 1, 1, 1))
       
        self.alwaysframe.hide()

    def HideDialog(self, dialogvalue):

        self.dialog.hide()
    
    def ToggleOnScreenMenu(self):
        
        if self.onscreenmenu.isHidden():
            self.onscreenmenu.show()
        else:
            self.onscreenmenu.hide()

    def OnScreenMenu(self):

        self.onscreenmenu = DirectFrame(
            frameColor = (0,0,0,0.4),
            frameSize = (-1, -0.2, -1, 1),
            pos = (-1,-1,0)
        )
        button1 = DirectButton(text="Menu główne",
                               command = self.Restart,
                               extraArgs = ["terrain"],
                               pos = (-0.52,0,0.7),
                               parent = self.onscreenmenu,
                               scale = 0.05,
                               text_font = self.buttonfont,
                               frameTexture = self.buttonImages,
                               frameSize = (-4,4,-1,1),
                               text_scale = 0.8,
                               text_fg = (1,1,1,1),
                               relief = DGG.FLAT,
                               text_pos = (0,-0.3))

        button2 = DirectButton(text="Mapa wysokości",
                               command = self.ShowMap,
                               pos = (-0.52,0,0.4),
                               parent = self.onscreenmenu,
                               scale = 0.05,
                               text_font = self.buttonfont,
                               frameTexture = self.buttonImages,
                               frameSize = (-4,4,-1,1),
                               text_scale = 0.8,
                               text_fg = (1,1,1,1),
                               relief = DGG.FLAT,
                               text_pos = (0,-0.3))

        button3 = DirectButton(text="Reset kamery",
                               command = self.ResetCamera,
                               pos = (-0.52,0,0.1),
                               parent = self.onscreenmenu,
                               scale = 0.05,
                               text_font = self.buttonfont,
                               frameTexture = self.buttonImages,
                               frameSize = (-4,4,-1,1),
                               text_scale = 0.8,
                               text_fg = (1,1,1,1),
                               relief = DGG.FLAT,
                               text_pos = (0,-0.3))

        button4 = DirectButton(text="Sterowanie",
                               command = self.dialog.show,
                               pos = (-0.52,0,-0.2),
                               parent = self.onscreenmenu,
                               scale = 0.05,
                               text_font = self.buttonfont,
                               frameTexture = self.buttonImages,
                               frameSize = (-4,4,-1,1),
                               text_scale = 0.8,
                               text_fg = (1,1,1,1),
                               relief = DGG.FLAT,
                               text_pos = (0,-0.3))

        button5 = DirectButton(text="Wyjście",
                               command = self.finalizeExit,
                               pos = (-0.52,0,-0.5),
                               parent = self.onscreenmenu,
                               scale = 0.05,
                               text_font = self.buttonfont,
                               frameTexture = self.buttonImages,
                               frameSize = (-4,4,-1,1),
                               text_scale = 0.8,
                               text_fg = (1,1,1,1),
                               relief = DGG.FLAT,
                               text_pos = (0,-0.3))          
        
        self.onscreenmenu.hide()

    def Restart(self, node_to_remove):

        self.mountain = False
        self.canyon = False

        if node_to_remove == "terrain":
            self.terrainNodePath.removeNode()
        elif node_to_remove == "canyon":
            self.canyonmenu.destroy()
        elif node_to_remove == "mountain":
            self.mountainmenu.destroy()

        self.alwaysframe.hide()
        self.onscreenmenu.hide()
        self.titleMenuBackdrop.show()
        self.titlemenu.show()

    def ResetCamera(self):
        
        if self.mountain == True:
            self.camera.setPos(self.camerapos["mountain"])
            self.camera.setHpr(self.camerahpr["mountain"])
        elif self.canyon == True:
            self.camera.setPos(self.camerapos["canyon"])
            self.camera.setHpr(self.camerahpr["canyon"])

    def ShowMap(self, ):

        self.onscreenmenu.hide()

        if self.mountain:
            filepath = self.heightmaps["mountain"]
        elif self.canyon:
            filepath = self.heightmaps["canyon"]

        self.mapimage = OnscreenImage(image=filepath, pos= (1,0,0.2),scale= 0.55)

        self.heightmapbutton = DirectButton(text="Zamknij",
                               command = self.DestroyMap,
                               pos = (1.45,0,0.8),
                               parent = self.alwaysframe,
                               scale = 0.05,
                               text_font = self.buttonfont,
                               frameTexture = self.buttonImages,
                               frameSize = (-2,2,-1,1),
                               text_scale = 0.8,
                               text_fg = (1,1,1,1),
                               relief = DGG.FLAT,
                               text_pos = (0,-0.3))

    def DestroyMap(self):

        self.mapimage.destroy()
        self.heightmapbutton.destroy()
        

if __name__ == '__main__':
    app = App()
    app.run()
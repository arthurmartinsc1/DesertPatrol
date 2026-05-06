# DesertPatrol - engine
# Autor: Arthur Martins
# Descrição: Configuração base do motor de jogo, iluminação, colisão e menus

from panda3d.core import *



appName = "DesertPatrol"

loadPrcFileData("",
                        """
                            window-title {}
                            textures-power-2 none
                            """.format(appName))




from direct.showbase.ShowBase import ShowBase
from direct.gui.DirectGui import *
import sys
sys.path.append(r"C:\Users\avise\Desktop\Games\RenderPipeline-master")

USE_RENDER_PIPELINE = False

if USE_RENDER_PIPELINE:
    from rpcore import RenderPipeline, SpotLight
    rp = RenderPipeline()

    models = {
        "terrain":"models/terrain.bam",
        "player":"models/jet/jet2.bam",
        }

else:
    models = {
        "terrain":"models/terrain.bam",
        "player":"models/supermarine_spitfire.glb",
        }


class GameBase(ShowBase):
    def __init__(self, autoSetup = True, debug = False):
        if USE_RENDER_PIPELINE:
            rp.set_loading_screen_image("screenshot7.png")
            rp.create(self)
            rp.daytime_mgr.time = 0.43
        else:
            ShowBase.__init__(self)
            try:
                import simplepbr
                simplepbr.init()
            except ImportError:
                render.setShaderAuto()
            render.setAntialias(AntialiasAttrib.MAuto)

        if autoSetup:
            self.setupLighting()
            self.setupCollision()
            base.enableParticles()

        if debug:
            base.setFrameRateMeter(True)
            self.accept("1", base.oobe)
            self.accept("s", base.win.saveScreenshot, ["Saved screenshot.png"])

    def setupCollision(self):
        base.cTrav = CollisionTraverser()
        base.pusher = CollisionHandlerPusher()
        base.pusher.addInPattern("%fn-into-%in")

    def setupLighting(self):
        if not USE_RENDER_PIPELINE:
            al = AmbientLight("scene light")
            al.setColor((0.55, 0.45, 0.25, 1.0))
            self.alnp = render.attachNewNode(al)
            render.setLight(self.alnp)

            self.createDirectionalLight(hpr = (0, 90, 30), sunColor = (1.0, 0.85, 0.5, 1.0))
            self.createDirectionalLight(hpr = (-90, 90, 120))
            self.createDirectionalLight(hpr = (90, -90, 270))

            self.worldColor = (0.87, 0.78, 0.55)

            base.setBackgroundColor(*self.worldColor)

            self.fog = Fog("scene fog")
            self.fog.setExpDensity(0.002)
            self.fog.setColor(*self.worldColor)
            render.setFog(self.fog)


        else:
            #Use RP scattering for lights
            pass

    def createDirectionalLight(self, hpr = (0, 0, 0), sunColor = None):
        dl = DirectionalLight("sun")
        if sunColor:
            dl.setColor(sunColor)
        dlnp = render.attachNewNode(dl)
        dlnp.setHpr(*hpr)
        render.setLight(dlnp)

    def setMusic(self, path, loops = True, volume = 1):
        sound = loader.loadSfx(path)
        sound.setVolume(volume)
        sound.setLoop(loops)
        sound.play()



class MenuBase:
    def __init__(self):
        self.frame = DirectFrame(
            frameSize = (base.a2dLeft, base.a2dRight,
                         base.a2dBottom, base.a2dTop),
            frameColor = (0.01, 0.012, 0.016, 0.96),
            )
        self.frame.setTransparency(1)


        self.hide()

    def makeButton(self, text = "New Button", pos = (0, -0.7), event = "unknown-button", scale = 0.03, hasPadding = True):
        btn = DirectButton(
            text = text,
            frameColor = (
                (0.82, 0.2, 0.08, 1),
                (1.0, 0.34, 0.12, 1),
                (0.55, 0.08, 0.04, 1),
                (0.16, 0.16, 0.18, 1),
                ),
            text_scale = scale,
            text_pos = (0, 0),
            scale = 2.45,
            pos = (pos[0], 0, pos[1]),
            text_fg = (1, 0.96, 0.86, 1),
            command = base.messenger.send,
            extraArgs = [event],
            rolloverSound = None,
            clickSound = None,
            relief = DGG.FLAT,
            borderWidth = (0.006, 0.006),
            )
        if hasPadding:
            btn["pad"] = (0.085, 0.01)
        else:
            btn["pad"] = (0.025, 0.008)
        return btn


    def makeTitle(self, text = "", pos = (0, 0.6), scale = 0.15):
         return DirectLabel(
            scale = scale,
            text_shadow = (0, 0, 0, 1),
            pos = (pos[0], 0, pos[1]),
            text = text,
            text_fg = (0.94, 0.88, 0.72, 1),
            frameColor = (0, 0, 0, 0),
            )

    def show(self):
        self.frame.show()

    def hide(self):
        self.frame.hide()

class Menu(MenuBase):
    def __init__(self):
        MenuBase.__init__(self)

        self.title = self.makeTitle("DesertPatrol", pos = (0, 0.34), scale = 0.18)
        self.title.reparentTo(self.frame)

        self.start = self.makeButton(text = "Jogar", pos = (0, 0.08), event = "menu-start")
        self.start.reparentTo(self.frame)

        self.settings = self.makeButton(text = "Configurações", pos = (0, -0.16), event = "menu-settings")
        self.settings.reparentTo(self.frame)

        self.quit = self.makeButton(text = "Sair", pos = (0, -0.4), event = "menu-quit")
        self.quit.reparentTo(self.frame)

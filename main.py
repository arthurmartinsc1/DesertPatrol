# DesertPatrol - main
# Autor: Arthur Martins
# Descrição: Ponto de entrada do jogo, gerencia estados da FSM e define missões

from panda3d.core import *
from direct.showbase.ShowBase import *
from direct.fsm.FSM import FSM
from direct.gui.OnscreenText import OnscreenText
from direct.particles.ParticleEffect import ParticleEffect
from engine import *
from briefing import MissionScreen
from report import Debrief, GameOverScreen
from cockpit_hud import Hud
from mission_menu import MissionSelect
from mission_loader import parseMissionFile, generate_random_models
from settings import Settings

import sys
import time
import random


def make_cocaine_packet():
    from panda3d.core import (GeomNode, Geom, GeomVertexData, GeomVertexFormat,
                               GeomVertexWriter, GeomTriangles, NodePath,
                               TransparencyAttrib)

    def make_box(name, size, color, pos=(0, 0, 0)):
        sx, sy, sz = size
        hx, hy = sx / 2.0, sy / 2.0
        fmt = GeomVertexFormat.getV3n3c4()
        vdata = GeomVertexData(name, fmt, Geom.UHStatic)
        vdata.setNumRows(24)
        vertex = GeomVertexWriter(vdata, 'vertex')
        normal = GeomVertexWriter(vdata, 'normal')
        vertex_color = GeomVertexWriter(vdata, 'color')
        faces = [
            (( hx,  hy, sz), (-hx,  hy, sz), (-hx, -hy, sz), ( hx, -hy, sz), (0, 0, 1)),
            (( hx,  hy,  0), ( hx, -hy,  0), (-hx, -hy,  0), (-hx,  hy,  0), (0, 0, -1)),
            (( hx,  hy, sz), ( hx,  hy,  0), (-hx,  hy,  0), (-hx,  hy, sz), (0, 1, 0)),
            (( hx, -hy, sz), (-hx, -hy, sz), (-hx, -hy,  0), ( hx, -hy,  0), (0, -1, 0)),
            (( hx,  hy, sz), ( hx, -hy, sz), ( hx, -hy,  0), ( hx,  hy,  0), (1, 0, 0)),
            ((-hx,  hy, sz), (-hx,  hy,  0), (-hx, -hy,  0), (-hx, -hy, sz), (-1, 0, 0)),
        ]
        tris = GeomTriangles(Geom.UHStatic)
        for i, (v0, v1, v2, v3, n) in enumerate(faces):
            base_i = i * 4
            for v in (v0, v1, v2, v3):
                vertex.addData3(*v)
                normal.addData3(*n)
                vertex_color.addData4(*color)
            tris.addVertices(base_i, base_i + 1, base_i + 2)
            tris.addVertices(base_i, base_i + 2, base_i + 3)

        geom = Geom(vdata)
        geom.addPrimitive(tris)
        node = GeomNode(name)
        node.addGeom(geom)
        np = NodePath(node)
        np.setPos(*pos)
        np.setColor(*color)
        np.setTwoSided(True)
        return np

    packet = NodePath("cocaine_packet")
    body = make_box("packet_wrapping", (0.55, 0.38, 0.18), (0.48, 0.39, 0.28, 1))
    band_y = make_box("packet_tape_y", (0.14, 0.42, 0.195), (0.92, 0.9, 0.78, 1), (0, 0, 0.004))
    band_x = make_box("packet_tape_x", (0.59, 0.09, 0.2), (0.88, 0.86, 0.72, 1), (0, 0, 0.008))
    label = make_box("packet_label", (0.22, 0.14, 0.012), (0.08, 0.55, 0.22, 1), (0, 0, 0.2))
    shadow = make_box("packet_shadow", (0.62, 0.45, 0.006), (0.06, 0.05, 0.04, 0.45), (0, 0, 0.002))

    for part in (shadow, body, band_y, band_x, label):
        part.reparentTo(packet)

    packet.setTransparency(TransparencyAttrib.MAlpha)
    packet.setH(random.uniform(-18, 18))
    packet.setScale(0.75)
    return packet


class Mission:
    def __init__(self, timeAllowed = 60,
                 objective = "Objetivo padrão",
                 question = "Pergunta padrão",
                 mapName = "models/terrain.egg",
                 options = ["o1", "o2", "o3"],
                 correctAnswer = "o2",
                 randomize = False,
                 randomModel = None,
                 randomMin = 2,
                 randomMax = 6,
                 randomCenter = (0, 0, 0.8)):
        self.timeAllowed = timeAllowed
        self.objective = objective
        self.objective += "\n Você tem " + str(timeAllowed) + " segundos\n para completar a missão."
        self.question = question
        self.mapName = mapName
        self.options = list(options)
        self.correctAnswer = correctAnswer
        self.randomize = randomize
        self.randomModel = randomModel
        self.randomMin = randomMin
        self.randomMax = randomMax
        self.randomCenter = randomCenter


missions = {
    "m1": Mission(
        timeAllowed = 60,
        objective = "ROTA DE CONTRABANDO\n Contrabandistas fugiram deixando\n pacotes de cocaína no deserto.\n Sobrevoe a área e conte os pacotes.",
        question = "Quantos pacotes de cocaína foram identificados?",
        mapName = "models/m1.mission",
        options = ["2", "3", "4"],
        correctAnswer = "3",
        randomize = True,
        randomModel = "cocaine-packet",
        randomMin = 2,
        randomMax = 6,
        randomCenter = (12, 22.7, 0.75),
        ),
    "m2": Mission(
        timeAllowed = 60,
        objective = "INFILTRAÇÃO NÔMADE\n Helicópteros não identificados\n pousaram em dois pontos distintos.\n Registre o número total de aeronaves.",
        question = "Quantos helicópteros foram avistados no total?",
        mapName = "models/m2.mission",
        options = ["3", "5", "7"],
        correctAnswer = "3",
        randomize = True,
        randomModel = "helicopter",
        randomMin = 2,
        randomMax = 6,
        randomCenter = (-12, 18, 2.8),
        ),
    "m3": Mission(
        timeAllowed = 180,
        objective = "PROTÓTIPO FANTASMA\n Inteligência detectou uma aeronave\n experimental escondida no deserto.\n Localize e reporte suas características.",
        question = "Quantas asas o protótipo possui?",
        mapName = "models/terrain_m1",
        options = ["3", "4", "2"],
        correctAnswer = "3"),
    "test": Mission(
        timeAllowed = 2,
        objective = "MISSÃO DE TREINO\n Familiarize-se com os controles\n antes de ir ao campo.",
        question = "Qual é o código de retorno ao base?",
        mapName = "models/m1.mission",
        options = ["t", "t1", "t2"],
        correctAnswer = "t"
        ),
    }

class Game(GameBase, FSM):
    def __init__(self):
        GameBase.__init__(self, debug = True)
        FSM.__init__(self, "GUI FSM")
        base.disableMouse()

        self.menu = Menu()
        self.settings = Settings()
        self.missionScreen = MissionScreen()
        self.debrief = Debrief()
        self.gameOver = GameOverScreen()
        self.hud = Hud()
        self.missionSelect = MissionSelect()

        base.camLens.setFov(90)


        self.request("Menu")
        base.taskMgr.add(self.missionOverTask, "is mission over")


    def enterMenu(self):
        self.menu.show()
        self.accept("menu-start", self.request, ["MissionSelect"])
        self.accept("menu-instructions", self.request, ["Instructions"])
        self.accept("menu-quit", sys.exit)
        self.accept("menu-settings", self.request, ["Settings"])

    def exitMenu(self):
        self.menu.hide()
        self.ignore("menu-start")
        self.ignore("menu-instructions")
        self.ignore("menu-quit")
        self.ignore("menu-settings")

    def enterSettings(self):
        self.settings.show()
        self.accept("settings-back", self.request, ["Menu"])

    def exitSettings(self):
        self.settings.hide()
        self.ignore("settings-back")

    def enterMissionSelect(self):
        self.missionSelect.show()
        self.accept("missionselect-m1", self.setMission, ["m1"])
        self.accept("missionselect-m2", self.setMission, ["m2"])

    def exitMissionSelect(self):
        self.missionSelect.hide()
        self.ignore("missionselect-m1")
        self.ignore("missionselect-m2")

    def enterMissionScreen(self):
        self.missionScreen.showWithTitle(self.currentMission.objective)
        self.accept("mission-start", self.request, ["Game"])

    def exitMissionScreen(self):
        self.missionScreen.hide()
        self.ignore("mission-start")

    def _makeRandomOptions(self, correct, min_val, max_val):
        opts = {correct}
        pool = list(range(max(1, min_val - 1), max_val + 3))
        random.shuffle(pool)
        for c in pool:
            if c != correct:
                opts.add(c)
            if len(opts) == 3:
                break
        result = [str(x) for x in sorted(opts)]
        random.shuffle(result)
        return result

    def enterGame(self):
        generatedModels = None
        if self.currentMission.randomize:
            count = random.randint(self.currentMission.randomMin, self.currentMission.randomMax)
            self.currentMission.correctAnswer = str(count)
            self.currentMission.options = self._makeRandomOptions(
                count, self.currentMission.randomMin, self.currentMission.randomMax)
            generatedModels = generate_random_models(
                self.currentMission.randomModel, count,
                center=self.currentMission.randomCenter)
        self.world = World(self.currentMission.mapName, generatedModels)
        self.startTime = "Not yet set - not loaded"  #set in self.missionOverTask
        self.player = Player(self.world)
        self.accept("player-into-Collision", self.showGameOver)
        self.accept("game-quit", self.request, ["Menu"])
        self.accept("game-finished", self.request, ["Debrief"])
        self.accept("game-crashed", self.showGameOver)

    def exitGame(self):
        self.world.destroy()
        self.player.model.removeNode()
        del self.player
        base.taskMgr.remove("hud update")
        self.hud.timer.setText("")
        self.hud.hide()
        base.taskMgr.remove("update player")
        self.ignore("game-quit")
        self.ignore("game-finished")
        self.ignore("game-crashed")
        self.ignore("player-into-Collision")

    def enterDebrief(self):
        self.debrief.show()
        self.debrief.setTitle(self.currentMission.question, isAnswer = False)
        self.debrief.setButtons(self.currentMission)
        self.accept("debrief-correct", self.debrief.setTitle, ["Correto!"])
        self.accept("debrief-wrong", self.debrief.setTitle, ["Errado!"])
        self.accept("debrief-back", self.request, ["Menu"])
        self.accept("debrief-restart", self.request, ["Game"])

    def exitDebrief(self):
        self.debrief.hide()
        self.ignore("debrief-correct")
        self.ignore("debrief-wrong")
        self.ignore("debrief-back")
        self.ignore("debrief-restart")
        self.debrief.initialise() #clear all settings on it, ie title and buttons, as they are mission specific

    def showGameOver(self, *args):
        self.request("GameOver")

    def enterGameOver(self):
        self.gameOver.show()
        self.accept("gameover-menu", self.request, ["Menu"])

    def exitGameOver(self):
        self.gameOver.hide()
        self.ignore("gameover-menu")

    def setMission(self, name):
        self.currentMission = missions[name]
        self.request("MissionScreen")

    def missionOverTask(self, task):
        if self.state == "Game" and self.world.loaded and self.startTime == "Not yet set - not loaded":
            self.startTime = time.time()
            self.hud.show()
            self.hud.initialise(self.currentMission.objective, self.currentMission.timeAllowed)
            base.taskMgr.add(self.hud.hudTask, "hud update")
        if self.state == "Game" and self.world.loaded:
            if time.time() - self.startTime > self.currentMission.timeAllowed:
                self.request("Debrief")
        return task.cont


class World:
    def __init__(self, missionMap, modelList=None):
        self.map = missionMap
        self.preloadedModels = modelList
        base.taskMgr.add(self.loadScene)
        self.loaded = False


    async def loadScene(self, task):
        text = OnscreenText("Carregando...")

        self.terrain = await loader.loadModel(models["terrain"], blocking = False)
        self.terrain.reparentTo(render)
        if USE_RENDER_PIPELINE:
            rp.prepare_scene(self.terrain)
        self.terrain.setScale(18)

        sandTex = loader.loadTexture("models/tex/desert_sand.png")
        sandTex.setWrapU(Texture.WMRepeat)
        sandTex.setWrapV(Texture.WMRepeat)
        self.terrain.setTexture(sandTex, 1)


        modelList = parseMissionFile(self.map) + (self.preloadedModels or [])
        print(modelList)
        self.particlesList = []
        for model in modelList:
            try:
                if model.modelName == "cocaine-packet":
                    m = make_cocaine_packet()
                    m.reparentTo(self.terrain)
                    m.setPos(*model.modelPos)
                    continue
                m = loader.loadModel("models/" + model.modelName)
                m.reparentTo(self.terrain)
                m.setPos(*model.modelPos)
                if model.modelName == "helicopter":
                    m.setScale(2)
            except:
                #Its a particle system
                floater = render.attachNewNode("particle floater")
                floater.setPos(self.terrain, *model.particlePos)
                floater.setScale(5)
                fx = ParticleEffect()
                fx.loadConfig(model.ptfFile)
                fx.start(parent=floater, renderParent=floater)
                self.particlesList.append((fx, floater))


        #Once loaded, remove loading text
        text.hide()
        del text

        self.loaded = True

    def show(self):
        self.terrain.show()

    def hide(self):
        self.terrain.hide()

    def destroy(self):
        self.terrain.removeNode()
        del self.terrain
        del self

class Player:
    START_SPEED = 35
    TERMINAL_SPEED = 35
    MIN_SPEED = 5
    SPEED_CHANGE_RATE = 0.01
    CRASH_Z = 0.75

    def __init__(self, worldInstance):       
        self.model = render.attachNewNode("player")
        self.model.setZ(19)
 
        mesh = loader.loadModel(models["player"])
        mesh.reparentTo(self.model)
        mesh.setScale(0.015)
        mesh.setHpr(90, 55, 120)

        if USE_RENDER_PIPELINE:
            rp.prepare_scene(self.model)

        base.taskMgr.add(self.playerUpdate, "update player")

        self.speed = self.START_SPEED
        self.crashed = False

        self.colNode = self.model.attachNewNode(CollisionNode("player"))
        self.colNode.node().addSolid(CollisionSphere(0, 0, 0, 1))
        #self.colNode.show()
        base.cTrav.addCollider(self.colNode, base.pusher)
        base.pusher.addCollider(self.colNode, self.model)

        #self.particles = ParticleEffect()
        #self.particles.loadConfig("vfx/exhaust.ptf")
        #self.particles.start(parent = self.model, renderParent = render)

        self.worldInstance = worldInstance

    def reset(self, event):
        self.model.setPos(0, 0, 19)
        self.model.setHpr(0, 0, 0)

    def playerUpdate(self, task):
        pressed = base.mouseWatcherNode.isButtonDown

        if self.worldInstance.loaded:

            if pressed(KeyboardButton.right()):
                self.model.setH(self.model, -1.0)
                self.model.setR(self.model, 1.0)
            elif pressed(KeyboardButton.left()):
                self.model.setH(self.model, 1.0)
                self.model.setR(self.model, -1.0)
            if pressed(KeyboardButton.up()):
                self.model.setP(self.model, 2)
                if self.speed > 0:
                    if self.speed < self.MIN_SPEED:
                        self.speed -= self.SPEED_CHANGE_RATE
            elif pressed(KeyboardButton.down()):
                self.model.setP(self.model, -2)
                if self.speed < self.TERMINAL_SPEED:
                    self.speed += self.SPEED_CHANGE_RATE

            if self.model.getP() < 0:
                self.model.setP(self.model, 0.5)
            elif self.model.getP() > 0:
                self.model.setP(self.model, -0.5)
            if self.model.getP() > -0.9 and self.model.getP() < 0.9:
                self.model.setP(0)

            if self.model.getR() < 0:
                self.model.setR(self.model, 0.5)
            elif self.model.getR() > 0:
                self.model.setR(self.model, -0.5)
            if self.model.getR() > -0.5 and self.model.getR() < 0.5:
                self.model.setR(0)

            if self.model.getP() == -180:
                self.model.setP(180)

            self.model.setY(self.model, self.speed * globalClock.getDt())
            if not self.crashed and self.model.getZ(render) <= self.CRASH_Z:
                self.crashed = True
                base.messenger.send("game-crashed")
            base.camera.setPos(self.model, 0, -9, 2)
            base.camera.lookAt(self.model)
        #print(self.speed)

        return task.cont



g = Game()
g.run()

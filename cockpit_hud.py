# DesertPatrol - cockpit_hud
# Autor: Arthur Martins
# Descrição: HUD do cockpit exibindo objetivo, timer e controles durante a missão

from direct.gui.DirectGui import *
from direct.gui.OnscreenText import *
import time

class Hud:
    def __init__(self):
        self.frame = DirectFrame(
            frameSize = (base.a2dLeft, base.a2dRight,
                         base.a2dBottom, base.a2dTop),
            frameColor = (0, 0, 0, 0),
            image_scale = (2, 0, 1),
            enableEdit = False,
            )
        self.frame.setTransparency(0)

        self.title = DirectLabel(
            scale = 0.045,
            pos = (0, 0, 0.86),
            text = "Missão Atual",
            text_fg = (0.96, 0.92, 0.78, 1),
            text_shadow = (0, 0, 0, 1),
            frameColor = (0.01, 0.012, 0.016, 0.58),
            pad = (0.03, 0.02),
            enableEdit = False,
            )

        self.createBtn("Sair", 0.78, ["game-quit"])
        self.createBtn("Encontrei!", 0.61, ["game-finished"])
        self.title.reparentTo(self.frame)

        self.timer = OnscreenText(
            text = "",
            mayChange = True,
            pos = (0.76, 0.9),
            fg = (0.96, 0.92, 0.78, 1),
            shadow = (0, 0, 0, 1),
            scale = 0.045)
        self.timer.reparentTo(self.frame)

        self.hide()

    def createBtn(self, text, verticalPos, commands):
        btn = DirectButton(
            text = text,
            text_fg = (1, 0.96, 0.86, 1),
            text_scale = 0.026,
            text_pos = (0, 0),
            scale = 2.35,
            pos = (-0.9, 0, verticalPos),
            relief = DGG.FLAT,
            frameColor = (
                (0.82, 0.2, 0.08, 0.86),
                (1.0, 0.34, 0.12, 0.95),
                (0.55, 0.08, 0.04, 0.9),
                (0.16, 0.16, 0.18, 0.75),
            ),
            pad = (0.055, 0.009),
            command = base.messenger.send,
            extraArgs = commands,
            rolloverSound = None,
            clickSound = None)
        btn.reparentTo(self.frame)

    def show(self):
        self.frame.show()

    def hide(self):
        self.frame.hide()

    def hudTask(self, task):
        self.timer.setText(str(self.missionLength - int(time.time() - self.startTime)) + " segundos restantes")
        return task.cont

    def initialise(self, currentMission, missionLength):
        self.startTime = time.time()
        self.missionLength = missionLength
        self.title["text"] = currentMission

# DesertPatrol - briefing
# Autor: Arthur Martins
# Descrição: Tela de briefing que exibe o objetivo da missão antes do início

from direct.gui.DirectGui import *
from panda3d.core import *
from engine import MenuBase

class MissionScreen(MenuBase):
    def __init__(self):
        MenuBase.__init__(self)

        self.title = self.makeTitle(text = "Missão", pos = (0, 0.22), scale = 0.07)
        self.title["text_fg"] = (0.86, 0.9, 0.92, 1)
        self.title.reparentTo(self.frame)

        self.startBtn = self.makeButton(text = "Iniciar", pos = (0, -0.62), event = "mission-start")
        self.startBtn.reparentTo(self.frame)

        self.hide()

    def showWithTitle(self, titleText):
        self.show()
        self.title["text"] = titleText

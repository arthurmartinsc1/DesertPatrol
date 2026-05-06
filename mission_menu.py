# DesertPatrol - mission_menu
# Autor: Arthur Martins
# Descrição: Menu de seleção de missões de reconhecimento disponíveis

from direct.gui.DirectGui import *
from engine import MenuBase

class MissionSelect(MenuBase):
    def __init__(self):
        MenuBase.__init__(self)

        self.title = self.makeTitle(text = "Selecionar Missão", pos = (0, 0.42), scale = 0.11)
        self.title.reparentTo(self.frame)

        self.m1 = self.makeButton(text = "Rota de Contrabando",  pos = (0, 0.08),  event = "missionselect-m1", scale = 0.04)
        self.m2 = self.makeButton(text = "Infiltração Nômade",   pos = (0, -0.16), event = "missionselect-m2", scale = 0.04)

        for btn in [self.m1, self.m2]:
            btn.reparentTo(self.frame)


        self.hide()

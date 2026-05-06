# DesertPatrol - settings
# Autor: Arthur Martins
# Descrição: Gerenciamento das configurações do jogo

from engine import MenuBase

class Settings(MenuBase):
    def __init__(self):
        MenuBase.__init__(self)

        self.title = self.makeTitle(text = "Configurações", pos = (0, 0.34), scale = 0.12)
        self.title.reparentTo(self.frame)

        self.info = self.makeTitle(
            text = "Use as setas para pilotar\nEncontrei! abre o relatório da missão",
            pos = (0, 0.05),
            scale = 0.055)
        self.info["text_fg"] = (0.78, 0.82, 0.86, 1)
        self.info.reparentTo(self.frame)

        self.backBtn = self.makeButton(text = "Voltar", pos = (0, -0.35), event = "settings-back")
        self.backBtn.reparentTo(self.frame)

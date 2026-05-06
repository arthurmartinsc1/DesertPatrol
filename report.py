# DesertPatrol - report
# Autor: Arthur Martins
# Descrição: Tela de relatório pós-missão com pergunta e verificação da resposta do piloto

from direct.gui.DirectGui import *
from engine import MenuBase

class Debrief(MenuBase):
    def __init__(self):
        MenuBase.__init__(self)

        self.title = self.makeTitle(text = "Aguardando pergunta", pos = (0, 0.28), scale = 0.075)
        self.title["text_fg"] = (0.86, 0.9, 0.92, 1)
        self.title.reparentTo(self.frame)


        #All buttons are set to sending the event debrief-wrong (for a wrong answer)
        #by default. This is changed to debreif-correct for the button containing the correct answer
        #by self.setButtons
        self.btn1 = self.makeButton(text = "3", pos = (-0.34, -0.48), event = "debrief-wrong", hasPadding = False)
        self.btn2 = self.makeButton(text = "5", pos = (0, -0.48), event = "debrief-wrong", hasPadding = False)
        self.btn3 = self.makeButton(text = "2", pos = (0.34, -0.48), event = "debrief-wrong", hasPadding = False)

        for btn in [self.btn1, self.btn2, self.btn3]:
             btn.reparentTo(self.frame)

        self.backBtn = self.makeButton(text = "Voltar", pos = (-0.62, -0.78), event = "debrief-back", scale = 0.028)
        self.backBtn.reparentTo(self.frame)

        self.restartBtn = self.makeButton(text = "Reiniciar", pos = (-0.62, -0.62), event = "debrief-restart", scale = 0.028)
        self.restartBtn.reparentTo(self.frame)

        self.hide()
        self.chosenAnswer = False

    def setTitle(self, newTitle, isAnswer = True):
        """isAnswer should be true if you are setting the title to a chosen answer"""
        if not self.chosenAnswer:
            self.title["text"] = newTitle
        self.backBtn.show()
        if isAnswer:
            self.chosenAnswer = True

    def setButtons(self, currentMission):
        buttonValues = currentMission.options #set the btn values to the options for the mission
        correctAnswer = currentMission.correctAnswer
        assert type(buttonValues) in (list, tuple) and len(buttonValues) == 3, "Values must be a list of length 3"
        self.btn1["text"] = buttonValues[0]
        self.btn2["text"] = buttonValues[1]
        self.btn3["text"] = buttonValues[2]

        for button in (self.btn1, self.btn2, self.btn3):
            button["extraArgs"] = ["debrief-wrong"]
            if button["text"] == correctAnswer:
                #Change the command to sending event debrief-correct
                button["extraArgs"] = ["debrief-correct"]


    def initialise(self):
        """Re-initialises the screen"""
        self.chosenAnswer = False
        self.title["text"] = ""


class GameOverScreen(MenuBase):
    def __init__(self):
        MenuBase.__init__(self)

        self.title = self.makeTitle(text = "GAME OVER", pos = (0, 0.28), scale = 0.15)
        self.title["text_fg"] = (1.0, 0.24, 0.12, 1)
        self.title.reparentTo(self.frame)

        self.message = self.makeTitle(
            text = "A aeronave caiu no chão",
            pos = (0, 0.02),
            scale = 0.06)
        self.message["text_fg"] = (0.86, 0.9, 0.92, 1)
        self.message.reparentTo(self.frame)

        self.menuBtn = self.makeButton(text = "Sair para o menu", pos = (0, -0.36), event = "gameover-menu", scale = 0.035)
        self.menuBtn.reparentTo(self.frame)

from engine import game
import pygame

class AGame(game.Game):
    def onInit(self):
        self.gfxEngine.screenColor = pygame.Color(80, 80, 75)
        
    def onStep(self):
        if self.input.keyReleased(pygame.K_ESCAPE):
            self.finished = True

from engine import game
import pygame

class AGame(game.Game):
    def onInit(self):
        self.gfxEngine.screenColor = pygame.Color(80, 80, 75)
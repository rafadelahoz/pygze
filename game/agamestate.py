import pygame
import random

from engine.gamestate import GameState
from engine.graphics import Stamp

from aentity import Dude

class AGameState(GameState):
    def init(self, game):
        GameState.init(self, game)
        self.bgColor = pygame.Color(100, 100, 100)
        self.gfxDude = Stamp(self.game.gfxEngine, "dude.png")
        for i in range(1, 10):
            d = Dude(i*24, i*16, self.game, self)
            d.graphic.alpha = 0.1+random.random()
            d.graphic.color = pygame.Color(random.randrange(0, 255, 1), random.randrange(0, 255, 1), random.randrange(0, 255, 1))
            d.graphic.xScale = 1.5
            d.graphic.yScale = 2.0
            self.add(d)
        
    def update(self):
        GameState.update(self)
        
    def render(self, gfxEngine):
        gfxEngine.clearRender(pygame.Color(234, 58, 67))
        GameState.render(self, gfxEngine)

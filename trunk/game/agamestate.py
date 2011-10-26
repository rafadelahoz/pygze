import pygame

from engine.gamestate import GameState
from engine.graphics import Stamp

from aentity import Dude

class AGameState(GameState):
    def init(self, game):
        GameState.init(self, game)
        self.bgColor = pygame.Color(100, 100, 100)
        self.gfxDude = Stamp(self.game.gfxEngine, "dude.png")
        for i in range(1, 10):
            self.add(Dude(i*24, i*16, self.game, self))
        
    def update(self):
        GameState.update(self)
        
    def render(self, gfxEngine):
	gfxEngine.clearRender(pygame.Color(234, 58, 67))
        GameState.render(self, gfxEngine)
        #gfxEngine.clearRender(pygame.Color(100, 100, 240))
        #self.gfxDude.render(32, 32)

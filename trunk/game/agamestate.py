from engine.gamestate import GameState
import pygame 

class AGameState(GameState):
    def init(self, game):
        GameState.init(self, game)
        print "AGameState initiated"
        self.bgColor = pygame.Color(100, 100, 100)
        
    def update(self):
        print "AGameState updating!"
        GameState.update(self)
        
    def render(self, gfxEngine):
        GameState.render(self, gfxEngine)
        gfxEngine.clearRender(pygame.Color(100, 100, 240))
        print "AGameState rendering!"
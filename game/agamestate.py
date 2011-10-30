import pygame

from engine.gamestate import GameState

from aentity import Dude, Other

class AGameState(GameState):
    def init(self):
        GameState.init(self)
        self.collisionManager.setGroups(["player", "other"])
        self.add(Dude(40, self.game.gfxEngine.renderSurface.get_height() / 2 - 48, self.game, self))
        self.add(Other(300, 48, self.game, self))
        
    def update(self):
        GameState.update(self)
        
    def render(self, gfxEngine):
        gfxEngine.clearRender(pygame.Color(234, 58, 67))
        GameState.render(self, gfxEngine)

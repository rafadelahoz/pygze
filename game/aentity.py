from engine.entity import Entity
from engine.graphics import Stamp

class Dude(Entity):
    def init(self):
        self.graphic = Stamp(self.game.gfxEngine, "dude.png")
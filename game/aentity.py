from engine.entity import Entity
from engine.graphics import Stamp
import random

class Dude(Entity):
    def init(self):
        self.graphic = Stamp(self.game.gfxEngine, "dude.png")

    def onStep(self):
	self.x += random.randint(-10, 10)


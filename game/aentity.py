import random

import pygame
from pygame import gfxdraw

from engine.entity import Entity
from engine.graphics import Stamp

class Dude(Entity):
    def init(self):
        self.graphic = Stamp(self.game.gfxEngine, "dude.png")

    def onStep(self):
        self.graphic.rotation += random.random()*10
        self.x += random.randint(-10, 10)
        
    def onRender(self):
        Entity.onRender(self)
        gfxdraw.hline(self.game.gfxEngine.renderSurface, self.x-2, self.x+2, self.y, (255, 255, 255))
        gfxdraw.vline(self.game.gfxEngine.renderSurface, self.x, self.y-2, self.y+2, (255, 255, 255))
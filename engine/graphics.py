import pygame
from pygame import locals

from engine.utils import config

class Graphic:
    def __init__(self, gfxEngine):
        self.gfxEngine = gfxEngine
        self.color = pygame.Color(255, 255, 255)
        self.xScale = 1.0
        self.yScale = 1.0
        self.rotation = 0.0
        self.alpha = 1.0

    def update(self):
        pass

    def render(self, x, y):
        if config.fastRender:
            self.fastRender(x, y)
        else:
            self.fullRender(x, y)
    
    def fastRender(self, x, y):
        pass
    
    def fullRender(self, x, y):
        pass

class Stamp(Graphic):
    def __init__(self, gfxEngine, path):
        Graphic.__init__(self, gfxEngine)
        self.image = pygame.image.load(path).convert()
    
    # Full effects render
    def fullRender(self, x, y):
        toRender = self.image.copy()
        # Color: not working (tints alpha too)
        if self.color != pygame.Color(255, 255, 255):
            toRender.fill(self.color, special_flags=locals.BLEND_RGB_MULT)
            toRender.set_colorkey(toRender.get_at((0, 0)))
        # Scale: working, warns about floats
        if self.xScale < 0 or self.yScale < 0:
            toRender = pygame.transform.flip(toRender, (self.xScale < 0), (self.yScale < 0))
        if self.xScale != 1.0 or self.yScale != 1.0:
            toRender = pygame.transform.scale(toRender, (self.image.get_width() * abs(self.xScale), self.image.get_height() * abs(self.yScale)))

        # Rotation: working but enlarges surface (solveable with an offset)
        if self.rotation != 0.0:
            toRender = pygame.transform.rotate(toRender, self.rotation)
    
        # Alpha: working
        if self.alpha != 1.0:
            toRender.set_alpha(self.alpha * 255)

        self.gfxEngine.renderSurface.blit(toRender, (x, y))
        
    # Fast render (just alpha and flip)
    def fastRender(self, x, y):
        # Alpha: working
        self.image.set_alpha(self.alpha * 255)
        # Flip
        if self.xScale < 0 or self.yScale < 0:
            self.gfxEngine.renderSurface.blit(pygame.transform.flip(self.image, (self.xScale < 0), (self.yScale < 0)), (x, y))
        else:
            self.gfxEngine.renderSurface.blit(self.image, (x, y))
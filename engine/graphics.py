import pygame

class Graphic:
    def __init__(self, gfxEngine):
        self.gfxEngine = gfxEngine
        
    def update(self):
        pass
    
    def render(self, x, y):
        pass
    
class Stamp(Graphic):
    def __init__(self, gfxEngine, path):
        Graphic.__init__(self, gfxEngine)
        self.image = pygame.image.load(path)
        
    def render(self, x, y):
        self.gfxEngine.renderSurface.blit(self.image, (x, y))
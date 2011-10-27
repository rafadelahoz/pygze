import pygame

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
        pass
    
class Stamp(Graphic):
    def __init__(self, gfxEngine, path):
        Graphic.__init__(self, gfxEngine)
        self.image = pygame.image.load(path)
        
    def render(self, x, y):
	toRender = self.image.copy()
	# Color
	if self.color != pygame.Color(255, 255, 255):
		toRender.fill(self.color, special_flags=BLEND_RGBA_MULT)
	# Scale
	if self.xScale < 0 or self.yScale < 0:
		toRender = pygame.transform.flip(toRender, (self.xScale < 0), (self.yScale < 0))
	if self.xScale != 1.0 or self.yScale != 1.0:
		toRender = pygame.transform.scale(toRender, (self.image.get_width()*self.xScale, self.image.get_height()*self.yScale))
	
	# Rotation
	if self.rotation != 0.0:
		toRender = pygame.transform.rotate(toRender, self.rotation)

	# Alpha
	if self.alpha != 1.0:
		toRender.set_alpha(self.alpha*255)
	
        self.gfxEngine.renderSurface.blit(toRender, (x, y))

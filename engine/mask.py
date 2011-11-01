import pygame

class Mask:
    def __init__(self, x= -1, y= -1, w= -1, h= -1):
        self.rect = pygame.Rect(x, y, w, h)
        self.maskType = "Mask"
        
    def updatePosition(self, x, y):
        self.rect.x = x
        self.rect.y = y
        
    # Fast collision checking for rects
    def collides(self, other):
        return self.rect.colliderect(other.rect)
    
    def update(self):
        pass
    
    def getX(self):
        return self.rect.x

    def getY(self):
        return self.rect.y
    
    def getW(self):
        return self.rect.w
    
    def getH(self):
        return self.rect.h
    
    def renderBounds(self, surface, color):
        pygame.draw.rect(surface, color, self.rect, 1)
            
class MaskBox(Mask):
    def __init__(self, w, h, x= -1, y= -1):
        Mask.__init__(self, x, y, w, h)
        self.maskType = "MaskBox"
    
    def updatePosition(self, x, y):
        Mask.updatePosition(self, x, y)
    
    def collides(self, other):
        return Mask.collides(self, other)

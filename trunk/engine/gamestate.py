from collisionManager import CollisionManager
import pygame

class GameState:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.collisionManager = CollisionManager()
        self.entities = []
        self.deathrow = []
        self.camera = None
        
    def _init(self, game):
        self.game = game
        self.init()
        
    def init(self):
        pass
    
    def update(self):
        # Init Step
        for ent in self.entities:
            ent.onInitStep()
        
        self.onStep()
        
        # Check collisions
        self.collisionManager.autoCollisions()
        
        # Update entities
        for ent in self.entities:
            ent.update()
        
        # End Step
        for ent in self.entities:
            ent.onEndStep()
            
        # Update camera
        if self.camera != None:
            self.camera.update()
            
        # Delete instances
        for ent in self.deathrow:
            self._remove(ent)
        self.deathrow = []
    
    def render(self, gfxEngine):
        self.game.gfxEngine.setActiveCamera(self.camera)
        self.renderBackground()
        for ent in sorted(self.entities, key=lambda entity: -entity.depth):
            ent._render(self.camera)
        self.renderForeground()

    def end(self):
        pass
    
    def clear(self):
        pass

    def add(self, entity):
        self.entities.append(entity)
        entity.onInit()
        
    def _remove(self, entity):
        self.entities.remove(entity)
        entity.onDestroy()
        del entity
        
    def remove(self, entity):
        if not entity in self.deathrow:
            self.deathrow.append(entity)

    def placeFree(self, entity, x, y, groups = "all"):
        return self.collisionManager.placeFree(entity, x, y, groups)
    
    def moveToContact(self, entity, x, y, groups = "all"):
        return self.collisionManager.moveToContact(entity, x, y, groups)
    
    def instanceCount(self, group):
        return self.collisionManager.instanceCount(group)
    
    def renderBackground(self):
        pass
    
    def renderForeground(self):
        pass
    
    def onStep(self):
        pass

class Camera:
    def __init__(self, x, y, w, h):
        self.rect = pygame.Rect(x, y, w, h)
        self.target = None
        
    def follow(self, entity):
        self.target = entity
        
    def update(self):
        if self.target != None:
            self.rect.x = self.target.x - self.rect.w/2
            self.rect.y = self.target.y - self.rect.h/2
    
    def move(self, (dx, dy)):
        self.rect.x += dx
        self.rect.y += dy
        
    def transform(self, x, y):
        return (x - self.rect.x, y - self.rect.y)
    
    def rectInView(self, rect):
        # return self.rect.contains(rect)
        if (rect.right < self.rect.left or
            rect.left > self.rect.right or
            rect.bottom < self.rect.top or
            rect.top > self.rect.bottom):
            return False
        else:
            return True 
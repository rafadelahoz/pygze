from engine.entity import Entity
from engine.graphics import Stamp
from engine.mask import MaskBox
import pygame

class Dude(Entity):
    def init(self):
        self.graphic = Stamp(self.game.gfxEngine, "dude.png")
        self.sp = 2
        self.facing = 0
        
        self.mask = MaskBox(64, 128)
        
        self.world.collisionManager.add(self, "player")
        self.world.collisionManager.subscribe("player", "other")
        
        self.joy = self.game.input.addJoystick()
        if not self.joy.isValid:
            del self.joy
            self.joy = None

    def onStep(self):
        self.graphic.alpha = 1.0
        
        if self.game.input.key(pygame.K_LEFT) or self.joy.getAxis(0) < -0.3:
            self.x -= self.sp
            self.facing = 1
        elif self.game.input.key(pygame.K_RIGHT) or self.joy.getAxis(0) > 0.3:
            self.x += self.sp
            self.facing = 0
            
        if self.facing == 0:
            self.graphic.xScale = 1
        else:
            self.graphic.xScale = -1
            
        if self.joy.buttonReleased(0):
            self.graphic.rotation += 5
            
        self.depth = self.y
        
    def onRender(self):
        Entity.onRender(self)
        pygame.draw.rect(self.game.gfxEngine.renderSurface, pygame.Color(10, 255, 20), pygame.Rect(self.mask.x, self.mask.y, self.mask.w, self.mask.h), 1)
        
    def onCollision(self, group, other):
        if group == "other":
            self.graphic.alpha = 0.5
        
class Other(Entity):
    def init(self):
        self.graphic = Stamp(self.game.gfxEngine, "dude.png");
        self.graphic.color = pygame.Color(100, 240, 100)
        self.sp = 2
        
        self.world.collisionManager.add(self, "other")
        self.world.collisionManager.subscribe("other", "player")
        
        self.mask = MaskBox(64, 128)
        
    def onStep(self):
        if self.game.input.keyReleased(pygame.K_z):
            self.graphic.xScale *= -1
        if self.game.input.keyPressed(pygame.K_z):
            self.graphic.yScale *= -1
        if self.game.input.key(pygame.K_LEFT):
            self.x += self.sp
        elif self.game.input.key(pygame.K_RIGHT):
            self.x -= self.sp
            
        self.depth = self.y
        
    def onRender(self):
        Entity.onRender(self)
        pygame.draw.rect(self.game.gfxEngine.renderSurface, pygame.Color(10, 255, 20), pygame.Rect(self.mask.x, self.mask.y, self.mask.w, self.mask.h), 1)

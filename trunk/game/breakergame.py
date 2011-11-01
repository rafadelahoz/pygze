# Arkanoid Style game
import pygame, random, math

from engine.game import Game
from engine.gamestate import GameState
from engine.entity import Entity
from engine.mask import MaskBox
from engine.graphics import Stamp

class BreakerGame(Game):
    def onStep(self):
        if self.input.keyPressed(pygame.K_ESCAPE):
            self.finished = True
            
class BreakerLevel(GameState):
    def init(self):
        self.collisionManager.setGroups(["ball", "brick", "bat"])
        self.collisionManager.subscribe("ball", "brick")
        self.collisionManager.subscribe("brick", "ball")
        self.collisionManager.subscribe("ball", "bat")
        
        self.bgColor = pygame.Color(random.randint(0, 120), 
                                    random.randint(0, 120), 
                                    random.randint(0, 120))
        self.generateLevel()
        
    def generateLevel(self):
        lwall = Wall(0, 8, self.game, self)
        lwall.rect = pygame.Rect(0, 8, 8, self.height-8)
        rwall = Wall(self.width-8, 8, self.game, self)
        rwall.rect = pygame.Rect(self.width-8, 8, 8, self.height-8)
        twall = Wall(0, 0, self.game, self)
        twall.rect = pygame.Rect(0, 0, self.width, 8)
        # bwall = Wall(0, self.height-8, self.game, self)
        # bwall.rect = pygame.Rect(0, self.height-8, self.width, 8)
        self.add(lwall)
        self.add(rwall)
        self.add(twall)
        # self.add(bwall)
        for i in range(32, self.width-32, 32):
            for j in range(32, 32+8*(3+random.randint(0,4)), 8):
                self.add(Brick(i, j, self.game, self))
                
        self.add(Bat(0, 0, self.game, self))
            
    def render(self, gfxEngine):
        self.game.gfxEngine.renderSurface.fill(self.bgColor)
        GameState.render(self, gfxEngine)
        
class Bat(Entity):
    def onInit(self):
        self.mask = MaskBox(24, 8)
        self.x = self.world.width/2-self.mask.getW()/2
        self.y = self.world.height-16
        self.color = pygame.Color(255, 255, 255)
        self.sp = 4
        self.joy = self.game.input.addJoystick()
        self.world.collisionManager.add(self, "bat")
                
    def onStep(self):
        if self.joy != None:
            if abs(self.joy.getAxis(0)) > 0.3:
                self.x += self.sp*self.joy.getAxis(0)
        
            if self.joy.buttonPressed(0):
                self.world.add(Ball(self.x+self.mask.getW()/2-4, self.y-8, self.game, self.world))
        
        if self.game.input.keyPressed(pygame.K_a):
            self.world.add(Ball(self.x+self.mask.getW()/2-4, self.y-8, self.game, self.world))
        
        if self.game.input.key(pygame.K_LEFT):
            self.x -= self.sp
        elif self.game.input.key(pygame.K_RIGHT):
            self.x += self.sp
        
        if self.x < 8:
            self.x = 8
        elif self.x > self.world.width-8-self.mask.getW():
            self.x = self.world.width-8-self.mask.getW()
        
    def onRender(self):
        pygame.draw.rect(self.game.gfxEngine.renderSurface, self.color, self.mask.rect)

class Ball(Entity):
    def onInit(self):
        self.sp = 4
        self.dir = random.randint(0, 18)*10
        self.mask = MaskBox(6, 6, offset=(1, 1))
        self.color = pygame.Color(255, 255, 255)
        self.world.collisionManager.add(self, "ball")
        self.ox = self.x
        self.oy = self.y
        self.graphic = Stamp(self.game.gfxEngine, "gfx/ball.png")
        
    def onStep(self):
        self.ox = self.x
        self.oy = self.y
        
        self.x = self.x - math.ceil(self.sp * math.cos(math.radians(self.dir)))
        self.y = self.y - math.ceil(self.sp * math.sin(math.radians(self.dir)))
                
        if self.x < 0 or self.x > self.world.width or self.y < 0 or self.y > self.world.height:
            self.world.collisionManager.remove(self, "ball")
            self.destroy()
            
        if self.dir == 0 or self.dir == 90 or self.dir == 180 or self.dir == 270:
            self.dir += random.randint(-10, 10)
        
    def onCollision(self, group, other):
        if group == "brick" or group == "bat":
            pos = self.getRelativePosition(other)
            self.x = self.ox
            self.y = self.oy
            if pos == 1 or pos == 7: # Top or bottom
                self.dir = 360-self.dir
            elif pos == 3 or pos == 5: # Left or Right
                if self.dir <= 180:
                    self.dir = 180 - self.dir
                else:
                    self.dir = 180 + (360-self.dir)
            else: # Corner
                if self.dir <= 180:
                    self.dir = 180+self.dir
                else:
                    self.dir = self.dir-180
                
            
    def getRelativePosition(self, other):
        mCenterx = self.mask.rect.x + self.mask.rect.w/2
        mCentery = self.mask.rect.y + self.mask.rect.h/2  
        
        if mCenterx < other.mask.rect.left:
            if mCentery < other.mask.rect.top: return 0
            elif mCentery > other.mask.rect.bottom: return 6
            else: return 3
        elif mCenterx > other.mask.rect.right:
            if mCentery < other.mask.rect.top: return 2
            elif mCentery > other.mask.rect.bottom: return 8
            else: return 5
        else:
            if mCentery < other.mask.rect.top: return 1
            elif mCentery > other.mask.rect.bottom: return 7
            else: return 4
            
        
    def onRender(self):
        Entity.onRender(self)
        pygame.draw.rect(self.game.gfxEngine.renderSurface, self.color, self.mask.rect)
        # self.mask.renderBounds(self.game.gfxEngine.renderSurface, pygame.Color(255, 0, 0))
        
    def onDestroy(self):
        print "Ball out"

class Wall(Entity):
    def onInit(self):
        self.color = self.world.bgColor+pygame.Color(35, 35, 35)
        self.mask = MaskBox(self.rect.width, self.rect.h)
        self.world.collisionManager.add(self, "brick")
        
    def onRender(self):
        pygame.draw.rect(self.game.gfxEngine.renderSurface, self.color, self.mask.rect, 0)
        # self.mask.renderBounds(self.game.gfxEngine.renderSurface, pygame.Color(255, 0, 0))

class Brick(Entity):
    def onInit(self):
        self.color = pygame.Color(100+random.randint(0, 150), 
                                    100+random.randint(0, 150), 
                                    100+random.randint(0, 150))
        self.mask = MaskBox(32, 8)
        self.world.collisionManager.add(self, "brick")
        self.hp = 1
        
    def onCollision(self, group, other):
        if group == "ball":
            other.sp += 0.1
            self.destroy()
            
    def onRender(self):
        pygame.draw.rect(self.game.gfxEngine.renderSurface, self.color, self.mask.rect, 0)
        # self.mask.renderBounds(self.game.gfxEngine.renderSurface, pygame.Color(255, 0, 0))
    
    def onDestroy(self):
        self.world.collisionManager.remove(self, "brick")

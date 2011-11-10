from engine.entity import Entity
from engine.game import Game
from engine.gamestate import GameState, Camera
from engine.graphics import Spritemap, Anim, Stamp
from engine.mask import MaskBox
import pygame
import random

from engine.fontmanager import cFontManager

pygame.font.init()

class PlatformGame(Game):
    def onInit(self):
        self.changeGameState(Level(1024, 768))
        
    def onStep(self):
        if self.input.keyPressed(pygame.K_ESCAPE):
            self.finished = True
    
class Level(GameState):
    def init(self):
        self.camera = Camera(0, 0, 320, 240)
        self.collisionManager.setGroups(["brick", "player", "bullet"])
        self.collisionManager.subscribe("player", "brick")
        self.collisionManager.subscribe("bullet", "brick")
        self.bgColor = pygame.Color(98, 98, 98)
        lwall = Wall(0, self.height-16, self.game, self)
        lwall.rect = pygame.Rect(0, self.height-16, self.width, 16)
        self.add(lwall)
        
        for _i in range(1, 200):
            x = random.randint(0, self.width)
            y = random.randint(0, self.height)
            wall = Wall(x, y, self.game, self)
            wall.rect = pygame.Rect(x, y, 
                        8+random.randint(0, 32), 8+random.randint(0, 32))
            self.add(wall)
        p = Player(150, 140, self.game, self)
        self.add(p)
        self.camera.follow(p)
        
        self.smx, self.smy, self.lmx, self.lmy = 0, 0, 0, 0

class Wall(Entity):
    def onInit(self):
        self.color = self.world.bgColor+pygame.Color(35, 35, 35)
        self.mask = MaskBox(self.rect.width, self.rect.h)
        self.world.collisionManager.add(self, "brick")
        
    def inView(self, camera):
        if camera == None:
            return True
        return camera.rectInView(self.mask.rect)
    
    def onRender(self):
        self.game.gfxEngine.renderRect(self.mask.rect.copy(), self.color)

class Bullet(Entity):
    def onInit(self):
        self.mask = MaskBox(6, 4)
        self.graphic = Stamp(self.game.gfxEngine, "../gfx/megabullet.png")
        self.world.collisionManager.add(self, "bullet")
    
    def onStep(self):
        self.x += self.sp
        
        if self.x < 0 or self.x > self.world.width:
            self.destroy()
        
    def onCollision(self, group, other):
        if group == "brick":
            self.moveToContact(self.x, self.y, ["brick"])
            self.destroy()
            
    def onDestroy(self):
        self.world.collisionManager.remove(self, "bullet")

class Player(Entity):
    def onInit(self):
        self.graphic = Spritemap(self.game.gfxEngine, "../gfx/mega.png", 32, 32);
        self.graphic.addAnim("stand", Anim([0], 1))
        self.graphic.addAnim("walk", Anim([1, 2, 3, 2], 0.3, True))
        self.graphic.addAnim("jump", Anim([5], 1))
        self.graphic.addAnim("shoot", Anim([4], 0.2, False, self.stopShooting))
        self.graphic.playAnim("stand")
        
        self.world.collisionManager.add(self, "player")
        self.mask = MaskBox(22, 24, offset=(5, 8))
        
        self.sp = 3
        self.gravity = 0.5
        self.vspeed = 0
        self.jumpPow = 7
        
        self.state = "stand"
        self.dir = "left"
        self.moving = False
        self.dx = self.x
        
        self.fontManager = cFontManager(((None, 24), ('arial', 18), ('arial', 24),
            ('courier', 12)))
        
    def onStep(self):
        nx, ny = self.x, self.y
        
        onAir = self.placeFree(self.x, self.y+1, ["brick"])
         
        if not onAir:
            if not self.state == "shoot":
                self.state = "stand"
                self.vspeed = 0
                if self.game.input.key(pygame.K_a):
                    self.vspeed = -self.jumpPow
                    self.state = "jump"
                elif (self.game.input.keyPressed(pygame.K_s) and 
                    self.world.instanceCount("bullet") < 3):
                    b = None
                    if self.dir == "left":
                        self.dx = self.x - 4
                        b = Bullet(self.x, self.y+17, self.game, self.world)
                        b.sp = -8
                    elif self.dir == "right":
                        self.dx = self.x + 4
                        b = Bullet(self.x+26, self.y+17, self.game, self.world)
                        b.sp = 8
                    self.state = "shoot"
                    self.graphic.playAnim("shoot")
                    self.world.add(b)
        else:
            self.state = "jump"
            if self.game.input.keyReleased(pygame.K_a) and self.vspeed < 0:
                self.vspeed /= 2
        
        self.moving = False
        if not self.state == "shoot":
            if self.game.input.key(pygame.K_LEFT):
                nx -= self.sp
                self.dir = "left"
                self.moving = True
            elif self.game.input.key(pygame.K_RIGHT):
                nx += self.sp
                self.dir = "right"
                self.moving = True
        
        ny += self.vspeed
        self.vspeed += self.gravity
        
        if self.game.input.key(pygame.K_LCTRL):
            self.x, self.y = nx, ny
        else:
            if not self.placeFree(nx, ny, ["brick"]):
                if not self.placeFree(self.x, ny):
                    self.moveToContact(self.x, ny, ["brick"])
                    self.vspeed = 0
                else:
                    self.y = ny
                if not self.placeFree(nx, self.y):
                    self.moveToContact(nx, self.y, ["brick"])
                    self.moving = False
                else:
                    self.x = nx
            else:
                self.x, self.y = nx, ny

        if not self.state == "shoot":
            self.dx = self.x
                
        if self.state == "jump":
            self.graphic.playAnim("jump")
        elif self.state == "stand":
            if self.moving:
                self.graphic.playAnim("walk")
            else:
                self.graphic.playAnim("stand")

        if self.dir == "left":
            self.graphic.xScale = 1.0
        else:
            self.graphic.xScale = -1.0
            
    def stopShooting(self):
        self.state = "stand"
        
    def onRender(self):
        self.graphic.render(self.dx, self.y)
        self.fontManager.Draw(self.game.gfxEngine.renderSurface, 
                              'arial', 18, "ANUS", 
                              self.world.camera.transform(self.world.camera.getX(),
                                                          self.world.camera.getY()),
                              pygame.Color(255, 255, 255))
        
game = PlatformGame(320, 240, title="Platformer Game Test", scaleH=2, scaleV=2)

while not game.finished:
    game.update()
    
game.end()

print "Platformer end."

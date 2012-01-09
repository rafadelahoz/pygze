from engine import game
from engine.gamestate import GameState
from engine.entity import Entity
from engine.graphics import Stamp
from engine.mask import MaskBox
import pygame

class AGame(game.Game):
    def onInit(self):
        self.gfxEngine.screenColor = pygame.Color(80, 80, 75)
        
    def onStep(self):
        if self.input.keyReleased(pygame.K_ESCAPE):
            self.finished = True
            
class AGameState(GameState):
    def init(self):
        GameState.init(self)
        self.collisionManager.setGroups(["player", "other"])
        self.add(Dude(40, self.game.gfxEngine.renderSurface.get_height() / 2 - 48, self.game, self))
        self.add(Other(300, 48, self.game, self))
        
    def update(self):
        GameState.update(self)
        
    def render(self, gfxEngine):
        gfxEngine.clearRender(pygame.Color(234, 58, 67))
        GameState.render(self, gfxEngine)

class Dude(Entity):
    def init(self):
        self.graphic = Stamp(self.game.gfxEngine, "../gfx/dude.png")
        self.sp = 2
        self.facing = 0
        
        self.mask = MaskBox(64, 128)
        
        self.world.collisionManager.add(self, "player")
        self.world.collisionManager.subscribe("player", "other")
        
        self.joy = self.game.input.addJoystick()
        if self.joy == None:
            return
        if not self.joy.isValid:
            del self.joy
            self.joy = None

    def onStep(self):
        self.graphic.alpha = 1.0
        
        if self.game.input.key(pygame.K_LEFT) or (self.joy != None and self.joy.getAxis(0) < -0.3):
            self.x -= self.sp
            self.facing = 1
        elif self.game.input.key(pygame.K_RIGHT) or (self.joy != None and self.joy.getAxis(0) > 0.3):
            self.x += self.sp
            self.facing = 0
            
        if self.facing == 0:
            self.graphic.xScale = 1
        else:
            self.graphic.xScale = -1
            
        if self.joy != None and self.joy.buttonReleased(0):
            self.graphic.rotation += 5
            
        self.depth = -self.y
        
    #def onRender(self):
    #    Entity.onRender(self)
    #    self.mask.renderBounds(self.game.gfxEngine.renderSurface, pygame.Color(10, 255, 20))
        
    def onCollision(self, group, other):
        if group == "other":
            self.graphic.alpha = 0.5
        
class Other(Entity):
    def init(self):
        self.graphic = Stamp(self.game.gfxEngine, "../gfx/dude.png");
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
        
    #def onRender(self):
    #    Entity.onRender(self)
    #    self.mask.renderBounds(self.game.gfxEngine.renderSurface, pygame.Color(10, 255, 20))

game = AGame(320, 240, title="A Game Test", scaleH=2, scaleV=2, fps=30)
game.changeGameState(AGameState(320, 240))

while not game.finished:
    game.update()

game.end()

print "End!"
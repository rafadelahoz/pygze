from engine.entity import Entity
from engine.game import Game
from engine.gamestate import GameState
from engine.graphics import Spritemap, Anim
import pygame
import random

class AnimationTestGame(Game):
    def onInit(self):
        self.changeGameState(Level(160, 140))
    
class Level(GameState):
    def init(self):
        for i in range(0, 10):
            for j in range(0, 8):
                self.add(Player(i*16, j*16, self.game, self))
        # self.add(Player(72, 62, self.game, self))
        
    def renderForeground(self):
        c = pygame.Color(self.game.input.mouseButton(0)*255, 
                         self.game.input.mouseButton(1)*255,
                         self.game.input.mouseButton(2)*255);
        (x, y) = self.game.input.getMousePosition(self.game.gfxEngine)
        pygame.draw.rect(self.game.gfxEngine.renderSurface,
                         c, (x, y, 2, 2))
        
class Player(Entity):
    def onInit(self):
        self.graphic = Spritemap(self.game.gfxEngine, "../gfx/char.png", 16, 16)
        self.graphic.addAnim("stand", Anim([0], 1))
        self.graphic.addAnim("walk", Anim([i for i in range(32, 40)], 0.5, True))
        self.graphic.addAnim("run", Anim([i for i in range(40, 48)], 0.5, True))
        self.graphic.addAnim("crouch", Anim([16, 17, 18, 19], 0.5, False))
        self.graphic.addAnim("up", Anim([19, 18, 17, 16], 0.5, False))
        self.graphic.playAnim("stand")
    
    def run(self):
        self.graphic.playAnim("run")
    
    def onStep(self):
        if self.game.input.key(pygame.K_LEFT):
            self.graphic.xScale = -1
            self.graphic.playAnim("run")
        elif self.game.input.keyPressed(pygame.K_RIGHT):
            self.graphic.xScale = 1
            if self.graphic.currentAnim == "crouch":
                self.graphic.playAnim("up", callback=self.run)
            else:
                self.graphic.playAnim("run")
        elif self.game.input.key(pygame.K_DOWN):
            if self.graphic.currentAnim != "crouch":
                self.graphic.playAnim("crouch")
        elif self.game.input.key(pygame.K_UP):
            if self.graphic.currentAnim == "crouch":
                self.graphic.playAnim("up")
                
        if random.choice(range(1, 24)) == 4:
            self.graphic.setAnimSpeed(random.random()*0.75)
        
game = AnimationTestGame(160, 140, title="AnimationTest", scaleH=4, scaleV=4)

while not game.finished:
    game.update()

game.end()

print "End!"
from engine.entity import Entity
from engine.game import Game
from engine.gamestate import GameState
from engine.graphics import Spritemap, Anim
import pygame

class AnimationTestGame(Game):
    def onInit(self):
        self.changeGameState(Level(160, 140))
    
class Level(GameState):
    def init(self):
        self.add(Player(72, 62, self.game, self))
        
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
            self.graphic.playAnim("walk")
        elif self.game.input.keyPressed(pygame.K_RIGHT):
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
        
game = AnimationTestGame(160, 140, title="AnimationTest", scaleH=3, scaleV=3)

while not game.finished:
    game.update()

game.end()

print "End!"
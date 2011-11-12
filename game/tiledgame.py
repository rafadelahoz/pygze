from engine.entity import Entity
from engine.game import Game
from engine.gamestate import GameState, Camera
from engine.graphics import Tileset, Tilemap, SparseTilemap
import pygame
import random

class TiledGame(Game):
    def onInit(self):
        self.changeGameState(TiledState(320, 240))

class TiledState(GameState):
    def init(self):
        self.camera = Camera(0, 0, 160, 140)
        self.add(Map(0, 0, self.game, self))
        
    def onStep(self):
        dx, dy = 0, 0
        if self.game.input.key(pygame.K_LEFT):
            dx = -2
        elif self.game.input.key(pygame.K_RIGHT):
            dx = +2
        if self.game.input.key(pygame.K_UP):
            dy = -2
        elif self.game.input.key(pygame.K_DOWN):
            dy = +2
            
        self.camera.move((dx, dy))
        
class Map(Entity):
    def onInit(self):
        tileset = Tileset(self.game.gfxEngine, "../gfx/tset.png", 8, 8)
        self.graphic = Tilemap(self.game.gfxEngine)
        self.graphic.setTileset(tileset)
        self.graphic.setTilemap(
            [[random.randint(0, 1) for _j in range(0, 240/8)] 
             for _i in range(0, 320/8)])
        
        self.overlay = SparseTilemap(self.game.gfxEngine, 320/16, 240/16)
        self.overlay.setTileset(
                        Tileset(self.game.gfxEngine, "../gfx/overtset.png", 
                                16, 16))
        for _i in range(0, random.randint(10, 60)):
            self.overlay.setTile((random.randint(0, (320/16)-1), 
                                  random.randint(0, (240/16)-1)), 
                                 random.randint(0,1))
        
    def onStep(self):
        if self.game.input.mousePressed(0): 
            (x, y) = self.game.input.getMousePosition(self.game.gfxEngine)
            tid = self.graphic.getTile(self.graphic.getTileCoordsAt((x, y)))
            self.graphic.setTile(self.graphic.getTileCoordsAt((x, y)), 
                                 (tid+1)%2)
            
    def onRender(self):
        self.graphic.render(self.x, self.y)
        self.overlay.render(self.x, self.y)
        
game = TiledGame(160, 140, title="Tiled Game Test", scaleH=2, scaleV=2)
while not game.finished:
    game.update()
    
game.end()
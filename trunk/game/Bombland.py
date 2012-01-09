'''
Created on 08/01/2012

@author: Rafa
'''
from engine.entity import Entity
from engine.game import Game
from engine.gamestate import GameState
from engine.graphics import Spritemap, Anim, Tileset, Tilemap
from engine.mask import MaskBox
import math
import pygame
import random

class BombGame(Game):
    def onInit(self):
        self.changeGameState(BombLevel(320, 240))
        
    def onStep(self):
        if self.input.keyPressed(pygame.K_ESCAPE):
            self.finished = True
        
class BombLevel(GameState):
    def init(self):
        print "Level 1"
        
        self.collisionManager.setGroups(['player', 'solid', 'bomb', 'destructible', 'boom', 'enemy'])
        
        self.collisionManager.subscribe('player', 'solid')
        self.collisionManager.subscribe('player', 'destructible')
        self.collisionManager.subscribe('player', 'boom')
        self.collisionManager.subscribe('player', 'bomb')
        self.collisionManager.subscribe('player', 'enemy')
        
        self.collisionManager.subscribe('destructible', 'boom')
        
        self.collisionManager.subscribe('bomb', 'boom')
        
        self.collisionManager.subscribe('boom', 'destructible')
        self.collisionManager.subscribe('boom', 'solid')
        
        self.add(Map(0, 0, self.game, self))
        self.add(Bomber(320/2, 240/2, self.game, self))
        
    def onStep(self):
        if self.game.input.mousePressed(0): 
            (x, y) = self.game.input.getMousePosition(self.game.gfxEngine)
            (x, y) = ((x // 16)*16, (y // 16)*16)
            self.add(Destructible(x, y, self.game, self))
        
class Map(Entity):
    def onInit(self):
        tileset = Tileset(self.game.gfxEngine, '../gfx/bombland/terrain.png', 16, 16)
        
        self.graphic = Tilemap(self.game.gfxEngine)
        self.graphic.setTileset(tileset)
        self.graphic.setTilemap([[random.randint(0, 1) for _j in range(0, 240/16)] 
             for _i in range(0, 320/16)])

        for _i in range(0, 320/16):
            for _j in range(0, 240/16):
                # Spawn a crate
                if random.randint(0, 15) == 5:
                    # Deleting the underlying solid, if present
                    if self.graphic.getTile((_i, _j)) == 1:
                        self.graphic.setTile((_i, _j), 0)
                    self.world.add(Destructible(_i*16, _j*16, self.game, self.world))
                    continue
                    
                if self.graphic.getTile((_i, _j)) == 1:
                    self.world.add(Solid(_i*16, _j*16, self.game, self.world))
    def onStep(self):
        if self.game.input.mousePressed(2): 
            (x, y) = self.game.input.getMousePosition(self.game.gfxEngine)
            (x, y) = ((x // 16), (y // 16))
            self.graphic.setTile((x, y), (self.graphic.getTile((x, y))+1)%2)
                
class Solid(Entity):
    def onInit(self):
        self.mask = MaskBox(16, 16, self.x, self.y)
        self.world.collisionManager.add(self, 'solid')
        
    #def onRender(self):
    #    self.game.gfxEngine.renderRect(self.mask.rect.copy(), pygame.Color(35, 35, 35), 1)
        
class Destructible(Entity):
    def onInit(self):
        self.mask = MaskBox(16, 16, self.x, self.y)
        self.world.collisionManager.add(self, 'destructible')
        
        self.graphic = Tilemap(self.game.gfxEngine)
        self.graphic.setTileset(Tileset(self.game.gfxEngine, '../gfx/bombland/things.png', 16, 16))
        self.graphic.setTilemap([[0]])
        
        self.hp = 1
        
        self.depth = -(self.y // 16)
        
    def onCollision(self, group, other):
        if group == 'boom':
            self.destroy()
            
    def onDestroy(self):
        self.world.collisionManager.remove(self, 'destructible')
        
class Bomb(Entity):
    def onInit(self):
        self.mask = MaskBox(16, 16, self.x, self.y)
        
        self.world.collisionManager.add(self, 'bomb')
        
        self.graphic = Spritemap(self.game.gfxEngine, '../gfx/bombland/boom.png', 16, 16)
        self.graphic.addAnim('normal', Anim([1, 2], 0.1, True))
        self.graphic.addAnim('fast', Anim([1, 2], 0.4))
        self.graphic.playAnim('normal')
        
        self.initialTimer = self.game.targetfps * 5 
        self.timers[0] = self.initialTimer
        
    def onStep(self):
        # self.depth = -(self.y // 16)
        self.passable = not self.placeFree(self.x, self.y, ['player'])
        
        if self.timers[0] < self.initialTimer / 4:
            self.graphic.playAnim('fast')
            
    def onTimer(self, timer):
        if timer == 0:
            self.destroy()
            
    def onCollision(self, group, other):
        if group == 'boom':
            self.destroy()
            
    def onDestroy(self):
        self.world.collisionManager.remove(self, 'bomb')
        _s = ExplosionSegment(self.x, self.y, self.game, self.world)
        _s.segmentType = 'c'
        _s.segmentCounter = 3
        self.world.add(_s)
        
    '''def onRender(self):
        Entity.onRender(self)
        if not self.passable:
            self.game.gfxEngine.renderRect(self.mask.rect, pygame.Color(10, 10, 200), 1)'''
            
class ExplosionSegment(Entity):
    def onInit(self):
        self.depth = -self.world.height
        self.mask = MaskBox(16, 16, self.x, self.y)
        self.world.collisionManager.add(self, 'boom')
        
        (_e, t) = self.world.collisionManager.placeMeetingType(self, self.x, self.y, ['solid', 'destructible'])
        if t == 'destructible':
            _e.destroy()
            self.destroy()
            return
        elif t == 'solid':
            self.destroy()
            return
        
        self.graphic = Spritemap(self.game.gfxEngine, '../gfx/bombland/boom.png', 16, 16)
        if self.segmentType == 'c':
            frames = [9, 17, 25]
        elif self.segmentType == 't':
            if self.segmentCounter == 0:
                frames = [13, 21, 29]
            else:
                frames = [12, 20, 28]
        elif self.segmentType == 'b':
            if self.segmentCounter == 0:
                frames = [14, 22, 30]
            else:
                frames = [12, 20, 28]
        elif self.segmentType == 'l':
            if self.segmentCounter == 0:
                frames = [8, 16, 24]
            else:
                frames = [11, 19, 27]
        elif self.segmentType == 'r':
            if self.segmentCounter == 0:
                frames = [10, 18, 26]
            else:
                frames = [11, 19, 27]
        self.graphic.addAnim('boom', Anim(frames, 0.5, False, self.destroy))
        self.graphic.playAnim('boom')
        
        # More?
        if self.segmentCounter > 0:
            if self.segmentType == 'c':
                self.newSegment('t')
                self.newSegment('b')
                self.newSegment('r')
                self.newSegment('l')
            else:
                self.newSegment(self.segmentType)
                
    def onCollision(self, group, other):
        if group in ['solid', 'destructible']:
            self.destroy()
    
    def newSegment(self, stype):
        if stype == 't':
            _s = ExplosionSegment(self.x, self.y-16, self.game, self.world)
        elif stype == 'b':
            _s = ExplosionSegment(self.x, self.y+16, self.game, self.world)
        elif stype == 'l':
            _s = ExplosionSegment(self.x-16, self.y, self.game, self.world)
        elif stype == 'r':
            _s = ExplosionSegment(self.x+16, self.y, self.game, self.world)
            
        _s.segmentType = stype
        _s.segmentCounter = self.segmentCounter - 1
        self.world.add(_s)
        
    def onDestroy(self):
        self.world.collisionManager.remove(self, 'boom')

class Bomber(Entity):
    def onInit(self):
        self.graphic = Spritemap(self.game.gfxEngine, '../gfx/bombland/player.png', 16, 24)
        self.graphic.offset = (0, -8)
        self.graphic.addAnim('stand', Anim([1], 1))
        self.graphic.addAnim('walk', Anim([2, 1, 3, 1], 0.3))
        
        self.graphic.playAnim('stand')
        
        self.mask = MaskBox(16, 16, self.x, self.y)
        self.world.collisionManager.add(self, 'player')
        
        self.sp = 2 
        
        self.moving = False
        
    def onStep(self):
        ox, oy = nx, ny = self.x, self.y
        
        solids = ['solid', 'destructible', 'bomb']
        
        self.moving = True
        if self.game.input.key(pygame.K_RIGHT):
            nx += self.sp
            self.graphic.xScale = 1.0
        elif self.game.input.key(pygame.K_LEFT):
            nx -= self.sp
            self.graphic.xScale = -1.0
        elif self.game.input.key(pygame.K_UP):
            ny -= self.sp
        elif self.game.input.key(pygame.K_DOWN):
            ny += self.sp
        else:
            self.moving = False
            
        self.depth = -(self.y // 16)
        
        if not self.game.input.key(pygame.K_LCTRL):
            if self.placeFree(nx, ny, solids):
                    self.x, self.y = nx, ny
            else:
                bomb = self.world.collisionManager.placeMeeting(self, 
                            nx, ny, ['bomb'])
                if bomb != None:
                    if not bomb.passable:
                        nx = self.x
                        ny = self.y
                
                solids = ['solid', 'destructible']
                if self.placeFree(nx, ny, solids):
                    self.x, self.y = nx, ny
                else:
                    if nx != self.x:
                        for _y in range(1, 12):
                            if _y > 2:
                                if self.placeFree(nx, ny-_y, solids):
                                    self.y -= self.sp/2
                                    break
                                elif self.placeFree(nx, ny+_y, solids):
                                    self.y += self.sp/2
                                    break
                            else:
                                if self.placeFree(nx, ny-_y, solids):
                                    self.x += math.copysign((self.sp / 2), (nx-self.x))
                                    self.y = ny-_y
                                    break
                                elif self.placeFree(nx, ny+_y, solids):
                                    self.x += math.copysign((self.sp / 2), (nx-self.x))
                                    self.y = ny+_y
                                    break
                    elif ny != self.y:
                        for _x in range(1, 12):
                            if _x > 2:
                                if self.placeFree(nx-_x, ny, solids):
                                    self.x -= self.sp/2
                                    break
                                elif self.placeFree(nx+_x, ny, solids):
                                    self.x += self.sp/2
                                    break
                            else:
                                if self.placeFree(nx-_x, ny, solids):
                                    self.y += math.copysign((self.sp / 2), (ny-self.y))
                                    self.x = nx-_x
                                    break
                                elif self.placeFree(nx+_x, ny, solids):
                                    self.y += math.copysign((self.sp / 2), (ny-self.y))
                                    self.x = nx+_x
                                    break
        else:
            self.x, self.y = nx, ny
        
        self.moving = self.x != ox or self.y != oy
        if self.moving:
            self.graphic.playAnim('walk')
        else:
            self.graphic.playAnim('stand')
            
        if self.game.input.keyPressed(pygame.K_z):
            if self.placeFree(self.x, self.y, ['bomb']):
                self.world.add(Bomb(((self.x+8) // 16)*16, ((self.y+8) // 16)*16, 
                                self.game, self.world))
        
    '''def onRender(self):
        Entity.onRender(self)
        self.game.gfxEngine.renderRect(self.mask.rect.copy(), pygame.Color(200, 10, 10), 1)'''
            
        
game = BombGame(320, 240, title="Bombland!", scaleH=3, scaleV=3)
while not game.finished:
    game.update()
    
game.end()
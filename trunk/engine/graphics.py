from engine.utils import config
from pygame import locals
import pygame
import math


class Graphic:
    def __init__(self, gfxEngine):
        self.gfxEngine = gfxEngine
        
        self.w = 0
        self.h = 0
        
        self.offset = (0, 0)
        
        self.color = pygame.Color(255, 255, 255)
        self.xScale = 1.0
        self.yScale = 1.0
        self.rotation = 0.0
        self.alpha = 1.0

    def update(self):
        pass

    def inView(self, camera, x, y):
        if camera == None:
            return True
        else:
            (_x, _y) = self.offset
            return camera.rectInView(pygame.Rect(x+_x, y+_y, self.w, self.h))

    def render(self, x, y, camera = None):
        (_x, _y) = self.offset
        if not camera == None:
            (x, y) = camera.transform(x + _x, y + _y)
        else:
            (x, y) = (x + _x, y + _y)
        if config.fastRender:
            self.fastRender(x, y)
        else:
            self.fullRender(x, y)
    
    def fastRender(self, x, y):
        pass
    
    def fullRender(self, x, y):
        pass

class Stamp(Graphic):
    def __init__(self, gfxEngine, path):
        Graphic.__init__(self, gfxEngine)
        self.image = pygame.image.load(path).convert()
        self.w = self.image.get_width()
        self.h = self.image.get_height()
    
    # Full effects render
    def fullRender(self, x, y):
        toRender = self.image.copy()
        # Color: not working (tints alpha too)
        if self.color != pygame.Color(255, 255, 255):
            toRender.fill(self.color, special_flags=locals.BLEND_RGB_MULT)
            toRender.set_colorkey(toRender.get_at((0, 0)))
        # Scale: working, warns about floats
        if self.xScale < 0 or self.yScale < 0:
            toRender = pygame.transform.flip(toRender, (self.xScale < 0), (self.yScale < 0))
        if self.xScale != 1.0 or self.yScale != 1.0:
            toRender = pygame.transform.scale(toRender, (self.image.get_width() * abs(self.xScale), self.image.get_height() * abs(self.yScale)))

        # Rotation: working but enlarges surface (solveable with an offset)
        if self.rotation != 0.0:
            toRender = pygame.transform.rotate(toRender, self.rotation)
    
        # Alpha: working
        if self.alpha != 1.0:
            toRender.set_alpha(self.alpha * 255)

        self.gfxEngine.renderSurface.blit(toRender, (x, y))
        
    # Fast render (just alpha and flip)
    def fastRender(self, x, y):
        # Alpha: working
        self.image.set_alpha(self.alpha * 255)
        # Flip
        if self.xScale < 0 or self.yScale < 0:
            self.gfxEngine.renderImage(
                pygame.transform.flip(self.image, 
                                      (self.xScale < 0), (self.yScale < 0)), 
                                        (x, y))
        else:
            self.gfxEngine.renderImage(self.image, (x, y))
            
class Spritemap(Graphic):
    def __init__(self, gfxEngine, path, spriteW, spriteH):
        Graphic.__init__(self, gfxEngine)
        
        self.image = pygame.image.load(path).convert()
        self.image.set_colorkey(self.image.get_at((0, 0)))
        
        self.spriteW = spriteW
        self.spriteH = spriteH
        
        self.w = spriteW
        self.h = spriteH
         
        self.cols = self.image.get_width() / spriteW
        self.rows = self.image.get_height() / spriteH
        
        self.imageIndex = 0
        self.anims = {}
        self.currentAnim = None

    def getBox(self):
        return ((self.imageIndex % self.cols)*self.spriteW,
             (self.imageIndex / self.cols)*self.spriteH,
             self.spriteW, self.spriteH)
    
    def addAnim(self, name, anim):
        self.anims[name] = anim
        
    def removeAnim(self, name):
        self.anims.pop(name)
        
    def playAnim(self, name, restart = False, speed = -1, loop = -1, callback = None):
        if self.currentAnim != name and self.currentAnim != None:
            self.anims[self.currentAnim].stop()
        if name in self.anims.keys():
            self.currentAnim = name
            self.anims[name].start(restart, speed, loop, callback)
            
    def pauseAnim(self):
        if self.currentAnim != None:
            self.anims[self.currentAnim].pause()
            
    def resumeAnim(self):
        if self.currentAnim != None:
            self.anims[self.currentAnim].resume()
            
    def setAnimSpeed(self, sp):
        if self.currentAnim != None:
            self.anims[self.currentAnim].speed = sp
    
    def update(self):
        if self.currentAnim != None:
            self.anims[self.currentAnim].update()
            self.imageIndex = self.anims[self.currentAnim].getImageIndex()
        
    def fastRender(self, x, y):
        sprite = pygame.surface.Surface((self.spriteW, self.spriteH))
        sprite.fill(pygame.Color(255, 0, 255))
        sprite.blit(self.image, (0, 0), self.getBox())
        sprite.set_colorkey(sprite.get_at((0, 0)))
        # Alpha: working
        sprite.set_alpha(self.alpha * 255)
        # Scale
        if self.xScale < 0 or self.yScale < 0:
            self.gfxEngine.renderImage(pygame.transform.flip(sprite, 
                            (self.xScale < 0), (self.yScale < 0)), (x, y))
        else:
            self.gfxEngine.renderImage(sprite, (x, y))

class Anim:
    def __init__(self, frames, speed, loop = False, callback = None):
        # Storage of defaults
        self._speed = speed
        self._loop = loop
        self._callback = callback

        # Actual values
        self.speed = speed
        self.loop = loop
        self.callback = callback
        
        self.paused = False
        self.frames = frames        
        self.frame = 0
        self.playing = False
        self.finished = False
        self.ticks = 0

    def update(self):
        if self.playing and not self.paused:
            # If a step of animation has been completed
            if self.ticks >= 1:
                # Reset ticker
                self.ticks = 0
                # Increase frame
                self.frame += 1
                # If finished
                if self.speed > 0 and self.frame >= len(self.frames):
                    # If it's a loop, restart
                    if self.loop:
                        self.ticks = 0
                        self.frame = 0
                        self.finished = False
                    # If it's not, we're finished
                    else:
                        self.ticks = 0
                        self.frame = len(self.frames)-1
                        self.finished = True
                        self.playing = False
                        self.paused = False
                    # Anyway, callback
                    if self.callback != None:
                        self.callback()
                    return
                elif self.speed < 0 and self.frame < -len(self.frames)+1:
                    if self.loop:
                        self.ticks = len(self.frames)-1
                        self.frame = len(self.frames)-1
                        self.finished = False
                        return
                    else:
                        self.ticks = 0
                        self.frame = 0
                        self.finished = True
                        self.playing = False
                        self.paused = False
                        return
            self.ticks += self.speed
                    
    def getImageIndex(self):
        return self.frames[self.frame]

    # Play the animation, with optional new parameters
    def start(self, restart = False, speed = -1, loop = -1, callback = None):
        # Only acts if not playing or forced restart
        if not self.playing or restart:
            if speed == -1:
                self.speed = self._speed
            else:
                self.speed = speed
                
            if loop == -1:
                self.loop = self._loop
            else:
                self.loop = loop
                
            if callback == None:
                self.callback = self._callback
            else:
                self.callback = callback
            
            self.frame = 0
            self.ticks = 0
            self.paused = False
            self.playing = True
            
    def pause(self):
        self.paused = True
        
    def resume(self):
        self.paused = False
        
    def stop(self):
        self.playing = False
        self.paused = False        
        self.frame = 0
        self.playing = False
        self.finished = False
        self.ticks = 0
        
    def isPlaying(self):
        return self.playing and not self.paused

class Tileset():
    def __init__(self, gfxEngine, path, tilew, tileh):
        self.gfxEngine = gfxEngine
        self.image = pygame.image.load(path).convert()
        # In tiles
        self.w = self.image.get_width()/tilew
        self.h = self.image.get_height()/tileh
        self.tilew = tilew
        self.tileh = tileh
    
    def getTileId(self, (x, y)):
        return y*self.w+x
    
    def getTile(self, tid):
        return pygame.Rect((tid%self.w)*self.tilew, (tid/self.w)*self.tileh, 
                           self.tilew, self.tileh)
    
class Tilemap(Graphic):
    def __init__(self, gfxEngine):
        self.gfxEngine = gfxEngine
        self.tileset = None
        self.tilemap = None
        # In tiles
        self.w = 0
        self.h = 0
        self.wTiles = 0
        self.hTiles = 0
        
    def setTileset(self, tset):
        self.tileset = tset
        # If all info's gathered, update!
        if self.tilemap != None:
            self.w = tset.tilew*self.wTiles
            self.h = tset.tileh*self.hTiles
        
    def setTilemap(self, tmap):
        self.tilemap = tmap
        self.wTiles = len(tmap)
        self.hTiles = len(tmap[0])
        # If all info's gathered, update!
        if self.tileset != None:
            self.w = self.tileset.tilew*self.wTiles
            self.h = self.tileset.tileh*self.hTiles
        
    def setTile(self, (x, y), tid):
        if x >= 0 and y >= 0 and x < self.w and y < self.h:
            self.tilemap[x][y] = tid
            
    def getTile(self, (x, y)):
        if x >= 0 and y >= 0 and x < self.w and y < self.h:
            return self.tilemap[x][y]
        else:
            return -1
        
    # Get coordinates of tile which contains pixel position (x, y)
    def getTileCoordsAt(self, (x, y)):
        return (x / self.tileset.tilew, y / self.tileset.tileh)
    
    # Get id of tile which contains pixel position (x, y)
    def getTileAt(self, (x, y)):
        (x, y) = self.getTileCoordsAt((x, y))
        return self.tilemap[x][y]
        
    def render(self, x, y, camera = None):
        # ix, iy = camera.getX()-x, camera.getY()-y
        itx, ity, ftx, fty = 0, 0, self.wTiles, self.hTiles
        # Adjust if camera present
        if not self.gfxEngine.activeCamera == None:
            camera = self.gfxEngine.activeCamera
            (itx, ity) = self.getTileCoordsAt((camera.getX()-x, 
                                               camera.getY()-y))
            '''(ftx, fty) = self.getTileCoordsAt(
                            (min(camera.getX()+camera.getW()-x, 
                                 (self.wTiles-1)*self.tileset.tilew), 
                             min(camera.getY()+camera.getH()-y,
                                 (self.hTiles-1)*self.tileset.tileh)))'''
            (ftx, fty) = (camera.getX()+camera.getW()-x, 
                            camera.getY()+camera.getH()-y)
            (itx, ity) = (max(0, itx), max(0, ity))
            (ftx, fty) = (min(ftx+1, (self.wTiles-1)),
                             min(fty+1, (self.hTiles-1)))
        # Render all tiles in range
        for i in range(itx, ftx):
            for j in range(ity, fty):
                self.gfxEngine.renderImage(self.tileset.image, 
                                   (x + i*self.tileset.tilew, y + j*self.tileset.tileh), 
                                       self.tileset.getTile(self.tilemap[i][j]))
                
# Tilemap for a small quantity of tiles (e.g. foreground tiles)
class SparseTilemap(Graphic):
    def __init__(self, gfxEngine, w, h):
        self.gfxEngine = gfxEngine
        self.tileset = None
        self.tilemap = {}
        # In pixels
        self.w = 0
        self.h = 0
        # In tiles
        self.wTiles = w
        self.hTiles = h 
        
    def setTileset(self, tset):
        self.tileset = tset
        self.w = tset.tilew*self.wTiles
        self.h = tset.tileh*self.hTiles
        
    def setTilemap(self, tmap):
        del self.tilemap
        self.tilemap = tmap
        
    def setTile(self, (x, y), tid):
        self.tilemap[(x, y)] = tid
        
    def getTile(self, (x, y)):
        if (x, y) in self.tilemap.keys():
            return self.tilemap[(x,y)]
        else:
            return -1
        
    def getTileCoordsAt(self, (x, y)):
        return (x / self.tileset.tilew, y / self.tileset.tileh)
    
    def getTileAt(self, (x, y)):
        (x, y) = self.getTileCoordsAt((x, y))
        return self.getTile((x, y))
    
    def render(self, x, y, camera = None):
        itx, ity, ftx, fty = 0, 0, self.wTiles, self.hTiles
        # Adjust if camera present
        if not self.gfxEngine.activeCamera == None:
            camera = self.gfxEngine.activeCamera
            (itx, ity) = self.getTileCoordsAt((camera.getX()-x, 
                                               camera.getY()-y))
            (ftx, fty) = (camera.getX()+camera.getW()-x, 
                            camera.getY()+camera.getH()-y)
            (itx, ity) = (max(0, itx), max(0, ity))
            (ftx, fty) = (min(ftx+1, (self.wTiles-1)),
                             min(fty+1, (self.hTiles-1)))
        # Render tiles in range
        for (tx, ty) in self.tilemap.keys():
            if tx in range(itx, ftx) and ty in range(ity, fty):
                self.gfxEngine.renderImage(self.tileset.image, 
                               (x + tx*self.tileset.tilew, y + ty*self.tileset.tileh), 
                               self.tileset.getTile(self.tilemap[(tx,ty)]))
from engine.utils import config
from pygame import locals
import pygame
import math


class Graphic:
    def __init__(self, gfxEngine):
        self.gfxEngine = gfxEngine
        
        self.w = 0
        self.h = 0
        
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
            return camera.rectInView(pygame.Rect(x, y, self.w, self.h))

    def render(self, x, y, camera = None):
        if not camera == None:
            (x, y) = camera.transform(x, y)
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
            self.gfxEngine.renderSurface.blit(pygame.transform.flip(self.image, (self.xScale < 0), (self.yScale < 0)), (x, y))
        else:
            self.gfxEngine.renderSurface.blit(self.image, (x, y))
            
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
             (self.imageIndex / self.cols)*self.spriteW,
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
            self.gfxEngine.renderSurface.blit(pygame.transform.flip(sprite, 
                                (self.xScale < 0), (self.yScale < 0)), (x, y))
        else:
            self.gfxEngine.renderSurface.blit(sprite, (x, y))

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
            self.ticks += self.speed
            (_dec, ent) = math.modf(self.ticks)
            if True:
                # Reset ticker
                # self.ticks = 0
                # Increase frame
                self.frame = ent.__int__()
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
                elif self.speed < 0 and self.frame < -len(self.frames)+1:
                    if self.loop:
                        self.ticks = len(self.frames)-1
                        self.frame = len(self.frames)-1
                        self.finished = False
                    else:
                        self.ticks = 0
                        self.frame = 0
                        self.finished = True
                        self.playing = False
                        self.paused = False
                    
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

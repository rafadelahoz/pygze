import pygame
from pygame import locals

from engine.utils import config

class Graphic:
    def __init__(self, gfxEngine):
        self.gfxEngine = gfxEngine
        self.color = pygame.Color(255, 255, 255)
        self.xScale = 1.0
        self.yScale = 1.0
        self.rotation = 0.0
        self.alpha = 1.0

    def update(self):
        pass

    def render(self, x, y):
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
    def __init__(self, gfxEngine, path, cols, rows):
        Graphic.__init__(self, gfxEngine)
        self.image = pygame.image.load(path).convert()
        self.cols = cols
        self.rows = rows
        self.spriteW = self.image.get_width() / self.cols
        self.spriteH = self.image.get_height() / self.rows
        self.imageIndex = 0
        self.anim = Anim("run", 5, [0, 1, 2, 3, 4, 5, 6, 7], True, self.thing)
        self.anim.start()
    
    def thing(self):
        print "IT IS ALIVE!"
    
    def update(self):
        self.anim.update()
        self.imageIndex = self.anim.getImageIndex()
        
    def fastRender(self, x, y):
        self.gfxEngine.renderSurface.blit(self.image, (x, y), 
            ((self.imageIndex % self.cols)*self.spriteW,
             (self.imageIndex / self.cols)*self.spriteW,
             self.spriteW, self.spriteH))

class Anim:
    def __init__(self, name, delay, frames, loop = False, callback = None):
        self.name = name

        # Storage of defaults
        self._delay = delay
        self._loop = loop
        self._callback = callback

        # Actual values
        self.delay = delay
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
            self.ticks += 1
            if self.ticks >= self.delay:
                # Reset ticker
                self.ticks = 0
                # Increase frame
                self.frame += 1
                # If finished
                if self.frame >= len(self.frames):
                    # If it's a loop, restart
                    if self.loop:
                        self.frame = 0
                        self.finished = False
                    # If it's not, we're finished
                    else:
                        self.frame = len(self.frames)-1
                        self.finished = True
                        self.playing = False
                        self.paused = False
                    # Anyway, callback
                    if self.callback != None:
                        self.callback()
                    
    def getImageIndex(self):
        return self.frames[self.frame]

    # Play the animation, with optional new parameters
    def start(self, restart = False, delay = -1, loop = -1, callback = None):
        # Only acts if not playing or forced restart
        if not self.playing or restart:
            if delay == -1:
                self.delay = self._delay
            else:
                self.delay = delay
                
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

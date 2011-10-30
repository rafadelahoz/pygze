import pygame

class GfxEngine:
    def __init__(self, width, height, hscale=1, vscale=1, winWidth= -1, winHeight= -1):
        self.renderWidth = width
        self.renderHeight = height
        self.renderScaleH = hscale
        self.renderScaleV = vscale
        if winWidth > 0 and winHeight > 0:
            self.winWidth = winWidth
            self.winHeight = winHeight
            if self.renderWidth * self.renderScaleH > winWidth:
                self.renderScaleH = 1
            if self.renderHeight * self.renderScaleV > winHeight:
                self.renderScaleV = 1
            self.renderPos = (self.winWidth / 2 - self.renderWidth * self.renderScaleH / 2,
                              self.winHeight / 2 - self.renderHeight * self.renderScaleV / 2)
        else:
            self.winWidth = width * hscale
            self.winHeight = height * vscale
            self.renderPos = (0, 0)
            
        self.renderSurface = pygame.Surface((self.renderWidth, self.renderHeight))
        self.screenSurface = pygame.display.set_mode((self.winWidth, self.winHeight))
        self.screenColor = pygame.Color(0, 0, 0)
        
    def clearRender(self, color=None):
        if color == None:
            color = self.screenColor
        self.renderSurface.fill(color)
            
    def clearScreen(self, color=None):
        if color == None:
            color = self.screenColor
        self.screenSurface.fill(color)
            
    def renderScreen(self):
        self.clearScreen()
        self.screenSurface.blit(
            pygame.transform.scale(self.renderSurface,
                                   (self.renderWidth * self.renderScaleH,
                                    self.renderHeight * self.renderScaleV)),
                                   (self.renderPos, self.renderPos))
        pygame.display.update()
        self.clearRender()

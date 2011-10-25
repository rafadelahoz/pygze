import pygame
from engine.gfxengine import GfxEngine

class Game:
    def __init__(self, renderW, renderH, fps = 30, title = "Game", scaleH=-1, scaleV=-1, windowW=-1, windowH=-1):
        self.gameState = None
        self.nextState = None
        self.clock = pygame.time.Clock()
        self.targetfps = fps
        
        self.title = title
        
        self.gfxEngine = GfxEngine(renderW, renderH, scaleH, scaleV, windowW, windowH)
        pygame.display.set_caption(title)

        self.finished = False
        
        # let user perform initialization
        self.onInit()
        
    def onInit(self):
        pass
        
    def update(self):
        # Input, ...
        for event in pygame.event.get():
            if (event.type == pygame.QUIT):
                self.finished = True
        
        if self.gameState != None:
            # Update GameState
            self.gameState.update()
    
            # Render GameState
            self.gfxEngine.clearRender()
            self.gameState.render(self.gfxEngine)
    
        # Change GameState
        if self.nextState != None:
            self.gameState.end()
            self.gameState = self.nextState
            self.gameState.init()
            self.nextState = None
        
        self.gfxEngine.renderScreen()
            
        self.clock.tick(self.targetfps)
            
    def end(self):
        if self.gameState != None:
            self.gameState.clear()
        if self.nextState != None:
            self.gameState.clear()
        pygame.quit()
            
    def changeGameState(self, gstate):
        if self.gameState == None:
            self.gameState = gstate
            self.gameState.init(self)
        else:
            if self.nextState != None:
                self.nextState.clear()
            self.nextState = gstate

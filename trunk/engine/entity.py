class Entity:
    def __init__(self, x, y, game, world):
        # Position
        self.x = x
        self.y = y
        
        # Game and world
        self.game = game
        self.world = world
        
        # Collision Variables
        self.collidable = True          # Causes collision events
        self.acceptCollisions = True    # Reacts to collision events
        
        # Collision mask
        self.mask = None
        
        # Graphic
        self.graphic = None
        
        # Timers
        self.timers = [-1 for i in range(1, 10)]
            
        # Let user perform initialization
        self.init()
    
    def update(self):
        # Performs common operations on every entity
        if self.graphic != None:
            self.graphic.update()
        if self.mask != None:
            self.mask.update()
        for i in range(0, 9):
            if self.timers[i] > 0:
                self.timers[i] -= 1
                if self.timers[i] == 0:
                    self.onTimer(i)
        self.onStep()
    
    def onInit(self):
        pass
    
    def onInitStep(self):
        pass

    def onStep(self):
        pass
    
    def onEndStep(self):
        pass
    
    def onRender(self):
        if self.graphic != None:
            self.graphic.render(self.x, self.y)
            
    def onCollision(self, group, other):
        pass
    
    def onTimer(self, timer):
        pass
    
    def onCustomEvent(self, event):
        pass
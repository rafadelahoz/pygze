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
        self.depth = 0
        self.graphic = None
        self.visible = True
        
        # Timers
        self.timers = [-1 for _i in range(1, 10)]
        
        # Ghost Status
        self.ghost = False
            
        # Let user perform initialization
        self.init()
    
    def update(self):
        if self.ghost:
            return
        # Performs common operations on every entity
        self.onStep()
        if self.graphic != None:
            self.graphic.update()
        if self.mask != None:
            self.mask.updatePosition(self.x, self.y)
            self.mask.update()
        for i in range(0, 9):
            if self.timers[i] > 0:
                self.timers[i] -= 1
                if self.timers[i] == 0:
                    self.onTimer(i)
        
    def collides(self, ent):
        if self.ghost:
            return False
        if ent == self:
            return False
        if not self.mask is None and not ent.mask is None:
            return self.mask.collides(ent.mask)
        
    def destroy(self):
        if self.ghost:
            return
        self.ghost = True
        
        self.world.remove(self)
        
    def _render(self, camera = None):
        if self.ghost:
            return
        if self.visible and self.inView(camera):
            self.onRender()
        
    def placeFree(self, x, y, groups = "any"):
        if self.ghost:
            return True
        return self.world.placeFree(self, x, y, groups)
    
    def moveToContact(self, x, y, groups="any"):
        if self.ghost:
            return True 
        return self.world.moveToContact(self, x, y, groups)
    
    def inView(self, camera):
        if self.ghost:
            return False
        if camera == None:
            return True
        else:
            return self.graphic.inView(camera, self.x, self.y)
    
    # Overridable
    # User initialization (on instantiation)
    def init(self):
        pass
    
    # Entity added to GameState
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

    def onDestroy(self):
        pass
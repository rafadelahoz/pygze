class Entity:
    def __init__(self, x, y, game, world):
        self.x = x
        self.y = y
        
        self.game = game
        self.world = world
        
        self.collidable = True
        self.acceptCollisions = True
        
        self.mask = None
        
    def onInit(self):
        pass

    def onStep(self):
        pass
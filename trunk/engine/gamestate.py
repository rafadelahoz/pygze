from collisionManager import CollisionManager

class GameState:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.collisionManager = CollisionManager()
        self.entities = []
        
    def init(self, game):
        self.game = game
    
    def update(self):
        print "GameState updating!"
        # Init Step
        for ent in self.entities:
            ent.onInitStep()
        
        # Update entities
        for ent in self.entities:
            ent.onStep()
        
        # Check collisions
        self.collisionManager.autoCollisions()
        
        # End Step
        for ent in self.entities:
            ent.onEndStep()
    
    def render(self, gfxEngine):
        for ent in self.entities:
            ent.onRender(gfxEngine)

    def end(self):
        pass
    
    def clear(self):
        pass

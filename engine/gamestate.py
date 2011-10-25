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
        # Init Step
        for ent in self.entities:
            ent.onInitStep()
        
        # Update entities
        for ent in self.entities:
            ent.update()
        
        # Check collisions
        self.collisionManager.autoCollisions()
        
        # End Step
        for ent in self.entities:
            ent.onEndStep()
    
    def render(self, gfxEngine):
        for ent in self.entities:
            ent.onRender()

    def end(self):
        pass
    
    def clear(self):
        pass

    def add(self, entity):
        self.entities.append(entity)
        
    def remove(self, entity):
        self.entities.remove(entity)
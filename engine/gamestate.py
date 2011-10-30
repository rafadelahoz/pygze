from collisionManager import CollisionManager

class GameState:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.collisionManager = CollisionManager()
        self.entities = []
        
    def _init(self, game):
        self.game = game
        self.init()
        
    def init(self):
        pass
    
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
        for ent in sorted(self.entities, key=lambda entity: entity.depth):
            ent.onRender()

    def end(self):
        pass
    
    def clear(self):
        pass

    def add(self, entity):
        self.entities.append(entity)
        
    def remove(self, entity):
        self.entities.remove(entity)

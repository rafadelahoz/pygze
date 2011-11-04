from collisionManager import CollisionManager

class GameState:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.collisionManager = CollisionManager()
        self.entities = []
        self.deathrow = []
        
    def _init(self, game):
        self.game = game
        self.init()
        
    def init(self):
        pass
    
    def update(self):
        # Init Step
        for ent in self.entities:
            ent.onInitStep()
        
        # Check collisions
        self.collisionManager.autoCollisions()
        
        # Update entities
        for ent in self.entities:
            ent.update()
        
        # End Step
        for ent in self.entities:
            ent.onEndStep()
            
        # Delete instances
        for ent in self.deathrow:
            self._remove(ent)
        self.deathrow = []
    
    def render(self, gfxEngine):
        self.renderBackground()
        for ent in sorted(self.entities, key=lambda entity: entity.depth):
            ent.onRender()
        self.renderForeground()

    def end(self):
        pass
    
    def clear(self):
        pass

    def add(self, entity):
        self.entities.append(entity)
        entity.onInit()
        
    def _remove(self, entity):
        self.entities.remove(entity)
        entity.onDestroy()
        del entity
        
    def remove(self, entity):
        if not entity in self.deathrow:
            self.deathrow.append(entity)

    def placeFree(self, entity, x, y):
        return self.collisionManager.placeFree(entity, x, y)
    
    def renderBackground(self):
        pass
    
    def renderForeground(self):
        pass

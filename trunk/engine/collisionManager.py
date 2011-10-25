class CollisionManager:
    def __init__(self):
        # Entities dictionary
        self.entities = {}
        self.groups = []
        self.listeners = {}
        
    # Insert entity into group 
    def add(self, entity, group):
        
        # Add group to CollisionManager if not present
        if group in self.groups:
            self.groups.append(group)
            self.listeners[group] = []
            
        # Create group list of entities
        if not (group in self.entities) or self.entities[group] == None:
            self.entities[group] = []
        
        # Add entity to group
        self.entities[group].append(entity)
    
    # Remove entity from group
    def remove(self, entity, group):
        if group in self.entities:
            self.entities[group].remove(entity)
            
    # Subscribe group to collisions with to
    def subscribe(self, group, to):
        if group in self.groups and to in self.groups:
            self.listeners[to].append(group)
    
    # Unsubscribe group from of
    def unsubscribe(self, group, of):
        if group in self.groups and of in self.groups:
            if group in self.listeners[of]:
                self.listeners[of].remove(group)

    # Check collisions between every group and its subscribers' entities 
    def autoCollisions(self):
        for group in self.groups:
            for subscriber in self.listeners[group]:
                for entA in self.entities[group]:
                    if entA.collidable and entA.acceptCollisions:
                        for entB in self.entities[subscriber]:
                            if entB.collidable:
                                # EntB will be noticed later
                                if entA.collides(entB):
                                        entA.onCollision(entB)
                                    # if entB.acceptCollisions:
                                    #    entB.onCollision(entA)
                      
    # Check collisions between groupA and groupB  
    def checkCollisions(self, groupA, groupB, forced = False):
        if groupA in self.groups and groupB in self.groups:
            if groupA in self.listeners[groupB] or forced:
                for entA in groupA:
                    if entA.collidable:
                        for entB in self.entities[groupB]:
                            if entB.collidable:
                                if entA.collides(entB):
                                    if entA.acceptCollisions:
                                        entA.onCollision(entB)
                                    if entB.acceptCollisions:
                                        entB.onCollision(entA)
                                    
    # Check collision between ent and groupB                                    
    def checkCollisionEntityGroup(self, ent, group):
        if ent.collidable:
            if group in self.groups:
                for entB in self.entities[group]:
                    if entB.collidable:
                        if ent.collides(entB):
                            if ent.acceptCollisions:
                                ent.onCollision(entB)
                            if entB.acceptCollisons:
                                entB.onCollison(ent)
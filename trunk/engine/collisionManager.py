class CollisionManager:
    def __init__(self):
        # Entities dictionary
        self.entities = {}
        self.groups = []
        self.listeners = {}
        
    # Set groups
    def setGroups(self, groups):
        for g in groups:
            self.groups.append(g)
            self.listeners[g] = []
            self.entities[g] = []
        
    # Insert entity into group 
    def add(self, entity, group):
        
        # Add group to CollisionManager if not present
        if not group in self.groups:
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
        if not group in self.groups:
            self.groups.append(group)
            self.listeners[group] = [] 
        if not to in self.groups:
            self.groups.append(to)
            self.listeners[to] = []
            
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
                    if entA.collidable:
                        for entB in self.entities[subscriber]:
                            if entB.collidable and entB.acceptCollisions:
                                # EntB will be noticed later
                                if entA.collides(entB):
                                    entB.onCollision(group, entA)
                                    # if entB.acceptCollisions:
                                    #    entB.onCollision(entA)
                      
    # Check collisions between groupA and groupB  
    def checkCollisions(self, groupA, groupB, forced=False):
        if groupA in self.groups and groupB in self.groups:
            if groupA in self.listeners[groupB] or forced:
                for entA in groupA:
                    if entA.collidable:
                        for entB in self.entities[groupB]:
                            if entB.collidable:
                                if entA.collides(entB):
                                    if entA.acceptCollisions:
                                        entA.onCollision(entB, groupB)
                                    if entB.acceptCollisions:
                                        entB.onCollision(entA, groupA)
                                    
    # Check collision between ent and groupB                                    
    def checkCollisionEntityGroup(self, ent, group):
        if ent.collidable:
            if group in self.groups:
                for entB in self.entities[group]:
                    if entB.collidable:
                        if ent.collides(entB):
                            if ent.acceptCollisions:
                                ent.onCollision(entB, group)
                            if entB.acceptCollisons:
                                entB.onCollison(ent, "any")

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
            if entity in self.entities[group]:
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
                 
    # Notice! If groups != "any" then it's a list               
    def placeFree(self, entity, x, y, groups = "any"):
        ox = entity.x
        oy = entity.y
        entity.mask.updatePosition(x, y)
        # If any group, check'em all
        if groups == "any":
            for g in self.groups:
                for ent in self.entities[g]:
                    if ent != entity and ent.collidable:
                        if ent.collides(entity):
                            entity.mask.updatePosition(ox, oy)
                            return False
        # If given group, check just those on the list
        else:
            for g in groups:
                for ent in self.entities[g]:
                    if ent != entity and ent.collidable:
                        if ent.collides(entity):
                            entity.mask.updatePosition(ox, oy)
                            return False
        # If not collided, place free
        entity.mask.updatePosition(ox, oy)
        return True
    
    def placeMeeting(self, entity, x, y, groups = "any"):
        ox, oy = entity.x, entity.y
        entity.mask.updatePosition(x, y)
        # If any group, check'em all
        if groups == "any":
            for g in self.groups:
                for ent in self.entities[g]:
                    if ent != entity and ent.collidable:
                        if ent.collides(entity):
                            entity.mask.updatePosition(ox, oy)
                            return ent
        # If given group, check just those on the list
        else:
            for g in groups:
                for ent in self.entities[g]:
                    if ent != entity and ent.collidable:
                        if ent.collides(entity):
                            entity.mask.updatePosition(ox, oy)
                            return ent
        return None
    
    def placeMeetingType(self, entity, x, y, groups = "any"):
        ox, oy = entity.x, entity.y
        entity.mask.updatePosition(x, y)
        # If any group, check'em all
        if groups == "any":
            for g in self.groups:
                for ent in self.entities[g]:
                    if ent != entity and ent.collidable:
                        if ent.collides(entity):
                            entity.mask.updatePosition(ox, oy)
                            return (ent, g)
        # If given group, check just those on the list
        else:
            for g in groups:
                for ent in self.entities[g]:
                    if ent != entity and ent.collidable:
                        if ent.collides(entity):
                            entity.mask.updatePosition(ox, oy)
                            return (ent, g)
        return (None, 'none')        
    
    def moveToContact(self, entity, x, y, groups = "any"):
        tx = entity.x
        ty = entity.y
        
        if (tx, ty) == (x, y):
            return
        
        deltaX, deltaY = 0, 0
        if tx < x:
            deltaX = +1
        else:
            deltaX = -1
        if ty < y:
            deltaY = +1
        else:
            deltaY = -1
            
        added = False
        # Adjust x
        while tx != x and self.placeFree(entity, tx, y, groups): 
            tx += deltaX
            added = True
        if added:
            tx -= deltaX
            
        # Adjust y
        added = False
        while ty != y and self.placeFree(entity, tx, ty, groups):
                ty += deltaY
                added = True
        if added:
            ty -= deltaY
                
        entity.x = tx
        entity.y = ty
        entity.mask.updatePosition(tx, ty)
        
    def instanceCount(self, group):
        if group == "all":
            return len(self.entities.values())
        else:
            return len(self.entities[group])
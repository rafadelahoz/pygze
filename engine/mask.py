class Mask:
    def __init__(self, x= -1, y= -1, w= -1, h= -1):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.maskType = "Mask"
        
    def updatePosition(self, x, y):
        self.x = x
        self.y = y
        
    def collides(self, other):
        return False
    
    def update(self):
        pass
    
class MaskBox(Mask):
    def __init__(self, w, h, x= -1, y= -1):
        Mask.__init__(self, x, y, w, h)
        self.maskType = "MaskBox"
    
    def collides(self, other):
        if (other.maskType == "MaskBox"):
            left, oleft = self.x, other.x
            right, oright = self.x + self.w, other.x + other.w
            top, otop = self.y, other.y
            bottom, obottom = self.y + self.h, other.y + other.h
            
            if bottom <= otop or top >= obottom or right <= oleft or left >= oright:
                return False
            return True
        else:
            return False

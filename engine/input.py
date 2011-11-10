import pygame
# import array

class Input:
    def __init__(self):
        # Keyboard
        self.keys = pygame.key.get_pressed()
        # self.oldKeys = array.array('B')
        self.oldKeys = [0 for _i in range(0, len(self.keys))]
        
        # Mouse
        # pygame.mouse.set_visible(False)
        self.mouseButtons = pygame.mouse.get_pressed()
        self.oldMouseButtons = [0 for _i in range(0, len(self.mouseButtons))] 
        
        # Joystick
        pygame.joystick.init()        
        self.numJoys = pygame.joystick.get_count()
        self.usedJoys = 0
        self.joys = []
    
    def update(self):
        # Keyboard
        for k in range(0, len(self.keys)):
            self.oldKeys[k] = self.keys[k]
        self.keys = pygame.key.get_pressed()
        
        # Joystick
        for joy in self.joys:
            joy.update()
            
        # Mouse
        for k in range(0, len(self.mouseButtons)):
            self.oldMouseButtons[k] = self.mouseButtons[k]
        self.mouseButtons = pygame.mouse.get_pressed()
                    
    # Keyboard
    def key(self, key):
        return self.keys[key]
    
    def keyPressed(self, key):
        return (self.keys[key] and not self.oldKeys[key])
    
    def keyReleased(self, key):
        return (not self.keys[key] and self.oldKeys[key])
    
    # Joystick
    def getNumJoysticks(self):
        return self.numJoys
    
    def getUsedJoysticks(self):
        return self.usedJoys
    
    def addJoystick(self, n = -1):
        if n == -1 and self.usedJoys < self.numJoys:
            j = Joystick(self.usedJoys, self)
            self.joys.append(j)
            self.usedJoys += 1
            return j
        else:
            if n != -1 and self.usedJoys > n:
                return self.joys[n]
            else: return None
        
    def removeJoystick(self, n):
        if n in range(0, len(self.usedJoys) - 1):
            self.usedJoys[n].deactivate()
            
    # Mouse
    # Get mouse position
    # If gfxEngine provided, will give it relative to scale and camera
    # else it will give it relative to display
    def getMousePosition(self, gfxEngine = None):
        if gfxEngine == None:
            return pygame.mouse.get_pos();
        else:
            (x, y) = pygame.mouse.get_pos();
            # This will actually get an old camera for a step when the
            # gamestate changes it
            if not gfxEngine.activeCamera == None:
                return (x/gfxEngine.renderScaleH+gfxEngine.activeCamera.getX(),
                        y/gfxEngine.renderScaleV+gfxEngine.activeCamera.getY()) 
            return (x/gfxEngine.renderScaleH, y/gfxEngine.renderScaleV)
    
    def mouseButton(self, button):
        return self.mouseButtons[button]
    
    def mousePressed(self, button):
        return self.mouseButtons[button] and not self.oldMouseButtons[button]
    
    def mouseReleased(self, button):
        return not self.mouseButtons[button] and self.oldMouseButtons[button]
    
class Joystick:
    def __init__(self, jid, jinput):
        self.input = jinput
        if jid >= 0 and jid < jinput.getNumJoysticks():
            self.id = jid
            self.joy = pygame.joystick.Joystick(jid)
            self.activate()
        else:
            self.id = -1
            self.joy = None
            print "Joystick {0} no valido!".format(jid)
            
    def activate(self):
        self.joy.init()
        self.numButtons = self.joy.get_numbuttons()
        self.buttons = [self.joy.get_button(i) for i in range(0, self.numButtons - 1)]
        self.oldButtons = [0 for _i in range(0, self.numButtons - 1)]

    def deactivate(self):
        self.joy.quit()
            
    def isValid(self):
        return (self.id != -1 and self.joy.get_init())
    
    def getNumAxes(self):
        return self.joy.get_numaxes()
    
    def getAxis(self, axis):
        return self.joy.get_axis(axis)
    
    def update(self):
        self.oldButtons = [self.buttons[i] for i in range(0, self.numButtons - 1)]
        self.buttons = [self.joy.get_button(i) for i in range(0, self.numButtons - 1)]
    
    def getNumButtons(self):
        return self.numButtons
        
    def button(self, button):
        if button in range(0, self.numButtons):
            return self.buttons[button]
        else:
            return 0
        
    def buttonPressed(self, button):
        if button in range(0, self.numButtons):
            return self.buttons[button] and not self.oldButtons[button]
        else:
            return 0
        
    def buttonReleased(self, button):
        if button in range(0, self.numButtons):
            return not self.buttons[button] and self.oldButtons[button]
        else:
            return 0

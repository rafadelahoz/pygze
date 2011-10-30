import pygame
import array

class Input:
    def __init__(self):
        self.keys = pygame.key.get_pressed()
        self.oldKeys = array.array('B')
        self.oldKeys = [0 for _i in range(1, len(self.keys))]
        
        pygame.joystick.init()
        
        self.numJoys = pygame.joystick.get_count()
        self.usedJoys = 0
        self.joys = []
    
    def update(self):
        for k in range(0, len(self.keys) - 1):
            self.oldKeys[k] = self.keys[k]
            
        self.keys = pygame.key.get_pressed()
        
        for joy in self.joys:
            joy.update()
            
    def key(self, key):
        return self.keys[key]
    
    def keyPressed(self, key):
        return (self.keys[key] and not self.oldKeys[key])
    
    def keyReleased(self, key):
        return (not self.keys[key] and self.oldKeys[key])
    
    def getNumJoysticks(self):
        return self.numJoys
    
    def getUsedJoysticks(self):
        return self.usedJoys
    
    def addJoystick(self, n= -1):
        if n == -1 and self.usedJoys < self.numJoys:
            j = Joystick(self.usedJoys, self)
            self.joys.append(j)
            self.usedJoys += 1
            return j
        else:
            return self.joys[n]
        
    def removeJoystick(self, n):
        if n in range(0, len(self.usedJoys) - 1):
            self.usedJoys[n].deactivate()
    
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

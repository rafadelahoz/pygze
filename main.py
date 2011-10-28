from game.agame import AGame
from game.agamestate import AGameState

game = AGame(320, 240, fps = 30, title = "AAAAAWESOME GAMERL!@2!", scaleH = 4, scaleV = 4, windowW = 320*4, windowH = 240*4)
game.changeGameState(AGameState(320, 240))

while not game.finished:
    game.update()

game.end()

print "End!"

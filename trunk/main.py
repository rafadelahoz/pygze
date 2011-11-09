from game.agame import AGame, AGameState

game = AGame(320, 240, title="A Game Test", scaleH=2, scaleV=2, fps=30)
game.changeGameState(AGameState(320, 240))

while not game.finished:
    game.update()

game.end()

print "End!"

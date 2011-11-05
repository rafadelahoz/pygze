from game.breakergame import BreakerGame, BreakerLevel

game = BreakerGame(320, 240, title="Breaker Game", scaleH=2, scaleV=2, fps=60)
game.changeGameState(BreakerLevel(320, 240))

while not game.finished:
    game.update()

game.end()

print "End!"

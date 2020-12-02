import sys
from Team import Team
from Player import Player
from Window import Window
import grid
from PyQt5.QtWidgets import QApplication

class Game:
    def __init__(self):
        self.window = Window()
        self.Team1 = Team([])
        self.Team2 = Team([])
        self.window.loadMap(grid.MATRIX)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    game = Game()
    game.Team1.players.append(Player(0, 100, "Thor"))
    game.window.highlightCells(grid.WATER, "lightblue")
    game.window.highlightCells(grid.ZONES, "violet")
    game.window.highlightCells(grid.ROOF, "lightyellow")


    #game.highlightCell([0], "blue")
    sys.exit(app.exec_())

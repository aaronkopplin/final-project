import sys
from Team import Team
from Player import Player
from Window import Window
import grid
from PyQt5.QtWidgets import QApplication

class Game:
    def __init__(self):
        self.window = Window()
        self.window.commandLine.returnPressed.connect(self.handleCommand)
        self.teams = [Team([]), Team([])]
        self.window.loadMap(grid.MATRIX)

    def updatePLayerLocations(self):
        for team in self.teams:
            for player in team.players:
                self.window.updatePlayer(player)

    def addPlayer(self, team: int, player: Player):
        self.teams[team].players.append(player)

        # update the color of the board
        self.window.updatePlayer(player)

    def handleCommand(self):
        args = self.window.commandLine.text().split(" ")
        command = args[0]

        if command == "move":
            print("Moving player from {0} to {1}.".format(args[1], args[2]))
        else:
            print("Unknown command.")

        self.window.commandLine.clear()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    game = Game()
    game.window.highlightCells(grid.WATER, "lightblue")
    game.window.highlightCells(grid.ZONES, "violet")
    game.window.highlightCells(grid.ROOF, "lightyellow")

    game.addPlayer(0, Player(0, 100, "Thor"))
    game.addPlayer(0, Player(1, 100, "Capitain America"))
    game.addPlayer(0, Player(2, 100, "Iron Man"))

    game.addPlayer(1, Player(221, 100, "Thor"))
    game.addPlayer(1, Player(222, 100, "Capitain America"))
    game.addPlayer(1, Player(223, 100, "Iron Man"))

    sys.exit(app.exec_())  # necessary

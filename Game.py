import sys
from Team import Team
from Player import Player
from Window import Window
import grid
from Dial import Dial
from PyQt5.QtWidgets import QApplication

class Game:
    def __init__(self):
        self.window = Window()
        self.window.commandLine.returnPressed.connect(self.handleCommand)
        self.teams = [Team([]), Team([])]
        self.window.loadMap(grid.MATRIX)

    def addPlayer(self, team: int, player: Player):
        self.teams[team].players.append(player)

        # update the color of the board
        self.window.updatePlayer(player, player.position)

    def handleCommand(self):
        args = self.window.commandLine.text().split(" ")
        if len(args) <= 0:
            return
        command = args[0]

        print(command)

        if command == "move":
            if len(args) < 3:
                print("Command arguments invalid.")
            else:
                startPos = int(args[1])
                endPos = int(args[2])

                for player in self.teams[0].players:
                    if player.position == startPos:
                        player.move(endPos)
                        self.window.updatePlayer(player, startPos)
        elif command == "take_turn":
            if len(args) < 3:
                print("Command arguments invalid.")
            else:
                die1 = int(args[1])
                die2 = int(args[2])
                print("Two dice rolls: {0} and {1}".format(die1, die2))
        else:
            print("Unknown command.")

        self.window.commandLine.clear()


if __name__ == "__main__":
    app = QApplication(sys.argv)

    # make the game, the game has the window and the grid
    game = Game()

    # color the board
    game.window.highlightCells(grid.WATER, "lightblue")
    game.window.highlightCells(grid.ZONES, "violet")
    game.window.highlightCells(grid.ROOF, "lightyellow")

    # make the dials
    thorsDial = Dial(150)
    thorsDial.speed = [10,10,10,10,10,10,9,9,9,0,0,0]
    thorsDial.attack = [11,11,11,10,10,10,9,9,9,0,0,0]
    thorsDial.defence = [18,17,17,17,17,17,17,17,16,0,0,0]
    thorsDial.explosion = [4,4,3,3,3,3,3,3,3,0,0,0]
    captainAmericasDial = Dial(50)
    captainAmericasDial.speed = [8, 7, 7, 6, 6, 5, 0, 0, 0, 0, 0, 0]
    captainAmericasDial.attack = [11, 10, 10, 9, 9, 9, 0, 0, 0, 0, 0, 0]
    captainAmericasDial.defence = [17, 17, 17, 16, 16, 17, 0, 0, 0, 0, 0, 0]
    captainAmericasDial.explosion = [3, 3, 3, 2, 2, 2, 0, 0, 0, 0, 0, 0]
    ironMansDial = Dial(100)
    ironMansDial.speed = [10,10,10,9,9,8,8,0,0,0,0,0]
    ironMansDial.attack = [10,10,10,9,9,9,9,0,0,0,0,0]
    ironMansDial.defence = [18,17,17,17,17,16,16,0,0,0,0,0]
    ironMansDial.explosion = [4,3,3,2,2,2,2,0,0,0,0,0]

    # add team 0
    game.addPlayer(0, Player(0, 100, "Thor", thorsDial))
    game.addPlayer(0, Player(1, 100, "Captain America", captainAmericasDial))
    game.addPlayer(0, Player(2, 100, "Iron Man", ironMansDial))

    # add team 1
    game.addPlayer(1, Player(221, 100, "Thor", thorsDial))
    game.addPlayer(1, Player(222, 100, "Captain America", captainAmericasDial))
    game.addPlayer(1, Player(223, 100, "Iron Man", ironMansDial))

    sys.exit(app.exec_())  # necessary

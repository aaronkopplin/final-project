import sys
from Team import Team
from Player import Player
from Window import Window
import grid
from Dial import Dial
from PyQt5.QtWidgets import QApplication
import the_map
import math
import copy
import DefaultCharacters

class Game:
    def __init__(self):
        self.window = Window()
        self.window.takeTurnButton.clicked.connect(self.takeTurn)
        self.window.moveButton.clicked.connect(self.moveCharacter)
        self.window.dealDamagebutton.clicked.connect(self.dealDamage)
        self.window.undoButton.clicked.connect(self.undo)
        self.teams = [Team([]), Team([])]
        self.window.loadMap(the_map.map)
        for button in self.window.playerButtons:
            button.clicked.connect(self.playerButtonListener)
        self.currentPath = []
        self.window.printStatsButton.clicked.connect(self.printStats)

    def printStats(self):
        args = self.window.commandLine.text().split(" ")
        if len(args) == 0:
            print("no value supplied")
            return
        if len(args) > 1:
            print("one character at a time please")
            return
        self.getPlayer(args[0]).dial.printDial(args[0])

    def playerButtonListener(self):
        def getTargetEnemy():
            return [enemy for enemy in self.teams[0].players if not enemy.isKOd][0]

        def playerOnCell(cell: int):
            for player in self.getPlayers():
                if player.position == cell:
                    return True
            return False

        def getCellsAdjacentTo(cell: int):
            # return [cell + 1, cell - 1, cell + 16, cell - 16, cell + 16 + 1, cell + 16 - 1, cell - 16 + 1,
            #         cell - 16 - 1]
            # x = math.floor(cell / 16)
            # y = cell % 16
            # return [self.window.maze[][]]
            return [i for i in range(len(the_map.map[cell])) if the_map.map[i] == 1]

        def cellNextToEnemy(cell: int):
            for enemy in self.teams[0].players:
                if cell in getCellsAdjacentTo(enemy.position):
                    return True
            return False

        # display the proposed path for the player that is selected
        for button in self.window.playerButtons:
            if button.isChecked():
                teammate = self.getPlayer(button.text())
                print(teammate.id)
                print(getTargetEnemy().id)
                # print("start pos " + str(teammate.position) + " target pos " + str(getTargetEnemy().position))

                path = self.window.maze.getPathTo(teammate.position, getTargetEnemy().position)
                # print(path)
                speed = teammate.currentSpeed()
                started_in_water = False
                if path.pop(0) in grid.WATER:
                    speed = speed/2
                    started_in_water = True

                good_path = []
                # hit water, player in the way, next to an enemy
                for cell in path:
                    if ((cell in grid.WATER and not started_in_water) or cellNextToEnemy(cell)) \
                            and not playerOnCell(cell):
                        good_path.append(cell)
                        break

                    if playerOnCell(cell) or path.index(cell) >= speed:
                        break
                    else:
                        good_path.append(cell)

                path = good_path
                self.resetGridColors()
                self.window.highlightCells(path, "red")
                self.currentPath = path


    def undo(self):
        print("undo")

    def getPlayer(self, id: str):
        for player in self.getPlayers():
            if player.id == id:
                return player
        return None

    def dealDamage(self):
        args = self.window.commandLine.text().split(" ")

        if len(args) == 2:
            self.getPlayer(args[0]).takeDamage(99999, int(args[1]))
            self.getPlayer(args[0]).printDial()
            return

        if (len(args) < 1 or len(args) > 3):
            return

        attacking_player = self.getPlayer(args[0])
        defending_player = self.getPlayer(args[1])


        if not attacking_player or not defending_player:
            print("player not found")
            return

        defending_player.takeDamage(int(args[2]), attacking_player.dial.currentDamage())
        if defending_player.isKOd:
            new_team0 = []
            new_team1 = []
            for player in self.getPlayers():
                if player.id != defending_player.id:
                    if player.team == 0:
                        new_team0.append(player)
                    elif player.team == 1:
                        new_team1.append(player)

            self.teams[0].players = new_team0
            self.teams[1].players = new_team1
            self.window.refreshBoard(self.getPlayers())
            print("player KO'd")
        else:
            defending_player.printDial()

    def addPlayer(self, team: int, player: Player):
        self.teams[team].players.append(player)

        # update the color of the board
        self.window.updatePlayer(player, player.position)

        # add a radio button
        if len(self.teams[1].players) > 0:
            self.window.playerButtons[len(self.teams[1].players) - 1].setText(self.teams[1].players[-1].id)

    def moveCharacter(self):
        args = self.window.commandLine.text().split(" ")

        for player in self.getPlayers():
            if player.id == args[0]:
                oldPos = player.position
                player.move(int(args[1]))
                self.window.updatePlayer(player, oldPos)

    def takeTurn(self):
        for button in self.window.playerButtons:
            if button.isChecked():
                teammate = self.getPlayer(button.text())
                if len(self.currentPath) > 0:
                    self.movePlayer(teammate, teammate.position, self.currentPath[-1])
                else:
                    print("the current path length is zero")
                self.window.radioGroup.setExclusive(False)
                button.setChecked(False)
                self.window.radioGroup.setExclusive(True)
                self.resetGridColors()

    def getPlayers(self):
        players = []
        for team in self.teams:
            for player in team.players:
                players.append(player)

        return players

    def movePlayer(self, player: Player, startLoc: int, endLoc: int):
        player.move(endLoc)
        self.window.refreshBoard(self.getPlayers())

    def resetGridColors(self):
        # color the board
        game.window.highlightCells([x for x in range(self.window.maze.width * self.window.maze.height)], "white")
        game.window.highlightCells(grid.WATER, "lightblue")
        game.window.highlightCells(grid.ZONES, "violet")
        game.window.highlightCells(grid.ROOF, "lightyellow")


if __name__ == "__main__":
    app = QApplication(sys.argv)

    # make the game, the game has the window and the grid
    game = Game()

    game.resetGridColors()

    # make the dials


    # add team 0
    game.addPlayer(0, Player(0, 100, "Thor", DefaultCharacters.thorsDial, 0))
    game.addPlayer(0, Player(1, 100, "Captain America", DefaultCharacters.captainAmericasDial, 0))
    game.addPlayer(0, Player(2, 100, "Iron Man", DefaultCharacters.ironMansDial, 0))

    # add team 1
    game.addPlayer(1, Player(221, 100, "Thor", copy.deepcopy(DefaultCharacters.thorsDial), 1))
    game.addPlayer(1, Player(222, 100, "Captain America", copy.deepcopy(DefaultCharacters.captainAmericasDial), 1))
    game.addPlayer(1, Player(223, 100, "Iron Man", copy.deepcopy(DefaultCharacters.ironMansDial), 1))

    sys.exit(app.exec_())  # necessary

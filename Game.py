import sys
from Team import Team
from Player import Player
from Window import Window
import grid
from Dial import Dial
from PyQt5.QtWidgets import QApplication
import map
import random

class Game:
    def __init__(self):
        self.window = Window()
        self.window.takeTurnButton.clicked.connect(self.takeTurn)
        self.window.moveButton.clicked.connect(self.moveCharacter)
        self.window.dealDamagebutton.clicked.connect(self.dealDamage)
        self.window.undoButton.clicked.connect(self.undo)
        self.teams = [Team([]), Team([])]
        self.window.loadMap(map.map)
        for button in self.window.playerButtons:
            button.clicked.connect(self.playerButtonListener)

    def playerButtonListener(self):
        def getTargetEnemy():
            return [enemy for enemy in self.teams[0].players if not enemy.isKOd][0]
        # display the proposed path for the player that is selected
        for button in self.window.playerButtons:
            if button.isChecked():
                teammate = self.getPlayer(button.text())
                print(teammate.id)
                print(getTargetEnemy().id)

                path = self.window.maze.getPathTo(teammate.position, getTargetEnemy().position)

                self.resetGridColors()
                self.window.highlightCells(path, "red")


    def undo(self):
        print("undo")

    def getPlayer(self, id: str):
        for player in self.getPlayers():
            if player.id == id:
                return player
        return None

    def dealDamage(self):
        args = self.window.commandLine.text().split(" ")
        if (len(args) < 1):
            return

        for player in self.getPlayers():
            if player.id == args[0]:
                player.takeDamage(int(args[1]), int(args[2]))
                break

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
        def getCellsAdjacentTo(cell: int):
            return [cell + 1, cell - 1, cell + 16, cell - 16, cell + 16 + 1, cell + 16 - 1, cell - 16 + 1,
                    cell - 16 - 1]

        def cellNextToEnemy(cell: int, enemies: list):
            for enemy in enemies:
                if cell in getCellsAdjacentTo(enemy.position):
                    return True
            return False

        def playerOnCell(cell: int):
            for player in self.getPlayers():
                if player.position == cell:
                    return True
            return False

        print("turn")
        die1 = random.randint(1, 6)
        die2 = random.randint(1, 6)

        # try to close the distance with the other players
        # seek out the first enemy that is not ko'd and have all teammates close on that enemy
        enemies = [enemy for enemy in self.teams[0].players if not enemy.isKOd]
        teammates = [member for member in self.teams[1].players if not member.isKOd]
        for teammate in teammates:
            if len(enemies) > 0:
                enemy = enemies[0]
                path = self.window.maze.getPathTo(teammate.position, enemy.position)

                self.resetGridColors()
                self.window.highlightCells(path, "red")

                # if you move next to an opposing player or into hindering terrain, you have to stop moving
                # if you begin a move in hindering terrain, you halve your speed value before moving
                # if you being a move next to an opposing player, you have to break away first. to do so, roll a
                # d6 if you roll 4-6 you can move, else your action is over.
                steps = 0
                while True:
                    if steps >= teammate.currentSpeed():
                        print("steps >= teammate speed ")
                        break
                    if len(path) == 1:
                        print("len path = 1")
                        break
                    if cellNextToEnemy(path[1], enemies):
                        print("cell next to enemy")
                        break
                    if playerOnCell(path[1]):
                        print("curr pos: " + str(teammate.position) + " next position: " + str(path[1]))
                        print("player on cell")
                        break

                    self.movePlayer(teammate, teammate.position, path.pop(0))
                    steps += 1

            else:
                print("GAME OVER, ALL ENEMIES KO'D")

    def getPlayers(self):
        players = []
        for team in self.teams:
            for player in team.players:
                players.append(player)

        return players

    def movePlayer(self, player: Player, startLoc: int, endLoc: int):
        player.move(endLoc)
        # self.window.updatePlayer(player, startLoc)
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
    thorsDial = Dial(150, 6)
    thorsDial.speed = [10,10,10,10,10,10,9,9,9,0,0,0]
    thorsDial.attack = [11,11,11,10,10,10,9,9,9,0,0,0]
    thorsDial.defence = [18,17,17,17,17,17,17,17,16,0,0,0]
    thorsDial.damage = [4, 4, 3, 3, 3, 3, 3, 3, 3, 0, 0, 0]
    captainAmericasDial = Dial(50, 5)
    captainAmericasDial.speed = [8, 7, 7, 6, 6, 5, 0, 0, 0, 0, 0, 0]
    captainAmericasDial.attack = [11, 10, 10, 9, 9, 9, 0, 0, 0, 0, 0, 0]
    captainAmericasDial.defence = [17, 17, 17, 16, 16, 17, 0, 0, 0, 0, 0, 0]
    captainAmericasDial.damage = [3, 3, 3, 2, 2, 2, 0, 0, 0, 0, 0, 0]
    ironMansDial = Dial(100, 7)
    ironMansDial.speed = [10,10,10,9,9,8,8,0,0,0,0,0]
    ironMansDial.attack = [10,10,10,9,9,9,9,0,0,0,0,0]
    ironMansDial.defence = [18,17,17,17,17,16,16,0,0,0,0,0]
    ironMansDial.damage = [4, 3, 3, 2, 2, 2, 2, 0, 0, 0, 0, 0]

    # add team 0
    game.addPlayer(0, Player(0, 100, "Thor", thorsDial, 0))
    game.addPlayer(0, Player(1, 100, "Captain America", captainAmericasDial, 0))
    game.addPlayer(0, Player(2, 100, "Iron Man", ironMansDial, 0))

    # add team 1
    game.addPlayer(1, Player(221, 100, "Thor", thorsDial, 1))
    game.addPlayer(1, Player(222, 100, "Captain America", captainAmericasDial, 1))
    game.addPlayer(1, Player(223, 100, "Iron Man", ironMansDial, 1))

    sys.exit(app.exec_())  # necessary

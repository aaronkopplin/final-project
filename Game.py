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

# keeps track of the state of the game
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
        self.window.resetCharacterButton.clicked.connect(self.resetCharacter)

    # deprecieated, used for creatign a new character from scratch in the event that
    # there was a bug or user mistake and we need a new character
    def resetCharacter(self):
        # characterID spawnLoc
        args = self.window.commandLine.text().split(" ")
        if len(args) == 2:
            char_name = ""
            dial = None
            if str(args[0][0]) == "T":
                char_name = "Thor"
                dial = copy.deepcopy(DefaultCharacters.thorsDial)
            if args[0][0] == "C":
                char_name = "Capitain America"
                dial = copy.deepcopy(DefaultCharacters.captainAmericasDial)
            if args[0][0] == "I":
                char_name = "Iron Man"
                dial = copy.deepcopy(DefaultCharacters.ironMansDial)
            game.createPlayer(int(args[0][1]), int(args[1]), char_name, dial)
            self.window.refreshBoard(self.getPlayers())

    # takes a character ID at the command line and will print the dial of that character
    def printStats(self):
        args = self.window.commandLine.text().split(" ")
        if len(args) == 0:
            print("no value supplied")
            return
        if len(args) > 1:
            print("one character at a time please")
            return
        self.getPlayer(args[0]).dial.printDial(args[0])

    # this method is attached to the player radio buttons. It will display a proposed path
    # for the character radio button that is selected. the user can then opt to take the move
    # by clicking the "Take Turn" button. If the proposed move is illegal, the user can wat until
    # the next turn to take a turn for that player.
    def playerButtonListener(self):
        # determines the enemey that is the current focus of the AI
        def getTargetEnemy():
            return [enemy for enemy in self.teams[0].players if not enemy.isKOd][0]

        # returns true if there is a player on that cell index. cell is a 0 - 255 value
        def playerOnCell(cell: int):
            for player in self.getPlayers():
                if player.position == cell:
                    return True
            return False

        # aks the adjacency matrix for the game what cells it is adjacent to.
        def getCellsAdjacentTo(cell: int):
            row = the_map.map[cell]
            cells = []
            for i in range(len(row)):
                if int(row[i]) == 1:
                    cells.append(i)
            return cells

        # returns true if the cell is next to any of the players on the enemy team.
        # cell is the 0 - 255 index of the cell
        def cellNextToEnemy(cell: int):
            for enemy in self.teams[0].players:
                if cell in getCellsAdjacentTo(enemy.position):
                    return True
            return False

        # display the proposed path for the player that is selected
        for button in self.window.playerButtons:
            # find the player that is selected from the radio buttons. Should be Tt, C1, or I1
            if button.isChecked():
                teammate = self.getPlayer(button.text())
                print(teammate.id)
                print(getTargetEnemy().id)

                # get the path to the target enemies position
                path = []
                try:
                    path = self.window.maze.getPathTo(teammate.position, getTargetEnemy().position)
                except:
                    print("path not found")
                    return

                # this is how many steps the player is allowed to take
                speed = teammate.currentSpeed()

                # if the player starts in water, then the player moves at 1/2 speed
                started_in_water = False
                if path.pop(0) in grid.WATER:
                    speed = speed/2
                    started_in_water = True

                # good path will keep the sanatized path
                good_path = []
                for cell in path:
                    # hit water, player in the way, next to an enemy
                    if ((cell in grid.WATER and not started_in_water) or cellNextToEnemy(cell)) \
                            and not playerOnCell(cell):
                        good_path.append(cell)
                        break

                    if playerOnCell(cell) or path.index(cell) >= speed:
                        break
                    else:
                        # if the next cell in the path is a legal move, append it to the good path
                        good_path.append(cell)

                # highlight the cells of the path, and then set the current path to the good path
                # current path will be executed when "Take Turn" is pressed in the GUI
                path = good_path
                self.resetGridColors()
                self.window.highlightCells(path, "red")
                self.currentPath = path

    # deprecieated
    def undo(self):
        print("undo")

    # return the player object matching the string ID
    def getPlayer(self, id: str):
        for player in self.getPlayers():
            if player.id == id:
                return player
        return None

    # this will determine how much damage a player should take, and apply the corresponding clicks, if any
    def dealDamage(self):
        # commands look like T0 T1 50, where T0 is the attacking player's id, T1 is the defending player's id
        # and 50 is the amount of damage points for the attack
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

    # add a player to the specified team, where team is 0 or 1 and player is a player object
    def addPlayer(self, team: int, player: Player, is_reset=False):
        self.teams[team].players.append(player)

        # update the color of the board
        self.window.updatePlayer(player, player.position)

        # add a radio button
        if not is_reset:
            if len(self.teams[1].players) > 0:
                self.window.playerButtons[len(self.teams[1].players) - 1].setText(self.teams[1].players[-1].id)

    # moves the character specified on the command line by ID to the cell index
    def moveCharacter(self):
        # T0 50 -> moves T0 from the cell it is on to cell 50
        args = self.window.commandLine.text().split(" ")

        for player in self.getPlayers():
            if player.id == args[0]:
                oldPos = player.position
                player.move(int(args[1]))
                self.window.updatePlayer(player, oldPos)

    # this will move the player along the path to the end of the path.
    def takeTurn(self):
        for button in self.window.playerButtons:
            if button.isChecked():
                teammate = self.getPlayer(button.text())
                if len(self.currentPath) > 0:
                    self.movePlayer(teammate, teammate.position, self.currentPath[-1])
                else:
                    print("the current path length is zero")

                # set the radio buttons to unselected
                self.window.radioGroup.setExclusive(False)
                button.setChecked(False)
                self.window.radioGroup.setExclusive(True)
                self.resetGridColors()

    # returns a list of all the players in the game
    def getPlayers(self):
        players = []
        for team in self.teams:
            for player in team.players:
                players.append(player)

        return players

    # sets the players location to endLoc (0-255 integer) and then updates the front end
    def movePlayer(self, player: Player, startLoc: int, endLoc: int):
        player.move(endLoc)
        self.window.refreshBoard(self.getPlayers())

    # resets the colors of the cells to their defaults. Wipes away any paths that were outlined in red.
    def resetGridColors(self):
        # color the board
        game.window.highlightCells([x for x in range(self.window.maze.width * self.window.maze.height)], "white")
        game.window.highlightCells(grid.WATER, "lightblue")
        game.window.highlightCells(grid.ZONES, "violet")
        game.window.highlightCells(grid.ROOF, "lightyellow")

    # depreceiated. Used to create a new player from scratch
    def createPlayer(self, team: int, spawnLoc: int, name: str, dial: Dial):
        game.addPlayer(team, Player(spawnLoc, 100, name, dial, team), True)


if __name__ == "__main__":
    app = QApplication(sys.argv)  # necessary

    # make the game, the game has the window and the grid
    game = Game()
    game.resetGridColors()

    # add team 0 ENEMIES
    game.addPlayer(0, Player(0, 100, "Thor", copy.deepcopy(DefaultCharacters.thorsDial), 0))
    game.addPlayer(0, Player(1, 100, "Captain America", copy.deepcopy(DefaultCharacters.captainAmericasDial), 0))
    game.addPlayer(0, Player(2, 100, "Iron Man", copy.deepcopy(DefaultCharacters.ironMansDial), 0))

    # add team 1 AI PLAYERS
    game.addPlayer(1, Player(221, 100, "Thor", copy.deepcopy(DefaultCharacters.thorsDial), 1))
    game.addPlayer(1, Player(222, 100, "Captain America", copy.deepcopy(DefaultCharacters.captainAmericasDial), 1))
    game.addPlayer(1, Player(223, 100, "Iron Man", copy.deepcopy(DefaultCharacters.ironMansDial), 1))

    sys.exit(app.exec_())  # necessary

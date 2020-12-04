from PyQt5 import  QtWidgets
from PyQt5.QtWidgets import QGridLayout, QWidget, QLineEdit
from PyQt5.QtWidgets import QSizePolicy
from PyQt5.QtCore import QRect, Qt
import Cell, Maze
import math
from Player import Player

# the GUI itself
class Window(QWidget):
    def __init__(self):
        super().__init__()
        self.mazeWidth = 16
        self.mazeHeight = 16
        self.frameWidth = 800
        self.frameHeight = 700
        self.setGeometry(QRect(0, 0, self.frameWidth, self.frameHeight))
        self.grid = QGridLayout()
        self.setLayout(self.grid)
        self.BuildMaze()
        self.BuildMenu()
        self.show()

    # the maze is the cell objects and the walls. walls are represented as cell borders
    def BuildMaze(self):
        self.maze = Maze.Maze(self.mazeWidth, self.mazeHeight)
        self.maze.setSizePolicy(QSizePolicy.Ignored, QSizePolicy.Ignored)
        self.grid.addWidget(self.maze)
        self.grid.setColumnStretch(0, 1)

    # the menue is the buttons and text field on the right side of the application
    def BuildMenu(self):
        verticalLayout = QtWidgets.QVBoxLayout()
        self.buttons = [QtWidgets.QCheckBox(x) for x in ["Left Wall", "Right Wall", "Top Wall", "Bottom Wall"]]
        for button in self.buttons:
            verticalLayout.addWidget(button)
            button.toggled.connect(self.buttonsClicked)

        # the text field in the menu where command data is entered
        self.commandLine = QLineEdit()
        verticalLayout.addWidget(self.commandLine)

        # one radio button for each AI player, T1, C1, I1
        self.radioGroup = QtWidgets.QButtonGroup()
        self.playerButtons = [QtWidgets.QRadioButton() for i in range(3)]
        for button in self.playerButtons:
            verticalLayout.addWidget(button)
            self.radioGroup.addButton(button)

        # this will save the current grid to a file
        self.printMAtrixButton = QtWidgets.QPushButton("Save Grid")
        verticalLayout.addWidget(self.printMAtrixButton)
        self.printMAtrixButton.clicked.connect(self.saveGrid)

        # used for moving the players
        self.takeTurnButton = QtWidgets.QPushButton("Take Turn")
        verticalLayout.addWidget(self.takeTurnButton)

        # this is for manually moving players
        self.moveButton = QtWidgets.QPushButton("Move Hero")
        verticalLayout.addWidget(self.moveButton)

        # this will assign damage to player. T0, T1 50 -> T0 attacks T1 for 50 damage
        self.dealDamagebutton = QtWidgets.QPushButton("Deal Damage")
        verticalLayout.addWidget(self.dealDamagebutton)

        # depreceited
        self.undoButton = QtWidgets.QPushButton("Undo")
        verticalLayout.addWidget(self.undoButton)

        # print the players stats to the command line
        self.printStatsButton = QtWidgets.QPushButton("Print Stats")
        verticalLayout.addWidget(self.printStatsButton)

        # depreceiated
        self.resetCharacterButton = QtWidgets.QPushButton("Reset Character")
        verticalLayout.addWidget(self.resetCharacterButton)
        self.resetCharacterButton.setEnabled(False)

        # shoves all the menu items to the top of the GUI
        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        verticalLayout.addItem(spacerItem)
        self.grid.addLayout(verticalLayout, 0, 1,1,1)

    # this will fill the walls of the saved map
    def loadMap(self, adjacency_matrix: list):
        self.maze.loadGridFromMatrix(adjacency_matrix)

    # this will save the current walls to the file
    def saveGrid(self):
        self.maze.printAdjacencyMatrix()

    # this is for adding and deleting walls from the map
    def buttonsClicked(self):
        self.maze.setWalls(self.buttons[0].isChecked(), self.buttons[1].isChecked(),
                           self.buttons[2].isChecked(), self.buttons[3].isChecked())

    # depreceiated
    def keyPressEvent(self, event):
        self.key = event.key()

    # highlights a list of indexes whatever color is passed in
    def highlightCells(self, path: list, color: str):
        # path is a list of the 0-255 indexes of cells to be highlighted
        for index in path:
            self.maze.highlightCell(index, color)

    # visually updates the location of the players on the cells. modifies the text of the cells according to the
    # locations of the players
    def updatePlayer(self, player: Player, previousPos: int):
        self.maze.updatePlayer(player, previousPos)

    # re paints the cells
    def refreshBoard(self, players: list):
        self.maze.refreshBoard(players)

import copy
import sys
from PyQt5 import  QtWidgets
from PyQt5.QtWidgets import QGridLayout, QWidget, QApplication, QVBoxLayout, QSpacerItem, QSplitter, QRadioButton, QLineEdit
from PyQt5.QtWidgets import QSizePolicy
import grid
from PyQt5.QtCore import QRect, Qt
import Cell, Maze
import math
import map
from Player import Player


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

    def BuildMaze(self):
        self.maze = Maze.Maze(self.mazeWidth, self.mazeHeight)
        self.maze.setSizePolicy(QSizePolicy.Ignored, QSizePolicy.Ignored)
        self.grid.addWidget(self.maze)
        self.grid.setColumnStretch(0, 1)

    def BuildMenu(self):
        verticalLayout = QtWidgets.QVBoxLayout()
        self.buttons = [QtWidgets.QCheckBox(x) for x in ["Left Wall", "Right Wall", "Top Wall", "Bottom Wall"]]
        for button in self.buttons:
            verticalLayout.addWidget(button)
            button.toggled.connect(self.buttonsClicked)

        self.commandLine = QLineEdit()
        verticalLayout.addWidget(self.commandLine)

        self.playerButtons = [QtWidgets.QRadioButton() for i in range(3)]
        for button in self.playerButtons:
            verticalLayout.addWidget(button)

        self.printMAtrixButton = QtWidgets.QPushButton("Save Grid")
        verticalLayout.addWidget(self.printMAtrixButton)
        self.printMAtrixButton.clicked.connect(self.saveGrid)

        self.takeTurnButton = QtWidgets.QPushButton("Take Turn")
        verticalLayout.addWidget(self.takeTurnButton)

        self.moveButton = QtWidgets.QPushButton("Move Hero")
        verticalLayout.addWidget(self.moveButton)

        self.dealDamagebutton = QtWidgets.QPushButton("Deal Damage")
        verticalLayout.addWidget(self.dealDamagebutton)

        self.undoButton = QtWidgets.QPushButton("Undo")
        verticalLayout.addWidget(self.undoButton)

        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        verticalLayout.addItem(spacerItem)
        self.grid.addLayout(verticalLayout, 0, 1,1,1)

    def loadMap(self, adjacency_matrix: list):
        self.maze.loadGridFromMatrix(adjacency_matrix)

    def saveGrid(self):
        self.maze.printAdjacencyMatrix()

    def buttonsClicked(self):
        self.maze.setWalls(self.buttons[0].isChecked(), self.buttons[1].isChecked(),
                           self.buttons[2].isChecked(), self.buttons[3].isChecked())

    def keyPressEvent(self, event):
        self.key = event.key()
        print("maze " + str(self.key))

    def aStarSearch(self, startIndex: int, goalIndex: int, matrix: list):
        #euclidian distance
        def h(x1, y1, x2, y2):
            return math.sqrt(math.pow((x2 - x1), 2) + math.pow((y2 - y1), 2))

        # start index is the 0-255 index of the starting cell
        openSet = [startIndex]
        closedSet = []
        path = {}
        while len(openSet) > 0:
            currentNodeIndex = 0
            for nodeIndex in openSet:
                if h(nodeIndex / 16, nodeIndex % 16, goalIndex / 16, goalIndex % 16) < h(currentNodeIndex / 16,
                                                                                         currentNodeIndex % 16,
                                                                                         goalIndex / 16,
                                                                                         goalIndex % 16):
                    currentNodeIndex = nodeIndex

            # path.append(currentNodeIndex)
            openSet.remove(currentNodeIndex)
            closedSet.append(currentNodeIndex)

            if (currentNodeIndex == goalIndex):
                total_path = [currentNodeIndex]
                while currentNodeIndex in path.keys():
                    currentNodeIndex = path[currentNodeIndex]
                    total_path = [currentNodeIndex] + total_path

                return total_path

            currentChildren = []
            for i in range(len(matrix[currentNodeIndex])):
                if (matrix[currentNodeIndex][i]):
                    currentChildren.append(i)

            for child in currentChildren:
                if child in closedSet:
                    continue

                if child in openSet:
                    if (h(child / 16, child % 16, startIndex / 16, startIndex % 16) > h(
                            openSet[openSet.index(child)] / 16, openSet[openSet.index(child)] % 16, startIndex / 16,
                            startIndex % 16)):
                        continue
                path[child] = currentNodeIndex
                openSet.append(child)

    def highlightCells(self, path: list, color: str):
        # path is a list of the 0-255 indexes of cells to be highlighted
        for index in path:
            self.maze.highlightCell(index, color)

    def updatePlayer(self, player: Player, previousPos: int):
        self.maze.updatePlayer(player, previousPos)

    def refreshBoard(self, players: list):
        self.maze.refreshBoard(players)

# if __name__ == "__main__":
#     app = QApplication(sys.argv)
#     maze = Window()
#     print("starting load")
#     maze.loadMap(grid.MATRIX)
#     print("finished")
#     path = maze.aStarSearch(15, 199, grid.MATRIX)
#     print(path)
#     maze.highlightCells(path)
#     sys.exit(app.exec_())

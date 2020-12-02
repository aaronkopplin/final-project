import copy

from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QGridLayout, QWidget, QApplication
import Cell
from PyQt5.QtWidgets import QSizePolicy
import grid
from Player import Player

from PyQt5.QtCore import QRect



class Maze(QtWidgets.QWidget):
    def __init__(self, width, height):
        super().__init__()
        self.width = width
        self.height = height
        self.grid = QGridLayout()
        self.setSizePolicy(QSizePolicy.Ignored, QSizePolicy.Ignored)
        self.grid.setHorizontalSpacing(0)
        self.grid.setVerticalSpacing(0)
        self.setLayout(self.grid)
        self.cells = []
        self.BuildGrid()
        self.show()

    def BuildGrid(self):
        for numeric in range(self.height):  # X axis
            row = []
            for alpha in range(self.width):  # Y axis
                c = Cell.Cell(numeric, alpha)
                if alpha == 0 or numeric == 0:
                    # c.setText(chr(97 + alpha) + ", " + str(numeric + 1))
                    c.setText("")
                self.grid.addWidget(c, numeric, alpha)
                row.append(c)
            self.cells.append(row)

    def setWalls(self, leftWall: bool, rightWall: bool, topWall: bool, bottomWall: bool):
        for row in self.cells:
            for cell in row:
                cell.setWalls(leftWall, rightWall, topWall, bottomWall)

    def loadGridFromMatrix(self, matrix: list):
        matrix = copy.deepcopy(matrix)
        for row in range(self.height):
            for column in range(self.width):
                adjacencyForCell = matrix.pop(0) # get the first row of the matrix
                cell = self.cells[row][column]

                for row2 in range(self.height):
                    for column2 in range(self.width):
                        val = adjacencyForCell.pop(0)
                        if val == 0:
                            if column2 == column - 1 and row2 == row:
                                cell.setWalls(True, cell.rightWall(), cell.topWall(), cell.bottomWall())
                                cell.updateWalls()
                            if column2 == column + 1 and row2 == row:
                                cell.setWalls(cell.leftWall(), True, cell.topWall(), cell.bottomWall())
                                cell.updateWalls()
                            if column2 == column and row2 == row - 1:
                                cell.setWalls(cell.leftWall(), cell.rightWall(), True, cell.bottomWall())
                                cell.updateWalls()
                            if column2 == column and row2 == row + 1:
                                cell.setWalls(cell.leftWall(), cell.rightWall(), cell.topWall(), True)
                                cell.updateWalls()

    def produceAdjacencyMartix(self):
        rows = []
        for row in range(self.height):
            for column in range(self.width):
                adjacencyRow = []
                cell = self.cells[row][column]

                for row2 in range(self.height):
                    for column2 in range(self.width):
                        val = 0
                        if column2 == column - 1 and row2 == row and not cell.leftWall():  # LEFT
                            val = 1
                        if column2 == column + 1 and row2 == row and not cell.rightWall():  # RIGHT
                            val = 1
                        if row2 == row + 1 and column2 == column and not cell.bottomWall():  # BOTTOM
                            val = 1
                        if row2 == row - 1 and column2 == column and not cell.topWall():  # TOP
                            val = 1

                        adjacencyRow.append(val)
                rows.append(adjacencyRow)
        return rows

    def highlightCell(self, index: int, color: str):
        # index is the 0 -255 index of the cell to be high lighted
        # convert the index to x, y
        self.cells[int(index / self.width)][index % self.height].changeBackgroundColor(color)

    def printAdjacencyMatrix(self):
        mat = self.produceAdjacencyMartix()
        print("---------------------------------------------------------------")
        for row in mat:
            print("[" + ", ".join(map(str, row)) + "]")
        print("---------------------------------------------------------------")

    def updatePlayer(self, player: Player):
        flat_list = [item for sublist in self.cells for item in sublist]
        flat_list[player.position].setText(player.name[0])



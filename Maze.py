import copy

from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QGridLayout, QWidget, QApplication
import Cell
from PyQt5.QtWidgets import QSizePolicy
import grid
from Player import Player
import os
import math
import map
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

    def getPathTo(self, start: int, end: int):
        path = self.aStarSearch(min(start, end), max(start, end), map.map)
        if start == max(start, end):
            path.reverse()
        return path

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
        # print("---------------------------------------------------------------")
        # for row in mat:
        #     print("[" + ", ".join(map(str, row)) + "]")
        # print("---------------------------------------------------------------")

        file_name = "map.py"
        if os.path.exists(file_name):
            os.remove(file_name)
        file = open(file_name, "x")
        file.write("map = [")
        for row in mat:
            #  comma separate all of the lists, this will add one unnecessary comma that we will remove later
            file.write("[" + ", ".join(map(str, row)) + "],\n")

        # remove the last comma from the end of of the file
        file.seek(0, os.SEEK_END)
        file.seek(file.tell() - 2, 0)
        file.truncate()

        # write the closing bracket
        file.write("]")

    def updatePlayer(self, player: Player, previousPos: int):
        flat_list = [item for sublist in self.cells for item in sublist]
        flat_list[previousPos].setText("")
        flat_list[player.position].setText(player.id)



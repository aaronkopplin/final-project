from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QSizePolicy
import re

# cells are the individual buttons that make up the game board. Cells can have text, color, and borders
class Cell(QtWidgets.QPushButton):
    def __init__(self, row, col):
        super().__init__()
        self.setStyleSheet(
            '''
            QPushButton {
                background-color : white;
                border : 4px solid;
                border-top-color : lightgray;
                border-left-color : lightgray;
                border-bottom-color : lightgray;
                border-right-color : lightgray;
            }
            ''')
        self.setSizePolicy(QSizePolicy.Ignored, QSizePolicy.Ignored)
        self.row = row
        self.col = col
        self.clicked.connect(self.updateWalls)
        self.editorLeftWall = False
        self.editorRightWall = False
        self.editorTopWall = False
        self.editorBottomWall = False

    # keeps track of the state of the cell
    def setWalls(self, leftWall: bool, rightWall: bool, topWall: bool, bottomWall: bool):
        self.editorLeftWall = leftWall
        self.editorRightWall = rightWall
        self.editorTopWall = topWall
        self.editorBottomWall = bottomWall

    # returns true if the cell has a left wall
    def leftWall(self):
        return re.search("border-left-color : black;", self.styleSheet())

    # returns true if the cell has a right wall
    def rightWall(self):
        return re.search("border-right-color : black;", self.styleSheet())

    # returns true if the cell has a top wall
    def topWall(self):
        return re.search("border-top-color : black;", self.styleSheet())

    # returns true if the cell has a bottom wall
    def bottomWall(self):
        return re.search("border-bottom-color : black;", self.styleSheet())

    # pass in a string of the wall left, right, top, bottom and it will set that border to black
    def setWall(self, wall: str):
        if str == "left":
            self.editorLeftWall = True
            self.changeWall(wall, self.editorLeftWall)
        if str == "right":
            self.editorRightWall = True
            self.changeWall(wall, self.editorRightWall)
        if str == "top":
            self.editorTopWall = True
            self.changeWall(wall, self.editorTopWall)
        if str == "bottom":
            self.editorBottomWall = True
            self.changeWall(wall, self.editorBottomWall)

    # make the visual appearance match the state of the cell
    def updateWalls(self):
        self.changeWall("left", self.editorLeftWall)
        self.changeWall("right", self.editorRightWall)
        self.changeWall("top", self.editorTopWall)
        self.changeWall("bottom", self.editorBottomWall)

    # takes a string, left, right, top, bottom and a bool True or False to set or clear that wall
    def changeWall(self, wall: str, activate: bool):
        self.setStyleSheet(re.sub("border-" + wall +"-color : [a-z]+;", "border-" + wall +"-color : " \
                                  + ("black" if activate else "lightgray") + ";", self.styleSheet()))

    # change the background color of the cell. can only use ROYGBIV colors
    def changeBackgroundColor(self, color: str):
        self.setStyleSheet(re.sub("background-color : [a-z]+;", "background-color : " + color + ";", self.styleSheet()))

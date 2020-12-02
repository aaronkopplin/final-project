import sys
from Window import Window
import grid
from PyQt5.QtWidgets import QApplication

if __name__ == "__main__":
    app = QApplication(sys.argv)
    maze = Window()
    maze.loadMap(grid.MATRIX)
    sys.exit(app.exec_())

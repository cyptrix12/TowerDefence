from PyQt5.QtWidgets import QGraphicsView

from config import GRID_WIDTH, GRID_HEIGHT, GRID_SIZE

class GameView(QGraphicsView):
    def __init__(self, scene):
        super().__init__(scene)
        self.setFixedSize(GRID_WIDTH * GRID_SIZE + 2, GRID_HEIGHT * GRID_SIZE + 2)
        self.setWindowTitle("Tower Defense")
from PyQt5.QtWidgets import QGraphicsView

from GameConfig import Config

class GameView(QGraphicsView):
    def __init__(self, scene):
        super().__init__(scene)
        self.config = Config()
        self.GRID_SIZE = self.config.get_grid_size()
        self.GRID_WIDTH = self.config.get_grid_width()
        self.GRID_HEIGHT = self.config.get_grid_height()
        self.setFixedSize(self.GRID_WIDTH * self.GRID_SIZE + 2, self.GRID_HEIGHT * self.GRID_SIZE + 2)
        self.setWindowTitle("Tower Defense")
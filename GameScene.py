from PyQt5.QtWidgets import QGraphicsScene, QGraphicsTextItem, QGraphicsPixmapItem
from PyQt5.QtGui import QPixmap, QFont, QColor
from PyQt5.QtCore import QPointF
from Enemies import AnimatedEnemy
from Towers import AnimatedTower

import assets_rc

GRID_SIZE = 100
GRID_WIDTH = 10
GRID_HEIGHT = 10

class GameScene(QGraphicsScene):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setSceneRect(0, 0, GRID_WIDTH * GRID_SIZE, GRID_HEIGHT * GRID_SIZE)
        self.lives = 3
        self.path = [
            (0, 5), (1, 5), (2, 5), (3, 5), (3, 4), (3, 3), (4, 3), (5, 3),
            (5, 4), (5, 5), (6, 5), (7, 5), (8, 5), (9, 5)
        ]
        self.init_grid()
        self.lives_text = QGraphicsTextItem(f"Lives: {self.lives}")
        self.lives_text.setDefaultTextColor(QColor(255, 0, 0))
        self.lives_text.setFont(QFont("Arial", 16))
        self.lives_text.setPos(GRID_WIDTH * GRID_SIZE - 150, 10)
        self.addItem(self.lives_text)

    def init_grid(self):
        for x in range(GRID_WIDTH):
            for y in range(GRID_HEIGHT):
                pos = QPointF(x * GRID_SIZE, y * GRID_SIZE)
                bg_pixmap = QPixmap(":/assets/Environment/Grass/spr_grass_01.png").scaled(GRID_SIZE, GRID_SIZE)
                bg_item = QGraphicsPixmapItem(bg_pixmap)
                bg_item.setPos(pos)
                self.addItem(bg_item)

                if (x, y) in self.path:
                    overlay_pixmap = QPixmap(":/assets/Environment/Tile Set/spr_tile_set_ground.png").scaled(GRID_SIZE, GRID_SIZE)
                    overlay_item = QGraphicsPixmapItem(overlay_pixmap)
                    overlay_item.setPos(pos)
                    self.addItem(overlay_item)

    def decrease_lives(self):
        self.lives -= 1
        self.lives_text.setPlainText(f"Lives: {self.lives}")
        if self.lives <= 0:
            print("Game Over!")

    def addEnemy(self):
        enemy = AnimatedEnemy(self.path[0][0], self.path[0][1], self.path, self)
        self.addItem(enemy)
    
    def addTower(self, x=0, y=0):
        tower = AnimatedTower(x, y)
        self.addItem(tower)
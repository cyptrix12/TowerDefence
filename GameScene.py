from PyQt5.QtWidgets import QGraphicsScene, QGraphicsTextItem, QGraphicsPixmapItem, QGraphicsRectItem, QGraphicsItem, QPushButton
from PyQt5.QtGui import QPixmap, QFont, QColor
from PyQt5.QtCore import QPointF, Qt, QEvent
from Enemies import AnimatedEnemy
from Towers import AnimatedTower
from Projectile import Projectile

import assets_rc
from config import GRID_WIDTH, GRID_HEIGHT, GRID_SIZE

class GameScene(QGraphicsScene):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.controller = None
        self.setSceneRect(0, 0, GRID_WIDTH * GRID_SIZE, GRID_HEIGHT * GRID_SIZE)
        self.path = [
            (0, 5), (1, 5), (2, 5), (3, 5), (3, 4), (3, 3), (4, 3), (5, 3),
            (5, 4), (5, 5), (6, 5), (7, 5), (8, 5), (9, 5)
        ]
        self.path_tiles = []
        self.init_path_tiles()
        self.init_grid()
        self.lives_text = QGraphicsTextItem(f"Lives: {0}")
        self.lives_text.setDefaultTextColor(QColor(255, 0, 0))
        self.lives_text.setFont(QFont("Arial", 16))
        self.lives_text.setPos(GRID_WIDTH * GRID_SIZE - 150, 10)
        self.addItem(self.lives_text)

        self.health_bars = {}
        self.enemy_class = AnimatedEnemy
        self.installEventFilter(self)

        self.tower_positions = set()

        self.tower_pallete = None
        self.add_tower_palette()

        self.start_button = QPushButton("START LEVEL")
        self.start_button.setGeometry(GRID_WIDTH * GRID_SIZE - 150, GRID_HEIGHT * GRID_SIZE - 50, 120, 40)
        self.start_button.clicked.connect(self.start_level_placeholder)  # Tymczasowy placeholder
        self.start_button.setParent(parent)
        self.start_button.show()

    def set_controller(self, controller):
        """Przypisuje kontroler do sceny."""
        self.controller = controller
        self.start_button.clicked.disconnect()  # Usuń placeholder
        self.start_button.clicked.connect(self.controller.start_level)  # Połącz z metodą kontrolera

    def start_level_placeholder(self):
        """Tymczasowy placeholder dla przycisku przed przypisaniem kontrolera."""
        print("Controller not set yet!")

    def init_path_tiles(self):
        overlay_pixmap = QPixmap(":/assets/Environment/Tile Set/spr_tile_set_ground.png").scaled(GRID_SIZE * 3, GRID_SIZE * 3)
        self.path_tiles = [
            overlay_pixmap.copy(x * GRID_SIZE, y * GRID_SIZE, GRID_SIZE, GRID_SIZE)
            for y in range(3) for x in range(3)
        ]

    def init_grid(self):
        for x in range(GRID_WIDTH):
            for y in range(GRID_HEIGHT):
                pos = QPointF(x * GRID_SIZE, y * GRID_SIZE)
                bg_pixmap = QPixmap(":/assets/Environment/Grass/spr_grass_01.png").scaled(GRID_SIZE, GRID_SIZE)
                bg_item = QGraphicsPixmapItem(bg_pixmap)
                bg_item.setPos(pos)
                self.addItem(bg_item)

                if (x, y) in self.path:
                    if (x+1,y) in self.path and (x,y+1) in self.path:
                        overlay_item = QGraphicsPixmapItem(self.path_tiles[0])
                    elif (x+1,y) in self.path and (x,y-1) in self.path:
                        overlay_item = QGraphicsPixmapItem(self.path_tiles[6])
                    elif (x-1,y) in self.path and (x,y+1) in self.path:
                        overlay_item = QGraphicsPixmapItem(self.path_tiles[2])
                    elif (x-1,y) in self.path and (x,y-1) in self.path:
                        overlay_item = QGraphicsPixmapItem(self.path_tiles[8])
                    elif (x+1,y) in self.path or (x-1,y) in self.path:
                        overlay_item = QGraphicsPixmapItem(self.path_tiles[1])
                    else:
                        overlay_item = QGraphicsPixmapItem(self.path_tiles[3])
                    overlay_item.setPos(pos)
                    self.addItem(overlay_item)

    def add_health_bar(self, enemy):
        health_bar = QGraphicsRectItem(0, -10, GRID_SIZE, 5) 
        health_bar.setBrush(QColor(0, 255, 0))  
        health_bar.setParentItem(enemy) 
        self.health_bars[enemy] = health_bar 

    def update_health_bar(self, enemy):
        if enemy in self.health_bars:
            health_bar = self.health_bars[enemy]
            health_percentage = max(enemy.hp / enemy.max_hp, 0)  
            health_bar.setRect(0, -10, GRID_SIZE * health_percentage, 5)  
            if health_percentage > 0.5:
                health_bar.setBrush(QColor(0, 255, 0))  # Green
            elif health_percentage > 0.2:
                health_bar.setBrush(QColor(255, 165, 0))  # Orange
            else:
                health_bar.setBrush(QColor(255, 0, 0))  # Red

    def remove_health_bar(self, enemy):
        if enemy in self.health_bars:
            health_bar = self.health_bars.pop(enemy)
            self.removeItem(health_bar)

    def eventFilter(self, source, event):
        if self.controller:
            handled = self.controller.EventFilter(source, event)
            if handled is not None:
                return handled

        return super().eventFilter(source, event)

    def add_tower_palette(self):
        background = QGraphicsRectItem(0, 0, GRID_SIZE, GRID_SIZE)
        background.setBrush(QColor(255, 255, 255))  # White

        self.addItem(background)

        tower_palette = AnimatedTower(0, 0, self)
        tower_palette.setFlag(QGraphicsItem.ItemIsMovable, True)
        tower_palette.setFlag(QGraphicsItem.ItemIsSelectable, True)

        self.tower_pallete = tower_palette
        self.addItem(tower_palette)

    def mouseReleaseEvent(self, event):
        if self.tower_pallete.isUnderMouse():
            pos = event.scenePos()
            x = int(pos.x() // GRID_SIZE)
            y = int(pos.y() // GRID_SIZE)
            if (x, y) not in self.path:
                self.controller.addTower(x, y)
            self.removeItem(self.tower_pallete)
            self.add_tower_palette()
            return
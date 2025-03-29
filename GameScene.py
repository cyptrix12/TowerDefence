from PyQt5.QtWidgets import QGraphicsScene, QGraphicsTextItem, QGraphicsPixmapItem, QGraphicsRectItem, QGraphicsItem, QPushButton
from PyQt5.QtGui import QPixmap, QFont, QColor
from PyQt5.QtCore import QPointF, Qt, QEvent
from Enemies import AnimatedEnemy
from Towers import AnimatedTower
from Projectile import Projectile
from GameConfig import Config

import assets_rc



import random

class GameScene(QGraphicsScene):
    def __init__(self, config, parent=None):
        self.config = Config()
        self.GRID_SIZE = self.config.get_grid_size()
        self.GRID_WIDTH = self.config.get_grid_width()
        self.GRID_HEIGHT = self.config.get_grid_height()


        super().__init__(parent)
        self.controller = None
        self.setSceneRect(0, 0, self.GRID_WIDTH * self.GRID_SIZE, self.GRID_HEIGHT * self.GRID_SIZE)
        self.path = self.generate_random_path()  # Generowanie losowej ścieżki
        self.path_tiles = []
        self.init_path_tiles()
        self.init_grid()
        self.lives_text = QGraphicsTextItem(f"Lives: {0}")
        self.lives_text.setDefaultTextColor(QColor(255, 0, 0))
        self.lives_text.setFont(QFont("Arial", 16))
        self.lives_text.setPos(self.GRID_WIDTH * self.GRID_SIZE - 150, 10)
        self.addItem(self.lives_text)

        self.health_bars = {}
        self.enemy_class = AnimatedEnemy
        self.installEventFilter(self)

        self.tower_positions = set()

        self.tower_pallete = None
        self.add_tower_palette()

        self.start_button = QPushButton("START LEVEL")
        self.start_button.setGeometry(self.GRID_WIDTH * self.GRID_SIZE - 150, self.GRID_HEIGHT * self.GRID_SIZE - 50, 120, 40)
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

    def generate_random_path(self):
        path = []
        visited = set()

        x, y = 0, self.GRID_HEIGHT // 2 
        path.append((x, y))
        visited.add((x, y))

        while x < self.GRID_WIDTH - 1:
            directions = []
            if x + 1 < self.GRID_WIDTH and (x + 1, y) not in visited:
                directions.append((x + 1, y))  # Prawo
            if y + 1 < self.GRID_HEIGHT and (x, y + 1) not in visited:
                directions.append((x, y + 1))  # Dół
            if y - 1 >= 0 and (x, y - 1) not in visited:
                directions.append((x, y - 1))  # Góra

            if not directions:
                # Jeśli brak dostępnych kierunków, zakończ generowanie
                break

            # Wybierz losowy kierunek
            x, y = random.choice(directions)
            path.append((x, y))
            visited.add((x, y))

        # Upewnij się, że ścieżka kończy się na x=self.GRID_WIDTH-1
        if path[-1][0] < self.GRID_WIDTH - 1:
            for i in range(path[-1][0] + 1, self.GRID_WIDTH):
                path.append((i, y))
                visited.add((i, y))

        return path

    def init_path_tiles(self):
        overlay_pixmap = QPixmap(":/assets/Environment/Tile Set/spr_tile_set_ground.png").scaled(self.GRID_SIZE * 3, self.GRID_SIZE * 3)
        self.path_tiles = [
            overlay_pixmap.copy(x * self.GRID_SIZE, y * self.GRID_SIZE, self.GRID_SIZE, self.GRID_SIZE)
            for y in range(3) for x in range(3)
        ]

    def init_grid(self):
        for x in range(self.GRID_WIDTH):
            for y in range(self.GRID_HEIGHT):
                pos = QPointF(x * self.GRID_SIZE, y * self.GRID_SIZE)
                bg_pixmap = QPixmap(":/assets/Environment/Grass/spr_grass_01.png").scaled(self.GRID_SIZE, self.GRID_SIZE)
                bg_item = QGraphicsPixmapItem(bg_pixmap)
                bg_item.setPos(pos)
                self.addItem(bg_item)

        previous_pos = None
        for path_pos in self.path:
            x, y = path_pos
            if previous_pos is None:
                previous_pos = (path_pos[0]-1, path_pos[1])
            next_path_pos = self.path[self.path.index(path_pos) + 1] if self.path.index(path_pos) + 1 < len(self.path) else (path_pos[0]+1, path_pos[1])
            pos = QPointF(x * self.GRID_SIZE, y * self.GRID_SIZE)

            if previous_pos == (x, y + 1) and next_path_pos == (x + 1, y):
                overlay_item = QGraphicsPixmapItem(self.path_tiles[0])
            elif previous_pos == (x - 1, y) and next_path_pos == (x, y + 1):
                overlay_item = QGraphicsPixmapItem(self.path_tiles[2])
            elif previous_pos == (x, y - 1) and next_path_pos == (x + 1, y):
                overlay_item = QGraphicsPixmapItem(self.path_tiles[6])
            elif previous_pos == (x - 1, y) and next_path_pos == (x, y - 1):
                overlay_item = QGraphicsPixmapItem(self.path_tiles[8])
            elif previous_pos == (x, y + 1) or previous_pos == (x, y - 1):
                overlay_item = QGraphicsPixmapItem(self.path_tiles[3])
            else:
                overlay_item = QGraphicsPixmapItem(self.path_tiles[1])

            overlay_item.setPos(pos)
            self.addItem(overlay_item)
            previous_pos = path_pos

    def add_health_bar(self, enemy):
        health_bar = QGraphicsRectItem(0, -10, self.GRID_SIZE, 5) 
        health_bar.setBrush(QColor(0, 255, 0))  
        health_bar.setParentItem(enemy) 
        self.health_bars[enemy] = health_bar 

    def update_health_bar(self, enemy):
        if enemy in self.health_bars:
            health_bar = self.health_bars[enemy]
            health_percentage = max(enemy.hp / enemy.max_hp, 0)  
            health_bar.setRect(0, -10, self.GRID_SIZE * health_percentage, 5)  
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
        background = QGraphicsRectItem(0, 0, self.GRID_SIZE, self.GRID_SIZE)
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
            x = int(pos.x() // self.GRID_SIZE)
            y = int(pos.y() // self.GRID_SIZE)
            if (x, y) not in self.path:
                self.controller.addTower(x, y)
            self.removeItem(self.tower_pallete)
            self.add_tower_palette()
            return
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
        self.path = self.generate_random_path()
        self.path_tiles = []
        self.init_path_tiles()

        self.overlay_assets = [
            (":/assets/Environment/Decoration/spr_mushroom_01.png", "mushroom"),
            (":/assets/Environment/Decoration/spr_rock_01.png", "rock"),
            (":/assets/Environment/Decoration/spr_tree_01_normal.png", "tree")
        ]

        self.overlay_items = []  
        self.init_grid()

        # Lives text
        self.lives_text = QGraphicsTextItem(f"Lives: {0}")
        self.lives_text.setDefaultTextColor(QColor(255, 0, 0))
        self.lives_text.setFont(QFont("Arial", 16))
        self.lives_text.setPos(self.GRID_WIDTH * self.GRID_SIZE - 150, 10)
        self.addItem(self.lives_text)

        # Level text
        self.level_text = QGraphicsTextItem(f"Level: {0}")
        self.level_text.setDefaultTextColor(QColor(0, 0, 255))  # Blue
        self.level_text.setFont(QFont("Arial", 16))
        self.level_text.setPos(self.GRID_WIDTH * self.GRID_SIZE - 150, 40)
        self.addItem(self.level_text)

        # Money text
        self.money_text = QGraphicsTextItem(f"Money: {100}")
        self.money_text.setDefaultTextColor(QColor(255, 215, 0))  # Gold
        self.money_text.setFont(QFont("Arial", 16))
        self.money_text.setPos(self.GRID_WIDTH * self.GRID_SIZE - 150, 70) 
        self.addItem(self.money_text)

        self.health_bars = {}
        self.enemy_class = AnimatedEnemy
        self.installEventFilter(self)

        self.tower_positions = set()

        self.tower_pallete = None
        self.add_tower_palette()

        self.start_button = QPushButton("START LEVEL")
        self.start_button.setGeometry(self.GRID_WIDTH * self.GRID_SIZE - 150, self.GRID_HEIGHT * self.GRID_SIZE - 50, 120, 40)
        self.start_button.clicked.connect(self.start_level_placeholder)
        self.start_button.setParent(parent)
        self.start_button.show()

    def set_controller(self, controller):
        self.controller = controller
        self.start_button.clicked.disconnect()
        self.start_button.clicked.connect(self.controller.start_level)

    def start_level_placeholder(self):
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
                directions.append((x + 1, y))
            if y + 1 < self.GRID_HEIGHT and (x, y + 1) not in visited:
                directions.append((x, y + 1))
            if y - 1 >= 0 and (x, y - 1) not in visited:
                directions.append((x, y - 1))

            if not directions:
                break

            x, y = random.choice(directions)
            path.append((x, y))
            visited.add((x, y))

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

                if (x, y) not in self.path and random.random() < 0.1:  # 10% chance
                    overlay_source, overlay_type = random.choice(self.overlay_assets)
                    overlay_pixmap = QPixmap(overlay_source).scaled(self.GRID_SIZE // 3, self.GRID_SIZE // 3)
                    overlay_item = QGraphicsPixmapItem(overlay_pixmap)
                    overlay_item.setPos(pos)
                    self.addItem(overlay_item)

                    self.overlay_items.append({"item": overlay_item, "type": overlay_type, "pos": (x, y)})

        previous_pos = None
        for path_pos in self.path:
            x, y = path_pos
            if previous_pos is None:
                previous_pos = (path_pos[0]-1, path_pos[1])
            next_path_pos = self.path[self.path.index(path_pos) + 1] if self.path.index(path_pos) + 1 < len(self.path) else (path_pos[0]+1, path_pos[1])
            pos = QPointF(x * self.GRID_SIZE, y * self.GRID_SIZE)

            if previous_pos == (x, y + 1) and next_path_pos == (x + 1, y): #Γ
                overlay_item = QGraphicsPixmapItem(self.path_tiles[0])
            elif previous_pos == (x - 1, y) and next_path_pos == (x, y + 1): #ㄱ
                overlay_item = QGraphicsPixmapItem(self.path_tiles[2])
            elif previous_pos == (x, y - 1) and next_path_pos == (x + 1, y): #L
                overlay_item = QGraphicsPixmapItem(self.path_tiles[6])
            elif previous_pos == (x - 1, y) and next_path_pos == (x, y - 1): #」
                overlay_item = QGraphicsPixmapItem(self.path_tiles[8])
            elif previous_pos == (x, y + 1) or previous_pos == (x, y - 1): #|
                overlay_item = QGraphicsPixmapItem(self.path_tiles[3])
            else:
                overlay_item = QGraphicsPixmapItem(self.path_tiles[1]) # -

            overlay_item.setPos(pos)
            self.addItem(overlay_item)
            previous_pos = path_pos

    def get_adjacent_overlays(self, x, y):
        adjacent_positions = [
            (x - 1, y), (x + 1, y),  # Left, Right
            (x, y - 1), (x, y + 1)   # Up, Down
        ]
        adjacent_overlays = []

        for overlay in self.overlay_items:
            if overlay["pos"] in adjacent_positions:
                adjacent_overlays.append({"type": overlay["type"], "item": overlay["item"]})

        return adjacent_overlays

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
        return
        background = QGraphicsRectItem(0, 2 * self.GRID_SIZE, self.GRID_SIZE, self.GRID_SIZE)
        background.setBrush(QColor(255, 255, 255))  # White

        self.addItem(background)

        tower_palette = AnimatedTower(0, 2, self)
        tower_palette.setFlag(QGraphicsItem.ItemIsMovable, True)
        tower_palette.setFlag(QGraphicsItem.ItemIsSelectable, True)

        self.tower_pallete = tower_palette
        self.addItem(tower_palette)

    def mouseReleaseEvent(self, event):
        # if self.tower_pallete.isUnderMouse():
        #     pos = event.scenePos()
        #     x = int(pos.x() // self.GRID_SIZE)
        #     y = int(pos.y() // self.GRID_SIZE)
        #     if (x, y) not in self.path:
        #         self.controller.addTower(x, y)
        #     self.removeItem(self.tower_pallete)
        #     self.add_tower_palette()
        return

    def update_level(self, level):
        """Aktualizuje tekst poziomu."""
        self.level_text.setPlainText(f"Level: {level}")

    def update_money(self, money):
        """Uaktualnia tekst wyświetlający money."""
        self.money_text.setPlainText(f"Money: {money}")
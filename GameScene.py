from PyQt5.QtWidgets import QGraphicsScene, QGraphicsTextItem, QGraphicsPixmapItem, QGraphicsRectItem
from PyQt5.QtGui import QPixmap, QFont, QColor
from PyQt5.QtCore import QPointF, Qt, QEvent
from Enemies import AnimatedEnemy
from Towers import AnimatedTower
from Projectile import Projectile

import assets_rc
from config import GRID_WIDTH, GRID_HEIGHT, GRID_SIZE

class GameScene(QGraphicsScene):
    def __init__(self, controller, parent=None):
        super().__init__(parent)
        self.controller = controller  # Referencja do GameController
        self.setSceneRect(0, 0, GRID_WIDTH * GRID_SIZE, GRID_HEIGHT * GRID_SIZE)
        self.path = [
            (0, 5), (1, 5), (2, 5), (3, 5), (3, 4), (3, 3), (4, 3), (5, 3),
            (5, 4), (5, 5), (6, 5), (7, 5), (8, 5), (9, 5)
        ]
        self.path_tiles = []  # Lista przechowująca 9 kwadratów ścieżki
        self.init_path_tiles()
        self.init_grid()
        self.lives_text = QGraphicsTextItem(f"Lives: {0}")
        self.lives_text.setDefaultTextColor(QColor(255, 0, 0))
        self.lives_text.setFont(QFont("Arial", 16))
        self.lives_text.setPos(GRID_WIDTH * GRID_SIZE - 150, 10)
        self.addItem(self.lives_text)

        self.health_bars = {}  # Słownik przechowujący paski życia
        self.enemy_class = AnimatedEnemy  # Referencja do klasy wroga
        self.installEventFilter(self)  # Zainstaluj filtr zdarzeń na GameScene

    def init_path_tiles(self):
        """Inicjalizuje listę 9 kwadratów wyciętych z obrazka ścieżki."""
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
        """Dodaje pasek życia nad wrogiem."""
        health_bar = QGraphicsRectItem(0, -10, GRID_SIZE, 5)  # Pasek nad wrogiem
        health_bar.setBrush(QColor(0, 255, 0))  # Zielony kolor
        health_bar.setParentItem(enemy)  # Pasek życia jest dzieckiem wroga
        self.health_bars[enemy] = health_bar  # Przechowuj pasek w słowniku

    def update_health_bar(self, enemy):
        """Aktualizuje pasek życia wroga."""
        if enemy in self.health_bars:
            health_bar = self.health_bars[enemy]
            health_percentage = max(enemy.hp / enemy.max_hp, 0)  # Procent życia
            health_bar.setRect(0, -10, GRID_SIZE * health_percentage, 5)  # Zmiana szerokości
            if health_percentage > 0.5:
                health_bar.setBrush(QColor(0, 255, 0))  # Zielony
            elif health_percentage > 0.2:
                health_bar.setBrush(QColor(255, 165, 0))  # Pomarańczowy
            else:
                health_bar.setBrush(QColor(255, 0, 0))  # Czerwony

    def remove_health_bar(self, enemy):
        """Usuwa pasek życia wroga."""
        if enemy in self.health_bars:
            health_bar = self.health_bars.pop(enemy)
            self.removeItem(health_bar)

    def eventFilter(self, source, event):
        """Przekazuje zdarzenia do kontrolera."""
        if event.type() == QEvent.GraphicsSceneMousePress:
            if event.button() == Qt.LeftButton:
                return self.controller.handle_mouse_event(event)  # Przekaż zdarzenie do kontrolera
        return super().eventFilter(source, event)
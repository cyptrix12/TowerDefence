import sys
from PyQt5.QtWidgets import (
    QApplication, QGraphicsScene, QGraphicsView, QGraphicsRectItem, QGraphicsItem, QGraphicsPixmapItem , QGraphicsTextItem
    
)
from PyQt5.QtGui import QBrush, QColor, QPen, QPainter, QPixmap, QFont
from PyQt5.QtCore import Qt, QRectF, QTimer

import assets_rc

# Stałe dla planszy
GRID_SIZE = 100
GRID_WIDTH = 10
GRID_HEIGHT = 10

# Kolory
GRAY = QColor(200, 200, 200)
DARK_GRAY = QColor(150, 150, 150)
BROWN = QColor(139, 69, 19)
RED = QColor(255, 0, 0)
BLUE = QColor(0, 0, 255)
GREEN = QColor(0, 255, 0)

from PyQt5.QtWidgets import QGraphicsItem
from PyQt5.QtGui import QPixmap, QPainter
from PyQt5.QtCore import QTimer, QRectF, Qt

class GameUnit(QGraphicsItem):
    def __init__(self, x, y, sprite_path, frame_count=1, frame_duration=0, parent=None):
        super().__init__(parent)
        self.grid_x = x
        self.grid_y = y
        self.setPos(x * GRID_SIZE, y * GRID_SIZE)

        self.sprite_sheet = QPixmap(sprite_path)
        self.frame_count = frame_count
        self.frame_index = 0
        self.frame_width = self.sprite_sheet.width() // frame_count
        self.frame_height = self.sprite_sheet.height()

        self.timer = QTimer()
        if frame_duration > 0:
            self.timer.timeout.connect(self.next_frame)
            self.timer.start(frame_duration)

    def boundingRect(self):
        return QRectF(0, 0, GRID_SIZE, GRID_SIZE)

    def paint(self, painter, option, widget):
        frame = self.get_current_frame()
        painter.drawPixmap(0, 0, frame)

    def get_current_frame(self):
        x = self.frame_index * self.frame_width
        frame = self.sprite_sheet.copy(x, 0, self.frame_width, self.frame_height)
        return frame.scaled(
            GRID_SIZE, GRID_SIZE,
            Qt.KeepAspectRatio,
            Qt.FastTransformation
        )

    def next_frame(self):
        self.frame_index = (self.frame_index + 1) % self.frame_count
        self.update()


class AnimatedEnemy(GameUnit):
    def __init__(self, x, y, path, scene):
        super().__init__(
            x, y,
            sprite_path=":/assets/Enemies/spr_bat.png",
            frame_count=4,
            frame_duration=200
        )
        self.path = path
        self.path_index = 0
        self.speed = 2  
        self.scene = scene 

        self.target_x = x * GRID_SIZE
        self.target_y = y * GRID_SIZE

        self.move_timer = QTimer()
        self.move_timer.timeout.connect(self.follow_path)
        self.move_timer.start(16)  # (60 FPS)

    def follow_path(self):
        if self.path_index < len(self.path):
            target_grid_pos = self.path[self.path_index]
            self.target_x = target_grid_pos[0] * GRID_SIZE
            self.target_y = target_grid_pos[1] * GRID_SIZE

            dx = self.target_x - self.x()
            dy = self.target_y - self.y()

            distance = (dx**2 + dy**2)**0.5

            if distance < self.speed:
                self.setPos(self.target_x, self.target_y)
                self.path_index += 1
            else:
                step_x = self.speed * dx / distance
                step_y = self.speed * dy / distance
                self.setPos(self.x() + step_x, self.y() + step_y)
        else:
            self.scene.decrease_lives()
            self.scene.removeItem(self) 
            self.move_timer.stop()


class AnimatedTower(GameUnit):
    def __init__(self, x, y):
        super().__init__(
            x, y,
            sprite_path=":/assets/Towers/Castle/spr_castle_blue.png",
            frame_count=4,
            frame_duration=200
        )


class GameScene(QGraphicsScene):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setSceneRect(0, 0, GRID_WIDTH * GRID_SIZE, GRID_HEIGHT * GRID_SIZE)
        self.selected_tiles = set()
        self.lives = 3
        self.path = [
            (0, 5), (1, 5), (2, 5), (3, 5), (3, 4), (3, 3), (4, 3), (5, 3),
            (5, 4), (5, 5), (6, 5), (7, 5), (8, 5), (9, 5)
        ]
        self.init_grid(self.path)

        self.lives_text = QGraphicsTextItem(f"Lives: {self.lives}")
        self.lives_text.setDefaultTextColor(Qt.red)
        self.lives_text.setFont(QFont("Arial", 16))
        self.lives_text.setPos(GRID_WIDTH * GRID_SIZE - 150, 10)
        self.addItem(self.lives_text)
        

        self.addItem(AnimatedEnemy(self.path[0][0], self.path[0][1], self.path, self))
        self.addItem(AnimatedTower(3, 3))
        
    def decrease_lives(self):
        self.lives -= 1
        self.lives_text.setPlainText(f"Lives: {self.lives}")
        if self.lives <= 0:
            print("Game Over!")

    def init_grid(self, path=None):
        for x in range(GRID_WIDTH):
            for y in range(GRID_HEIGHT):
                tile = QGraphicsRectItem(x * GRID_SIZE, y * GRID_SIZE, GRID_SIZE, GRID_SIZE)
                if (x,y) in path:
                    tile.setBrush(QBrush(GREEN))
                else:
                    tile.setBrush(QBrush(GRAY))
                tile.setPen(DARK_GRAY)
                tile.setData(0, (x, y))
                tile.setAcceptHoverEvents(True)
                tile.setFlag(QGraphicsRectItem.ItemIsSelectable)
                self.addItem(tile)

    def mousePressEvent(self, event):
        item = self.itemAt(event.scenePos(), self.views()[0].transform())
        if item and isinstance(item, QGraphicsRectItem):
            pos = item.data(0)
            if pos in self.selected_tiles:
                item.setBrush(QBrush(GREEN if pos in self.path else GRAY))
                self.selected_tiles.remove(pos)
            else:
                item.setBrush(QBrush(RED))
                self.selected_tiles.add(pos)
        super().mousePressEvent(event)


class GameView(QGraphicsView):
    def __init__(self, scene):
        super().__init__(scene)
        self.setFixedSize(GRID_WIDTH * GRID_SIZE + 2, GRID_HEIGHT * GRID_SIZE + 2)
        self.setWindowTitle("Tower Defense")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    scene = GameScene()
    view = GameView(scene)
    view.show()
    sys.exit(app.exec_())

from PyQt5.QtWidgets import QGraphicsItem
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import QTimer, QRectF, Qt

from GameConfig import Config

class GameUnit(QGraphicsItem):
    def __init__(self, x, y, sprite_path, frame_count=1, frame_duration=0, parent=None):
        super().__init__(parent)

        self.config = Config()
        self.GRID_SIZE = self.config.get_grid_size()

        self.grid_x = x
        self.grid_y = y
        self.setPos(x * self.GRID_SIZE, y * self.GRID_SIZE) 

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
        return QRectF(0, 0, self.GRID_SIZE, self.GRID_SIZE) 

    def paint(self, painter, option, widget):
        frame = self.get_current_frame()
        painter.drawPixmap(0, 0, frame)

    def get_current_frame(self):
        x = self.frame_index * self.frame_width
        frame = self.sprite_sheet.copy(x, 0, self.frame_width, self.frame_height)
        return frame.scaled(self.GRID_SIZE, self.GRID_SIZE, Qt.KeepAspectRatio, Qt.FastTransformation) 

    def next_frame(self):
        self.frame_index = (self.frame_index + 1) % self.frame_count
        self.update()
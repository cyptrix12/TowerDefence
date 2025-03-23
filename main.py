import sys
from PyQt5.QtWidgets import QApplication, QGraphicsScene, QGraphicsView, QGraphicsRectItem
from PyQt5.QtGui import QBrush, QColor
from PyQt5.QtCore import Qt

# Stałe dla planszy
GRID_SIZE = 50  # Rozmiar pojedynczej kratki
GRID_WIDTH = 10  # Szerokość planszy (liczba kratek)
GRID_HEIGHT = 10  # Wysokość planszy (liczba kratek)

# Kolory
GRAY = QColor(200, 200, 200)
DARK_GRAY = QColor(150, 150, 150)
BROWN = QColor(139, 69, 19)  # Kolor ścieżki
RED = QColor(255, 0, 0)  # Kolor wybranego pola


class GameScene(QGraphicsScene):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setSceneRect(0, 0, GRID_WIDTH * GRID_SIZE, GRID_HEIGHT * GRID_SIZE)
        self.selected_tiles = set()
        self.init_grid()

    def init_grid(self):
        """Tworzy siatkę planszy."""
        for x in range(GRID_WIDTH):
            for y in range(GRID_HEIGHT):
                tile = QGraphicsRectItem(x * GRID_SIZE, y * GRID_SIZE, GRID_SIZE, GRID_SIZE)
                if y == GRID_HEIGHT // 2:
                    tile.setBrush(QBrush(BROWN))  # Ścieżka przez środek
                else:
                    tile.setBrush(QBrush(GRAY))  # Szare tło
                tile.setPen(DARK_GRAY)
                tile.setData(0, (x, y))  # Przechowywanie pozycji
                tile.setAcceptHoverEvents(True)
                tile.setFlag(QGraphicsRectItem.ItemIsSelectable)
                self.addItem(tile)

    def mousePressEvent(self, event):
        """Obsługuje kliknięcie myszy, zmieniając kolor wybranego pola na czerwony."""
        item = self.itemAt(event.scenePos(), self.views()[0].transform())
        if item and isinstance(item, QGraphicsRectItem):
            pos = item.data(0)
            if pos in self.selected_tiles:
                item.setBrush(QBrush(GRAY if pos[1] != GRID_HEIGHT // 2 else BROWN))
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
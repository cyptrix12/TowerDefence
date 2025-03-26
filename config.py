from PyQt5.QtWidgets import QApplication
from PyQt5.QtGui import QGuiApplication

app = QApplication([])

screen = QGuiApplication.primaryScreen()
geometry = screen.geometry()
screen_width = geometry.width()
screen_height = geometry.height()

GRID_WIDTH = 10
GRID_HEIGHT = 10

GRID_SIZE = min(screen_width // GRID_WIDTH, screen_height // GRID_HEIGHT)
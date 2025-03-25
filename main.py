import sys
from PyQt5.QtWidgets import QApplication
from GameScene import GameScene
from GameView import GameView
from GameController import GameController

class Game:
    def __init__(self):
        self.scene = GameScene(None)  # Tymczasowo None
        self.controller = GameController(self.scene)  # Inicjalizacja kontrolera
        self.scene.controller = self.controller  # Przypisz kontroler do sceny
        self.view = GameView(self.scene)
        self.view.show()
        self.view.setMouseTracking(True)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    game = Game()
    sys.exit(app.exec_())
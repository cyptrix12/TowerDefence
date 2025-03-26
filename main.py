import sys
from PyQt5.QtWidgets import QApplication
from GameScene import GameScene
from GameView import GameView
from GameController import GameController

class Game:
    def __init__(self):
        self.scene = GameScene(None)
        self.controller = GameController(self.scene) 
        self.scene.controller = self.controller 
        self.view = GameView(self.scene)
        self.view.show()
        self.view.setMouseTracking(True)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    game = Game()
    sys.exit(app.exec_())
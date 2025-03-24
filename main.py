import sys
from PyQt5.QtWidgets import QApplication
from GameScene import GameScene
from GameView import GameView

class Game:
    def __init__(self):
        self.scene = GameScene()
        self.view = GameView(self.scene)
        self.view.show()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    game = Game()
    game.scene.addEnemy()
    game.scene.addTower(4,4)
    sys.exit(app.exec_())
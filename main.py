import sys
from PyQt5.QtWidgets import QApplication, QDialog
from GameScene import GameScene
from GameView import GameView
from GameController import GameController
from ConfigWindow import ConfigWindow
from GameConfig import Config

class Game:
    def __init__(self):
        self.scene = GameScene(None)
        self.controller = GameController(self.scene) 
        self.scene.set_controller(self.controller) 
        self.view = GameView(self.scene)
        self.scene.start_button.setParent(self.view) 
        self.view.show()
        self.view.setMouseTracking(True)

if __name__ == "__main__":
    app = QApplication(sys.argv)

    # Wyświetl okno konfiguracji
    config_window = ConfigWindow()
    if config_window.exec_() == QDialog.Accepted:
        grid_width, grid_height = config_window.get_config()
        print(f"Wybrane wartości: Grid Width = {grid_width}, Grid Height = {grid_height}")

        config = Config(grid_width, grid_height)

        print("zainicjowane")


        # Uruchom grę z wprowadzonymi wartościami
        game = Game()
        sys.exit(app.exec_())
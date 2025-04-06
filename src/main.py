import sys
from PyQt5.QtWidgets import QApplication, QDialog
from GameScene import GameScene
from GameView import GameView
from GameController import GameController
from ConfigWindow import ConfigWindow
from GameConfig import Config
from GameHistory import GameHistory

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

    config_window = ConfigWindow()
    if config_window.exec_() == QDialog.Accepted:
        config_data = config_window.get_config()
        grid_width = config_data["grid_width"]
        grid_height = config_data["grid_height"]
        endless_runner = config_data["endless_conquest"]
        game_mode = config_data["game_mode"]
        ip_address = config_data["ip"]
        port = config_data["port"]

        gamehistory = GameHistory()
        print(f"Wybrane wartości: Grid Width = {grid_width}, Grid Height = {grid_height}, Endless Runner = {endless_runner}")

        config = Config(grid_width, grid_height)
        config.set_endless_conquest(endless_runner)
        config.set_game_mode(game_mode)
        config.set_network_config(ip_address, port)

        game = Game()
        game.controller.endless_runner = endless_runner
        sys.exit(app.exec_())
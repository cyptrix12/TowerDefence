from Towers import AnimatedTower
from Enemies import AnimatedEnemy

from config import GRID_SIZE

class GameController:
    def __init__(self, scene):
        self.scene = scene
        self.lives = 3
        self.updateLifes()
        self.addEnemy()  # Dodaj pierwszego wroga
    

    def handle_mouse_event(self, event):
        """Obsługuje zdarzenia myszy."""
        pos = event.scenePos()
        x = int(pos.x() // GRID_SIZE)
        y = int(pos.y() // GRID_SIZE)
        if (x, y) not in self.scene.path:  # Upewnij się, że nie stawiamy wieży na ścieżce
            self.addTower(x, y)
            return True  # Zdarzenie zostało obsłużone
        else:
            self.addEnemy()
            return True
        return False

    def addTower(self, x, y):
        tower = AnimatedTower(x, y, self.scene)
        self.scene.addItem(tower)

    def addEnemy(self):
        enemy = AnimatedEnemy(self.scene.path[0][0], self.scene.path[0][1], self.scene.path, self.scene, self)
        self.scene.addItem(enemy)
        self.scene.add_health_bar(enemy)

    def decrease_lives(self):
        self.lives -= 1
        self.scene.lives_text.setPlainText(f"Lives: {self.lives}")
        if self.lives <= 0:
            print("Game Over!")

    def updateLifes(self):
        self.scene.lives_text.setPlainText(f"Lives: {self.lives}")
        if self.lives <= 0:
            print("Game Over!")
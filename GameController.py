from PyQt5.QtCore import Qt, QEvent, QTimer

from Towers import AnimatedTower
from Enemies import AnimatedEnemy
from GameConfig import Config


class GameController:
    def __init__(self, scene):
        self.config = Config()
        self.GRID_SIZE = self.config.get_grid_size()
        self.scene = scene
        self.lives = 3
        self.updateLifes()
        self.current_level = 0
        self.enemies_to_spawn = 0
        self.spawned_enemies = 0
        self.active_enemies = 0

    def EventFilter(self, obj, event):
        if event.type() == QEvent.GraphicsSceneMousePress:
            if event.button() == Qt.LeftButton:
                return self.handle_mouse_event(event)
        return False

    def handle_mouse_event(self, event):
        pos = event.scenePos()
        x = int(pos.x() // self.GRID_SIZE)
        y = int(pos.y() // self.GRID_SIZE)
        if (x, y) == (0, 0):
            self.scene.add_tower_palette()
            return False
        if (x, y) not in self.scene.path:
            self.addTower(x, y)
            return False
        else:
            self.addEnemy()
            return True
        return False

    def addTower(self, x, y):
        if (x, y) in self.scene.tower_positions:
            return
        if (x, y) in self.scene.path:
            return
        tower = AnimatedTower(x, y, self.scene)
        self.scene.addItem(tower)
        self.scene.tower_positions.add((x, y))

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

    def start_level(self):
        self.current_level += 1
        self.enemies_to_spawn = self.current_level
        self.spawned_enemies = 0
        self.active_enemies = 0
        self.scene.start_button.hide()
        self.spawn_wave()

    def spawn_wave(self):
        if self.spawned_enemies < self.enemies_to_spawn:
            self.spawn_enemy()
            QTimer.singleShot(500, self.spawn_wave) 
        else:
            self.check_level_end()

    def spawn_enemy(self):
        enemy = self.scene.enemy_class(self.scene.path[0][0], self.scene.path[0][1], self.scene.path, self.scene, self)
        self.scene.addItem(enemy)
        self.scene.add_health_bar(enemy)
        self.spawned_enemies += 1
        self.active_enemies += 1 

    def on_enemy_destroyed(self):
        self.active_enemies -= 1
        self.check_level_end()

    def check_level_end(self):
        if self.active_enemies == 0 and self.spawned_enemies == self.enemies_to_spawn:
            self.scene.start_button.show() 
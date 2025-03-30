from PyQt5.QtCore import Qt, QEvent, QTimer
from PyQt5.QtWidgets import QGraphicsTextItem
from PyQt5.QtGui import QFont, QColor

from Towers import AnimatedTower
from Enemies import AnimatedEnemy, FastEnemy
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
        self.endless_runner = False  
        self.w_pressed = False
        self.money = 100 
        self.scene.update_money(self.money)
        self.game_over = False

    def EventFilter(self, obj, event):
        if self.game_over:
            return True
        if event.type() == QEvent.KeyPress:
            if event.key() == Qt.Key_W:
                self.w_pressed = True
            if event.key() == Qt.Key_Space:
                self.scene.start_button.click()
        elif event.type() == QEvent.KeyRelease:
            if event.key() == Qt.Key_W:
                self.w_pressed = False
        if event.type() == QEvent.GraphicsSceneMousePress:
            if event.button() == Qt.LeftButton:
                return self.handle_mouse_event(event)
        return False

    def handle_mouse_event(self, event):
        if not self.w_pressed:
            return False
        pos = event.scenePos()
        x = int(pos.x() // self.GRID_SIZE)
        y = int(pos.y() // self.GRID_SIZE)
        if (x, y) == (0, 0):
            self.scene.add_tower_palette()
            return False
        if (x, y) not in self.scene.path:
            if self.money < 20:
                print("Not enough money!")
                return False
            self.money -= 20
            self.scene.update_money(self.money)
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
        for overlay in self.scene.overlay_items:
            if (x, y) == overlay["pos"]:
                return
        if x < 0 or y < 0 or x >= self.scene.GRID_WIDTH or y >= self.scene.GRID_HEIGHT:
            return
        tower = AnimatedTower(x, y, self.scene)
        self.scene.addItem(tower)
        self.scene.tower_positions.add((x, y))

    def addEnemy(self):
        enemy = AnimatedEnemy(self.scene.path[0][0], self.scene.path[0][1], self.scene.path, self.scene, self)
        self.scene.addItem(enemy)
        self.scene.add_health_bar(enemy)

    def addFastEnemy(self):
        enemy = FastEnemy(self.scene.path[0][0], self.scene.path[0][1], self.scene.path, self.scene, self)
        self.scene.addItem(enemy)
        self.scene.add_health_bar(enemy)

    def decrease_lives(self):
        self.lives -= 1
        self.scene.lives_text.setPlainText(f"Lives: {self.lives}")
        if self.lives <= 0 and not self.game_over:
            self.show_game_over()

    def updateLifes(self):
        self.scene.lives_text.setPlainText(f"Lives: {self.lives}")
        if self.lives <= 0 and not self.game_over:
            self.show_game_over()

    def show_game_over(self):
        game_over_text = QGraphicsTextItem("GAME OVER!")
        game_over_text.setDefaultTextColor(QColor(255, 0, 0))
        game_over_text.setFont(QFont("Arial", 48, QFont.Bold))
        scene_rect = self.scene.sceneRect()
        text_rect = game_over_text.boundingRect()
        game_over_text.setPos((scene_rect.width() - text_rect.width()) / 2,
                              (scene_rect.height() - text_rect.height()) / 2)
        print(f"self.scene.width() = {scene_rect.width()}")
        print(f"self.scene.height() = {scene_rect.height()}")
        self.scene.addItem(game_over_text)
        print("Game Over!")
        QTimer.singleShot(50, lambda: setattr(self, 'game_over', True))

    def start_level(self):
        if self.active_enemies > 0:
            print("Enemies are still alive!")
            return
        self.current_level += 1
        self.enemies_to_spawn = self.current_level
        self.spawned_enemies = 0
        self.active_enemies = 0
        self.scene.update_level(self.current_level)
        self.scene.start_button.hide() 
        self.spawn_wave()

    def spawn_wave(self):
        if self.spawned_enemies < self.enemies_to_spawn:
            self.spawn_enemy()
            QTimer.singleShot(500, self.spawn_wave)  
        else:
            self.check_level_end()

    def spawn_enemy(self):
        if (self.enemies_to_spawn - self.spawned_enemies) // 5 > 0:
            self.addFastEnemy()
            self.spawned_enemies += 5
        else:
            self.addEnemy()
            self.spawned_enemies += 1
        self.active_enemies += 1

    def on_enemy_destroyed(self, worth):
        self.active_enemies -= 1
        self.money += worth
        self.scene.update_money(self.money)
        self.check_level_end()

    def check_level_end(self):
        if self.active_enemies == 0 and self.spawned_enemies == self.enemies_to_spawn:
            if self.endless_runner:
                self.start_level()
            else:
                self.scene.start_button.show()
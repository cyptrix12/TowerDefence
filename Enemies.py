from PyQt5.QtCore import QTimer

from config import GRID_SIZE
from GameUnit import GameUnit

import assets_rc

class AnimatedEnemy(GameUnit):
    def __init__(self, x, y, path, scene, controller):
        super().__init__(
            x, y,
            sprite_path=":/assets/Enemies/spr_bat.png",
            frame_count=4,
            frame_duration=200
        )
        self.hp = 100
        self.max_hp = 100 

        self.path = path
        self.path_index = 0
        self.speed = 7
        self.scene = scene 
        self.controller = controller


        self.target_x = x * GRID_SIZE
        self.target_y = y * GRID_SIZE

        self.move_timer = QTimer()
        self.move_timer.timeout.connect(self.follow_path)
        self.move_timer.start(16)  # (60 FPS)

    def follow_path(self):
        if self.path_index < len(self.path):
            target_grid_pos = self.path[self.path_index]
            self.target_x = target_grid_pos[0] * GRID_SIZE
            self.target_y = target_grid_pos[1] * GRID_SIZE

            dx = self.target_x - self.x()
            dy = self.target_y - self.y()

            distance = (dx**2 + dy**2)**0.5

            if distance < self.speed:
                self.setPos(self.target_x, self.target_y)
                self.path_index += 1
            else:
                step_x = self.speed * dx / distance
                step_y = self.speed * dy / distance
                self.setPos(self.x() + step_x, self.y() + step_y)
        else:
            self.controller.decrease_lives()
            self.scene.remove_health_bar(self)  
            self.scene.removeItem(self) 
            self.move_timer.stop()

    def take_damage(self, damage):
        self.hp -= damage
        if self.hp <= 0:
            self.scene.remove_health_bar(self)  
            self.scene.removeItem(self) 
            self.move_timer.stop()
        else:
            self.scene.update_health_bar(self) 


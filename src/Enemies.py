from PyQt5.QtCore import QTimer

from GameUnit import GameUnit
from GameConfig import Config

import assets_rc

class AnimatedEnemy(GameUnit):
    def __init__(self, x, y, path, scene, controller, frame_count=4, sprite_path=":/assets/Enemies/spr_bat.png"):   
        super().__init__(
            x, y,
            sprite_path=sprite_path,
            frame_count=frame_count,
            frame_duration=200
        )
        self.config = Config()
        self.GRID_SIZE = self.config.get_grid_size()

        self.hp = 100
        self.max_hp = 100 


        self.worth = 10 

        self.path = path
        self.path_index = 0
        self.speed = 5
        self.speed = self.speed * self.GRID_SIZE / 50  # Speed in pixels per millisecond
        self.scene = scene 
        self.controller = controller

        self.target_x = x * self.GRID_SIZE
        self.target_y = y * self.GRID_SIZE

        self.move_timer = QTimer()
        self.move_timer.timeout.connect(self.follow_path)
        self.move_timer.start(16)  # (60 FPS)
    
    def take_damage(self, damage):
        self.hp -= damage
        if self.hp <= 0:
            self.scene.remove_health_bar(self)
            self.scene.removeItem(self)
            print("Enemy destroyed!")
            self.move_timer.stop()
            self.controller.on_enemy_destroyed(self.worth)
        else:
            self.scene.update_health_bar(self)

    def follow_path(self):
        if self.path_index < len(self.path):
            target_grid_pos = self.path[self.path_index]
            self.target_x = target_grid_pos[0] * self.GRID_SIZE
            self.target_y = target_grid_pos[1] * self.GRID_SIZE

            dx = self.target_x - self.x()
            dy = self.target_y - self.y()

            distance = (dx**2 + dy**2)**0.5

            time_to_target = distance / self.speed

            if time_to_target <= 1:  
                self.setPos(self.target_x, self.target_y)
                self.path_index += 1
            else:
                step_x = dx / time_to_target
                step_y = dy / time_to_target
                self.setPos(self.x() + step_x, self.y() + step_y)
        else:
            self.controller.decrease_lives()
            self.scene.remove_health_bar(self)  
            self.scene.removeItem(self) 
            self.move_timer.stop()
            self.controller.on_enemy_destroyed(self.worth)

class FastEnemy(AnimatedEnemy):
    def __init__(self, x, y, path, scene, controller):
        super().__init__(
            x, y, path, scene, controller, frame_count=8, sprite_path = ":/assets/Enemies/spr_ghost.png"
        )
        
        self.hp = 50
        self.max_hp = 50
        self.worth = 20
        self.speed = 10  # Faster speed
        self.speed = self.speed * self.GRID_SIZE / 50  

class TankEnemy(AnimatedEnemy):
    def __init__(self, x, y, path, scene, controller):
        super().__init__(
            x, y, path, scene, controller, frame_count=4, sprite_path = ":/assets/Enemies/spr_big_slime.png"
        )
        
        self.hp = 200
        self.max_hp = 200
        self.worth = 30
        self.speed = 3  # Slower speed
        self.speed = self.speed * self.GRID_SIZE / 50

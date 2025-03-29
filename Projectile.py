from PyQt5.QtCore import QTimer, QLineF
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QGraphicsPixmapItem

from GameConfig import Config

import assets_rc

class Projectile(QGraphicsPixmapItem):
    def __init__(self, x, y, target, damage, scene):
        super().__init__()
        self.config = Config()
        self.GRID_SIZE = self.config.get_grid_size()
        self.setPixmap(QPixmap(":/assets/Towers/Combat Towers Projectiles/spr_tower_archer_projectile.png").scaled(self.GRID_SIZE//4, self.GRID_SIZE//4))
        self.setPos(x, y)

        self.target = target
        self.damage = damage
        self.scene = scene
        self.speed = 20 

        dx = self.target.x() - self.x()
        dy = self.target.y() - self.y()
        angle = QLineF(0, 0, dx, dy).angle() 
        self.setRotation(-angle)

        self.timer = QTimer()
        self.timer.timeout.connect(self.move)
        self.timer.start(16)  # (60 FPS)

    def move(self):
        if not self.scene.items().__contains__(self.target):
            self.scene.removeItem(self)
            self.timer.stop()
            return

        dx = self.target.x() - self.x()
        dy = self.target.y() - self.y()
        distance = (dx**2 + dy**2)**0.5
        angle = QLineF(0, 0, dx, dy).angle()  
        self.setRotation(-angle)  

        if distance < self.speed:
            self.target.take_damage(self.damage)  
            self.scene.removeItem(self)  
            self.timer.stop()
        else:
            step_x = self.speed * dx / distance
            step_y = self.speed * dy / distance
            self.setPos(self.x() + step_x, self.y() + step_y)
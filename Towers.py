from PyQt5.QtCore import QTimer, QPointF, QEvent
from PyQt5.QtGui import QColor
from PyQt5.QtWidgets import QGraphicsEllipseItem, QGraphicsItem
from GameUnit import GameUnit
from GameConfig import Config

from Projectile import Projectile

import assets_rc

class AnimatedTower(GameUnit):
    def __init__(self, x, y, scene):
        super().__init__(
            x, y,
            sprite_path=":/assets/Towers/Combat Towers/spr_tower_lightning_tower.png",
            frame_count=1,
            frame_duration=0
        )
        self.config = Config()
        self.GRID_SIZE = self.config.get_grid_size()
        self.scene = scene
        self.range = 3 * self.GRID_SIZE
        self.damage = 10

        # self.setFlag(QGraphicsItem.ItemIsMovable, True)
        # self.setFlag(QGraphicsItem.ItemIsSelectable, True)

        self.attack_timer = QTimer()
        self.attack_timer.timeout.connect(self.attack_enemies)
        self.attack_timer.start(1000) 

    def attack_enemies(self):
        nearest_enemy = None
        nearest_distance = float('inf')

        for enemy in self.scene.items():
            if isinstance(enemy, GameUnit) and isinstance(enemy, self.scene.enemy_class): 
                distance = self.distance_to(enemy)
                if distance < nearest_distance:
                    nearest_distance = distance
                    nearest_enemy = enemy

        if nearest_distance <= self.range:
            self.create_projectile(nearest_enemy)

    def create_projectile(self, target):
        projectile = Projectile(self.x() + self.GRID_SIZE / 2, self.y() + self.GRID_SIZE / 2, target, self.damage, self.scene)
        self.scene.addItem(projectile)

    def distance_to(self, target):
        dx = (target.x() - self.x())
        dy = (target.y() - self.y())
        return (dx**2 + dy**2)**0.5
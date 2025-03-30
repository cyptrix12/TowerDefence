from PyQt5.QtCore import QTimer, QPointF, QEvent
from PyQt5.QtGui import QColor
from PyQt5.QtWidgets import QGraphicsEllipseItem, QGraphicsItem, QGraphicsPixmapItem
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
        self.damage = 20
        self.attack_speed = 1000

        self.buff_icons = []

        self.apply_buffs()

        self.attack_timer = QTimer()
        self.attack_timer.timeout.connect(self.attack_enemies)
        self.attack_timer.start(self.attack_speed)

    def apply_buffs(self):
        adjacent_overlays = self.scene.get_adjacent_overlays(self.grid_x, self.grid_y)

        for icon in self.buff_icons:
            self.scene.removeItem(icon)
        self.buff_icons.clear()

        for overlay in adjacent_overlays:
            overlay_type = overlay["type"]
            overlay_pixmap = overlay["item"].pixmap() 

            if overlay_type == "mushroom":
                self.attack_speed = max(500, self.attack_speed - 200)
                print("Buff: Attack speed increased!")
                self.add_buff_icon(overlay_pixmap, overlay_type)

            if overlay_type == "rock":
                self.damage *= 2
                print("Buff: Damage increased!")
                self.add_buff_icon(overlay_pixmap, overlay_type)

            if overlay_type == "tree":
                self.range = max(self.GRID_SIZE, self.range - self.GRID_SIZE)
                print("Buff: Range decreased!")
                self.add_buff_icon(overlay_pixmap, overlay_type)

    def add_buff_icon(self, pixmap, type):
        icon_pixmap = pixmap.scaled(self.GRID_SIZE // 3, self.GRID_SIZE // 3)
        icon_item = QGraphicsPixmapItem(icon_pixmap)
        icon_item.setParentItem(self) 
        x_shift = - (self.GRID_SIZE // 4)
        if type == "mushroom":
            x_shift += 4*self.GRID_SIZE // 6
        elif type == "rock":
            x_shift += (2*self.GRID_SIZE) // 6
        elif type == "tree":
            x_shift += 0
        icon_item.setPos(self.grid_x * self.GRID_SIZE + x_shift, self.grid_y * self.GRID_SIZE - self.GRID_SIZE // 3) 
        self.buff_icons.append(icon_item)
        self.scene.addItem(icon_item)

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
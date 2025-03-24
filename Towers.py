from PyQt5.QtCore import QTimer, QPointF
from PyQt5.QtGui import QColor
from PyQt5.QtWidgets import QGraphicsEllipseItem
from GameUnit import GameUnit
from config import GRID_SIZE
from Projectile import Projectile

import assets_rc

class AnimatedTower(GameUnit):
    def __init__(self, x, y, scene):
        super().__init__(
            x, y,
            sprite_path=":/assets/Towers/Castle/spr_castle_blue.png",
            frame_count=4,
            frame_duration=200
        )
        self.scene = scene
        self.range = 3 * GRID_SIZE  # Zasięg wieży w pikselach
        self.damage = 10  # Obrażenia zadawane przez pocisk

        # Timer do atakowania wrogów
        self.attack_timer = QTimer()
        self.attack_timer.timeout.connect(self.attack_enemies)
        self.attack_timer.start(1000)  # Atak co 1000 ms (1 sekunda)

    def attack_enemies(self):
        """Sprawdza wrogów w zasięgu i tworzy pocisk w ich kierunku."""
        for enemy in self.scene.items():
            if isinstance(enemy, GameUnit) and isinstance(enemy, self.scene.enemy_class):  # Sprawdź, czy to wróg
                distance = self.distance_to(enemy)
                if distance <= self.range:
                    self.create_projectile(enemy)

    def create_projectile(self, target):
        """Tworzy pocisk i kieruje go w stronę celu."""
        projectile = Projectile(self.x() + GRID_SIZE / 2, self.y() + GRID_SIZE / 2, target, self.damage, self.scene)
        self.scene.addItem(projectile)

    def distance_to(self, target):
        """Oblicza odległość od wieży do celu."""
        dx = (target.x() - self.x())
        dy = (target.y() - self.y())
        return (dx**2 + dy**2)**0.5
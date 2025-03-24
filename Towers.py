from PyQt5.QtCore import QTimer, QPointF
from GameUnit import GameUnit
from config import GRID_SIZE

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
        self.damage = 30  # Obrażenia zadawane na sekundę

        # Timer do atakowania wrogów
        self.attack_timer = QTimer()
        self.attack_timer.timeout.connect(self.attack_enemies)
        self.attack_timer.start(1000)  # Atak co 1000 ms (1 sekunda)

    def attack_enemies(self):
        """Sprawdza wrogów w zasięgu i zadaje im obrażenia."""
        for enemy in self.scene.items():
            if isinstance(enemy, GameUnit) and isinstance(enemy, self.scene.enemy_class):  # Sprawdź, czy to wróg
                distance = self.distance_to(enemy)
                if distance <= self.range:
                    enemy.take_damage(self.damage)

    def distance_to(self, target):
        """Oblicza odległość od wieży do celu."""
        dx = (target.x() - self.x())
        dy = (target.y() - self.y())
        return (dx**2 + dy**2)**0.5
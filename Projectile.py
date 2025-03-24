from PyQt5.QtCore import QTimer, QPointF
from PyQt5.QtGui import QColor
from PyQt5.QtWidgets import QGraphicsEllipseItem

class Projectile(QGraphicsEllipseItem):
    def __init__(self, x, y, target, damage, scene):
        super().__init__(-5, -5, 10, 10)  # Pocisk o średnicy 10 pikseli
        self.setBrush(QColor(255, 0, 0))  # Czerwony kolor
        self.setPos(x, y)

        self.target = target
        self.damage = damage
        self.scene = scene
        self.speed = 10  # Prędkość pocisku (piksele na iterację)

        # Timer do animacji pocisku
        self.timer = QTimer()
        self.timer.timeout.connect(self.move)
        self.timer.start(16)  # Wywołanie co ~16 ms (60 FPS)

    def move(self):
        """Przesuwa pocisk w stronę celu."""
        if not self.scene.items().__contains__(self.target):
            # Jeśli cel został usunięty, usuń pocisk
            self.scene.removeItem(self)
            self.timer.stop()
            return

        dx = self.target.x() - self.x()
        dy = self.target.y() - self.y()
        distance = (dx**2 + dy**2)**0.5

        if distance < self.speed:
            # Jeśli pocisk dotarł do celu
            self.target.take_damage(self.damage)  # Zadaj obrażenia
            self.scene.removeItem(self)  # Usuń pocisk
            self.timer.stop()
        else:
            # Przesuń pocisk w stronę celu
            step_x = self.speed * dx / distance
            step_y = self.speed * dy / distance
            self.setPos(self.x() + step_x, self.y() + step_y)
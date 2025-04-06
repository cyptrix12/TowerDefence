from PyQt5.QtCore import Qt, QEvent, QTimer
from PyQt5.QtWidgets import QGraphicsTextItem, QGraphicsPixmapItem
from PyQt5.QtGui import QFont, QColor, QPixmap

from Towers import AnimatedTower, LightningTower
from Enemies import AnimatedEnemy, FastEnemy, TankEnemy
from GameConfig import Config
from GameHistory import GameHistory



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
        self.pressed_keys = set()
        self.money = 100 
        self.scene.update_money(self.money)
        self.game_over = False
        self.game_history = GameHistory()

    def EventFilter(self, obj, event):
        if self.game_over:
            return True
        if event.type() == QEvent.KeyPress:
            self.pressed_keys.add(event.key())
            if event.key() == Qt.Key_Space:
                self.scene.start_button.click()
        elif event.type() == QEvent.KeyRelease:
            self.pressed_keys.discard(event.key())
        if event.type() == QEvent.GraphicsSceneMousePress:
            if event.button() == Qt.LeftButton:
                return self.handle_mouse_event(event)
        return False

    def handle_mouse_event(self, event):
        pos = event.scenePos()
        clicked_items = self.scene.items(pos) 

        if len(clicked_items) != 0:
            for item in clicked_items:
                if isinstance(item, AnimatedTower) and Qt.Key_W in self.pressed_keys:
                    if self.money < 10:
                        print("Not enough money to upgrade the tower!")
                        return False

                    self.money -= 10
                    self.scene.update_money(self.money)

                    item.upgrade()
                    print(f"Tower upgraded! New damage: {item.damage}, new range: {item.range}")
                    return True

        x = int(pos.x() // self.GRID_SIZE)
        y = int(pos.y() // self.GRID_SIZE)
        if (x ,y) in self.scene.tower_positions:
            return False
            
        if (x, y) not in self.scene.get_path():
            if self.addTower(x, y, tower_type="lightning" if Qt.Key_L in self.pressed_keys else "archer"):
                self.scene.update_money(self.money)
                return True
            else:
                return False
        else:
            self.addEnemy()
            return True
        return False

    def addTower(self, x, y, tower_type="archer"):
        if (x, y) in self.scene.tower_positions:
            return False
        if (x, y) in self.scene.path:
            return False 
        for overlay in self.scene.overlay_items:
            if (x, y) == overlay["pos"]:
                return False
        if x < 0 or y < 0 or x >= self.scene.GRID_WIDTH or y >= self.scene.GRID_HEIGHT:
            return False
        if tower_type == "archer":
            tower = AnimatedTower(x, y, self.scene)
            if self.money < 20:
                print("Not enough money!")
                return False
            self.money -= 20
        elif tower_type == "lightning":
            tower = LightningTower(x, y, self.scene)
            if self.money < 80:
                print("Not enough money!")
                return False
            self.money -= 80
        else:
            print("Invalid tower type!")
            return False
        self.scene.addItem(tower)
        self.scene.tower_positions.add((x, y))
        return True

    def addEnemy(self):
        enemy = AnimatedEnemy(self.scene.path[0][0], self.scene.path[0][1], self.scene.path, self.scene, self)
        self.scene.addItem(enemy)
        self.scene.add_health_bar(enemy)

    def addFastEnemy(self):
        enemy = FastEnemy(self.scene.path[0][0], self.scene.path[0][1], self.scene.path, self.scene, self)
        self.scene.addItem(enemy)
        self.scene.add_health_bar(enemy)

    def addTankEnemy(self):
        enemy = TankEnemy(self.scene.path[0][0], self.scene.path[0][1], self.scene.path, self.scene, self)
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
        if (self.enemies_to_spawn - self.spawned_enemies) // 10 > 0:
            self.addTankEnemy()
            self.spawned_enemies += 10
        elif (self.enemies_to_spawn - self.spawned_enemies) // 5 > 0:
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
            towers = [item for item in self.scene.items() if isinstance(item, AnimatedTower)]
            tower_data = [
            {
                "position": {"x": tower.x() // self.GRID_SIZE, "y":tower.y() // self.GRID_SIZE},
                "type": tower.type_str,
                "level": tower.upgrade_count
            }
            for tower in towers
            ]

            overlay_data = [
                {"type": overlay["type"], "position": {"x": overlay["pos"][0], "y": overlay["pos"][1]}}
                for overlay in self.scene.overlay_items
            ]

            self.game_history.update_state(
                grid=self.scene.path,
                overlay_items=overlay_data,
                towers=tower_data,
                level=self.current_level,
                money=self.money,
                lives=self.lives,
                config=self.config.get_config()
            )

    def load_game(self):
        """Wczytuje zapis gry z pliku JSON i aktualizuje stan gry."""
        game_history = GameHistory()
        try:
            state = game_history.state

            # Aktualizuj stan gry
            self.lives = int(state["lives"])
            self.money = int(state["money"])
            self.current_level = int(state["level"])
            self.scene.path = [tuple(pos) for pos in state["grid"]]


            # Aktualizuj teksty w scenie
            # Odśwież siatkę
            self.scene.init_path_tiles()
            self.scene.init_grid(False)

            


            # Dodaj elementy overlay
            for overlay_data in state["overlay_items"]:
                position = overlay_data["position"]
                overlay_type = overlay_data["type"]
                x, y = int(position["x"]), int(position["y"])
                if overlay_type == "mushroom":
                    overlay_source = ":/assets/Environment/Decoration/spr_mushroom_01.png"
                elif overlay_type == "rock":
                    overlay_source = ":/assets/Environment/Decoration/spr_rock_01.png"
                elif overlay_type == "tree":
                    overlay_source = ":/assets/Environment/Decoration/spr_tree_01_normal.png"
                overlay_pixmap = QPixmap(overlay_source).scaled(self.GRID_SIZE // 3, self.GRID_SIZE // 3)
                overlay_item = QGraphicsPixmapItem(overlay_pixmap)
                overlay_item.setPos(x * self.GRID_SIZE, y * self.GRID_SIZE)
                self.scene.addItem(overlay_item)
                self.scene.overlay_items.append({"item": overlay_item, "type": overlay_type, "pos": (x, y)})

            # Dodaj wieże
            for tower_data in state["towers"]:
                position = tower_data["position"]
                tower_type = tower_data["type"]
                level = int(tower_data["level"])
                x, y = int(position["x"]), int(position["y"])
                if tower_type == "archer":
                    tower = AnimatedTower(x, y, self.scene)
                elif tower_type == "lightning":
                    tower = LightningTower(x, y, self.scene)
                else:
                    continue
                for _ in range(level):
                    tower.upgrade()
                self.scene.addItem(tower)
                self.scene.tower_positions.add((x, y))

            self.scene.second_init()
            self.updateLifes()
            self.scene.update_level(self.current_level)
            self.scene.update_money(self.money)

            print("Gra została wczytana pomyślnie!")
        except Exception as e:
            print(f"Błąd podczas wczytywania gry: {e}")


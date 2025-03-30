from PyQt5.QtWidgets import QApplication, QGraphicsScene, QGraphicsView, QGraphicsRectItem
from PyQt5.QtCore import Qt, QRectF, QPointF, QTimer
from PyQt5.QtGui import QBrush, QColor
import sys
import heapq

GRID_SIZE = 10
TILE_SIZE = 50

class Tile(QGraphicsRectItem):
    def __init__(self, x, y, is_obstacle=False):
        super().__init__(0, 0, TILE_SIZE, TILE_SIZE)
        self.setPos(x * TILE_SIZE, y * TILE_SIZE)
        self.x, self.y = x, y
        self.is_obstacle = is_obstacle
        self.update_color()

    def update_color(self):
        color = QColor('gray') if self.is_obstacle else QColor('white')
        self.setBrush(QBrush(color))
        self.setPen(QColor('black'))

class Unit(QGraphicsRectItem):
    def __init__(self, x, y):
        super().__init__(0, 0, TILE_SIZE * 0.8, TILE_SIZE * 0.8)
        self.setBrush(QBrush(QColor('blue')))
        self.setZValue(1)
        self.setPos(x * TILE_SIZE + TILE_SIZE*0.1, y * TILE_SIZE + TILE_SIZE*0.1)
        self.grid_pos = (x, y)
        self.setFlag(QGraphicsRectItem.ItemIsMovable)
        self.setFlag(QGraphicsRectItem.ItemSendsGeometryChanges)

    def move_to(self, path):
        self.path = path
        self.step_index = 0
        self.timer = QTimer()
        self.timer.timeout.connect(self.step_along_path)
        self.timer.start(300)

    def step_along_path(self):
        if self.step_index >= len(self.path):
            self.timer.stop()
            return
        x, y = self.path[self.step_index]
        self.setPos(x * TILE_SIZE + TILE_SIZE*0.1, y * TILE_SIZE + TILE_SIZE*0.1)
        self.grid_pos = (x, y)
        self.step_index += 1

class GameScene(QGraphicsScene):
    def __init__(self):
        super().__init__(0, 0, GRID_SIZE * TILE_SIZE, GRID_SIZE * TILE_SIZE)
        self.tiles = {}
        for y in range(GRID_SIZE):
            for x in range(GRID_SIZE):
                is_obstacle = (x + y) % 7 == 0 and (x, y) != (0, 0)
                tile = Tile(x, y, is_obstacle)
                self.addItem(tile)
                self.tiles[(x, y)] = tile
        self.unit = Unit(0, 0)
        self.addItem(self.unit)

    def mouseReleaseEvent(self, event):
        if self.unit.isUnderMouse():
            scene_pos = event.scenePos()
            grid_x = int(scene_pos.x() / TILE_SIZE)
            grid_y = int(scene_pos.y() / TILE_SIZE)
            if (grid_x, grid_y) in self.tiles and not self.tiles[(grid_x, grid_y)].is_obstacle:
                path = self.find_path(self.unit.grid_pos, (grid_x, grid_y))
                if path:
                    self.unit.move_to(path)

    def find_path(self, start, goal):
        open_set = [(0, start)]
        came_from = {}
        cost_so_far = {start: 0}

        while open_set:
            _, current = heapq.heappop(open_set)
            if current == goal:
                break
            for dx, dy in [(-1,0),(1,0),(0,-1),(0,1)]:
                nx, ny = current[0]+dx, current[1]+dy
                next_pos = (nx, ny)
                if 0 <= nx < GRID_SIZE and 0 <= ny < GRID_SIZE:
                    if self.tiles[next_pos].is_obstacle:
                        continue
                    new_cost = cost_so_far[current] + 1
                    if next_pos not in cost_so_far or new_cost < cost_so_far[next_pos]:
                        cost_so_far[next_pos] = new_cost
                        priority = new_cost + abs(goal[0]-nx) + abs(goal[1]-ny)
                        heapq.heappush(open_set, (priority, next_pos))
                        came_from[next_pos] = current

        if goal not in came_from:
            return None

        path = []
        current = goal
        while current != start:
            path.append(current)
            current = came_from[current]
        path.reverse()
        return path

if __name__ == '__main__':
    app = QApplication(sys.argv)
    view = QGraphicsView()
    scene = GameScene()
    view.setScene(scene)
    view.show()
    sys.exit(app.exec_())
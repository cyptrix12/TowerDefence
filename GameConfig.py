from PyQt5.QtGui import QGuiApplication

class Config:
    _instance = None  # Statyczna zmienna przechowująca jedyną instancję klasy

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(Config, cls).__new__(cls)
        return cls._instance

    def __init__(self, width=50, height=50):
        if not hasattr(self, "initialized"):  # Zapobiega wielokrotnej inicjalizacji
            screen = QGuiApplication.primaryScreen()
            geometry = screen.geometry()
            self.screen_width = geometry.width()
            self.screen_height = geometry.height()

            self.grid_width = width
            self.grid_height = height
            self.grid_size = self.calculate_grid_size()
            self.initialized = True  # Flaga, aby uniknąć ponownej inicjalizacji

    def calculate_grid_size(self):
        return min(
            self.screen_width // self.grid_width - 1,
            int(0.8 * self.screen_height) // self.grid_height
        )

    def set_grid_dimensions(self, width, height):
        self.grid_width = width
        self.grid_height = height
        self.grid_size = self.calculate_grid_size()

    def get_grid_width(self):
        return self.grid_width

    def get_grid_height(self):
        return self.grid_height

    def get_grid_size(self):
        return self.grid_size
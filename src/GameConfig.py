from PyQt5.QtGui import QGuiApplication

# Singleton

class Config:
    _instance = None  

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(Config, cls).__new__(cls)
        return cls._instance

    def __init__(self, width=50, height=50):
        if not hasattr(self, "initialized"):  
            screen = QGuiApplication.primaryScreen()
            geometry = screen.geometry()
            self.screen_width = geometry.width()
            self.screen_height = geometry.height()

            # Domyślne wartości konfiguracji
            self.grid_width = width
            self.grid_height = height
            self.grid_size = self.calculate_grid_size()

            self.endless_conquest = False
            self.game_mode = "Single player"
            self.ip_address = "127.0.0.1"
            self.port = "8080"

            self.initialized = True  

    def calculate_grid_size(self):
        return min(
            self.screen_width // self.grid_width - 1,
            int(0.8 * self.screen_height) // self.grid_height
        )

    # Metody do ustawiania i pobierania konfiguracji
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

    def set_endless_conquest(self, endless_conquest):
        self.endless_conquest = endless_conquest

    def get_endless_conquest(self):
        return self.endless_conquest

    def set_game_mode(self, game_mode):
        self.game_mode = game_mode

    def get_game_mode(self):
        return self.game_mode

    def set_network_config(self, ip_address, port):
        self.ip_address = ip_address
        self.port = port

    def get_network_config(self):
        return {"ip_address": self.ip_address, "port": self.port}
    
    def get_config(self):
        return {
            "grid_width": self.grid_width,
            "grid_height": self.grid_height,
            "endless_conquest": self.endless_conquest,
            "game_mode": self.game_mode,
            "ip_address": self.ip_address,
            "port": self.port
        }
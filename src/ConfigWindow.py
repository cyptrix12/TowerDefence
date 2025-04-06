from PyQt5.QtWidgets import (
    QDialog, QVBoxLayout, QLabel, QLineEdit, QPushButton, QCheckBox, QRadioButton, QButtonGroup, QHBoxLayout
)
from PyQt5.QtGui import QIntValidator

class ConfigWindow(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Game Configuration")
        self.setGeometry(100, 100, 400, 300)

        # Layout
        layout = QVBoxLayout()

        # Grid Width
        self.grid_width_label = QLabel("Grid Width:")
        self.grid_width_input = QLineEdit()
        self.grid_width_input.setText("10")
        layout.addWidget(self.grid_width_label)
        layout.addWidget(self.grid_width_input)

        # Grid Height
        self.grid_height_label = QLabel("Grid Height:")
        self.grid_height_input = QLineEdit()
        self.grid_height_input.setText("10")
        layout.addWidget(self.grid_height_label)
        layout.addWidget(self.grid_height_input)

        # Endless conquest Checkbox
        self.endless_conquest_checkbox = QCheckBox("Endless conquest")
        layout.addWidget(self.endless_conquest_checkbox)

        # Game Mode (Radio Buttons)
        self.game_mode_label = QLabel("Game mode:")
        layout.addWidget(self.game_mode_label)

        self.game_mode_group = QButtonGroup(self)
        self.single_player_radio = QRadioButton("Single player")
        self.local_multiplayer_radio = QRadioButton("Local multiplayer")
        self.network_game_radio = QRadioButton("Network game")
        self.single_player_radio.setChecked(True)

        self.game_mode_group.addButton(self.single_player_radio)
        self.game_mode_group.addButton(self.local_multiplayer_radio)
        self.game_mode_group.addButton(self.network_game_radio)

        layout.addWidget(self.single_player_radio)
        layout.addWidget(self.local_multiplayer_radio)
        layout.addWidget(self.network_game_radio)

        # IP Address and Port
        self.ip_label = QLabel("Ip addres:")
        layout.addWidget(self.ip_label)

        self.ip_input = QLineEdit()
        self.ip_input.setPlaceholderText("Insert IP addres (ex. 192.168.1.1)")
        layout.addWidget(self.ip_input)

        self.port_label = QLabel("Port:")
        layout.addWidget(self.port_label)

        self.port_input = QLineEdit()
        self.port_input.setValidator(QIntValidator(1, 65535))
        self.port_input.setPlaceholderText("Insert port (ex. 8080)")
        layout.addWidget(self.port_input)

        # Load Game Button
        self.load_game_button = QPushButton("Load Game")
        self.load_game_button.clicked.connect(self.load_game_clicked)
        layout.addWidget(self.load_game_button)

        # Start Button
        self.start_button = QPushButton("Start")
        self.start_button.clicked.connect(self.accept)
        layout.addWidget(self.start_button)

        self.setLayout(layout)
        self.load_game_selected = False

    def load_game_clicked(self):
        """Ustawia flagę, że użytkownik wybrał opcję 'Load Game'."""
        self.load_game_selected = True
        self.accept()

    def is_load_game_selected(self):
        """Zwraca True, jeśli użytkownik wybrał opcję 'Load Game'."""
        return self.load_game_selected

    def get_config(self):
        grid_width = int(self.grid_width_input.text())
        grid_height = int(self.grid_height_input.text())
        endless_conquest = self.endless_conquest_checkbox.isChecked()
        game_mode = (
            "Single player" if self.single_player_radio.isChecked()
            else "Local multiplayer" if self.local_multiplayer_radio.isChecked()
            else "Network game"
        )
        ip = self.ip_input.text()
        port = self.port_input.text()
        return {
            "grid_width": grid_width,
            "grid_height": grid_height,
            "endless_conquest": endless_conquest,
            "game_mode": game_mode,
            "ip": ip,
            "port": port
        }
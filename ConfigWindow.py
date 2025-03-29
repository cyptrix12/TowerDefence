from PyQt5.QtWidgets import QDialog, QVBoxLayout, QLabel, QLineEdit, QPushButton

class ConfigWindow(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Konfiguracja Gry")
        self.setGeometry(100, 100, 300, 200)

        # Layout
        layout = QVBoxLayout()

        # Grid Width
        self.grid_width_label = QLabel("Grid Width:")
        self.grid_width_input = QLineEdit()
        self.grid_width_input.setText("50")  # Domyślna wartość
        layout.addWidget(self.grid_width_label)
        layout.addWidget(self.grid_width_input)

        # Grid Height
        self.grid_height_label = QLabel("Grid Height:")
        self.grid_height_input = QLineEdit()
        self.grid_height_input.setText("50")  # Domyślna wartość
        layout.addWidget(self.grid_height_label)
        layout.addWidget(self.grid_height_input)

        # Start Button
        self.start_button = QPushButton("Start")
        self.start_button.clicked.connect(self.accept)  # Zatwierdź i zamknij okno
        layout.addWidget(self.start_button)

        self.setLayout(layout)

    def get_config(self):
        """Zwraca wprowadzone wartości jako int."""
        grid_width = int(self.grid_width_input.text())
        grid_height = int(self.grid_height_input.text())
        return grid_width, grid_height
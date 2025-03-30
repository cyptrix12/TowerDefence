# TowerDefence

A Tower Defence game written in Python using the PyQt5 framework.

## 🔍 Overview

**TowerDefence** is a real-time strategy game where the player must defend territory from waves of incoming enemies by deploying and upgrading defensive units.

### Features:

- Map implemented with `QGraphicsScene`
- Units and terrain as custom `QGraphicsItem` subclasses
- Interactive unit control (selection, leveling up, appearance upgrades)
- Keyboard-based army control
- Optional drag-and-drop unit control with automatic pathfinding
- Graphics loaded from `.rc` file
- 3 types of enemies with different behavior (random, strategist, aggressor)
- Random map generation (configurable size, e.g. 50x50)
- Terrain-based combat modifiers (castles, forests, mountains)
- Unit and combat animations
- 3D FPP/TPP gameplay mode (optional)
- Endless Conquest mode – survive infinite enemy waves
- Story mode with missions and narration
- Gesture-based control via camera (hand movement recognition)
- Logging system with rotating logs (console + QTextEdit)

## ⚙️ Installation

### 1. Clone the repository

```bash
git clone https://github.com/cyptrix12/TowerDefence.git
cd TowerDefence
```

### 2. Set up a virtual environment (optional but recommended)

```bash
python -m venv venv
source venv/bin/activate      # macOS/Linux
venv\Scripts\activate         # Windows
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Run the game

```bash
cd src
python main.py
```

### 5. Configurate the game

Choose grid size, and allow Endless Conquest mode (optional) 

## 🧪 Requirements

- Python 3.8+
- PyQt5
- OS: Windows / Linux / macOS

## 👨‍💻 Author

Created by [@cyptrix12](https://github.com/cyptrix12) as a university project.

---

Have fun defending your territory! 🛡️

# TowerDefence

A Tower Defence game written in Python using the PyQt5 framework.

## 🔍 Overview

**TowerDefence** is a real-time strategy game where the player must defend territory from waves of incoming enemies by deploying and upgrading defensive units.

### Features:

- [x] Map implemented with `QGraphicsScene`
- [x] Units and terrain as custom `QGraphicsItem` subclasses
- [x] Interactive unit control (selection, leveling up, appearance upgrades)
- [x] Keyboard-based army control
- [x] Optional drag-and-drop unit control with automatic pathfinding
- [x] Graphics loaded from `.rc` file
- [x] 3 types of enemies with different behavior (random, strategist, aggressor)
- [x] Random map generation (configurable size, e.g. 50x50)
- [x] Terrain-based combat modifiers (castles, forests, mountains)
- [x] Unit and combat animations
- [x] 3D FPP/TPP gameplay mode (optional)
- [x] Endless Conquest mode – survive infinite enemy waves
- [x] Story mode with missions and narration
- [x] Gesture-based control via camera (hand movement recognition)
- [x] Logging system with rotating logs (console + QTextEdit)

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

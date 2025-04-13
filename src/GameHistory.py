import json
import xml.etree.ElementTree as ET
from pymongo import MongoClient

class GameHistory:
    _instance = None  # Singleton

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(GameHistory, cls).__new__(cls, *args, **kwargs)
        return cls._instance

    def __init__(self):
        if not hasattr(self, "state"):
            self.state = {
                "grid": [],
                "overlay_items": [],
                "towers": [],
                "level": 0,
                "money": 0,
                "lives": 0,
                "config": {}
            }

    def update_state(self, grid, towers, overlay_items, level, money, lives, config):
        """Aktualizuje stan gry."""
        self.state = {
            "grid": grid,
            "towers": towers,
            "overlay_items": overlay_items,
            "level": level,
            "money": money,
            "lives": lives,
            "config": config
        }

        self.save_to_json("game_state1.json")
        self.save_to_xml("game_state1.xml")
        # self.save_to_mongodb("game_db", "game_history")

    def save_to_json(self, filepath):
        """Zapisuje stan gry do pliku JSON."""
        with open(filepath, 'w') as file:
            json.dump(self.state, file, indent=4)

    def save_to_xml(self, filepath):
        """Zapisuje stan gry do pliku XML."""
        root = ET.Element("GameState")
        for key, value in self.state.items():
            if isinstance(value, list):
                parent = ET.SubElement(root, key)
                for item in value:
                    if isinstance(item, tuple):  # Obsługa tuple w liście
                        item_element = ET.SubElement(parent, "Item")
                        item_element.set("x", str(item[0]))
                        item_element.set("y", str(item[1]))
                    elif isinstance(item, dict):  # Obsługa słowników w liście
                        item_element = ET.SubElement(parent, "Item")
                        for sub_key, sub_value in item.items():
                            if sub_key == "position" and isinstance(sub_value, dict):  # Obsługa pozycji jako słownika
                                position_element = ET.SubElement(item_element, sub_key)
                                position_element.set("x", str(sub_value["x"]))
                                position_element.set("y", str(sub_value["y"]))
                            else:
                                ET.SubElement(item_element, sub_key).text = str(sub_value)
                    else:
                        ET.SubElement(parent, "Item").text = str(item)
            elif isinstance(value, dict):  # Obsługa konfiguracji jako słownika
                parent = ET.SubElement(root, key)
                for sub_key, sub_value in value.items():
                    ET.SubElement(parent, sub_key).text = str(sub_value)
            elif value is not None:  # Obsługa innych typów danych
                ET.SubElement(root, key).text = str(value)
        tree = ET.ElementTree(root)
        tree.write(filepath, encoding="utf-8", xml_declaration=True)

    def save_to_mongodb(self, db_name, collection_name):
        """Zapisuje stan gry do bazy MongoDB."""
        try:
            client = MongoClient("mongodb://localhost:27017/")
            db = client[db_name]
            collection = db[collection_name]
            collection.insert_one(self.state)
            print("Stan gry zapisany w MongoDB.")
        except Exception as e:
            print(f"Błąd podczas zapisu do MongoDB: {e}")

    def load_from_json(self, filepath):
        """Ładuje stan gry z pliku JSON."""
        with open(filepath, 'r') as file:
            self.state = json.load(file)

    def load_from_xml(self, filepath):
        """Ładuje stan gry z pliku XML."""
        tree = ET.parse(filepath)
        root = tree.getroot()
        self.state = {}
        for child in root:
            if len(child) > 0:  # Jeśli element ma dzieci (np. lista)
                if child.tag == "grid":  # Odczyt pozycji z listy
                    self.state[child.tag] = [
                        (int(item.get("x")), int(item.get("y"))) for item in child
                    ]
                elif child.tag == "towers":  # Odczyt wież
                    self.state[child.tag] = []
                    for item in child:
                        tower_data = {}
                        for sub in item:
                            if sub.tag == "position":
                                tower_data[sub.tag] = {
                                    "x": float(sub.get("x")),
                                    "y": float(sub.get("y"))
                                }
                            else:
                                tower_data[sub.tag] = sub.text
                        self.state[child.tag].append(tower_data)
                elif child.tag == "overlay_items":  # Odczyt elementów overlay
                    self.state[child.tag] = []
                    for item in child:
                        overlay_data = {}
                        for sub in item:
                            if sub.tag == "position":
                                overlay_data[sub.tag] = {
                                    "x": int(sub.get("x")),
                                    "y": int(sub.get("y"))
                                }
                            else:
                                overlay_data[sub.tag] = sub.text
                        self.state[child.tag].append(overlay_data)
                elif child.tag == "config":  # Odczyt konfiguracji jako słownika
                    self.state[child.tag] = {sub.tag: self._convert_value(sub.text) for sub in child}
                else:  # Odczyt innych list
                    self.state[child.tag] = [
                        {sub.tag: sub.text for sub in item} for item in child
                    ]
            else:
                self.state[child.tag] = self._convert_value(child.text)

    def _convert_value(self, value):
        """Konwertuje wartość tekstową na odpowiedni typ (int, float, bool lub str)."""
        if value is None:
            return None
        if value.lower() in ("true", "false"):
            return value.lower() == "true"
        try:
            if "." in value:
                return float(value)
            return int(value)
        except ValueError:
            return value

    def load_from_mongodb(self, db_name, collection_name):
        """Ładuje stan gry z bazy MongoDB."""
        client = MongoClient("mongodb://localhost:27017/")
        db = client[db_name]
        collection = db[collection_name]
        self.state = collection.find_one({}, {"_id": 0})  # Pobiera pierwszy dokument bez pola `_id`

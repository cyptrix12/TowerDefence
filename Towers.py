from GameUnit import GameUnit

import assets_rc

class AnimatedTower(GameUnit):
    def __init__(self, x, y):
        super().__init__(
            x, y,
            sprite_path=":/assets/Towers/Castle/spr_castle_blue.png",
            frame_count=4,
            frame_duration=200
        )
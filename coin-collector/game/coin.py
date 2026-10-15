"""
Coin: a static collectible circle. Drawn as a circle, hit-tested as a
bounding square around it.

Three coin types (Task 2): bronze, silver, gold - each with its own
value and color.
"""

import pygame

# name: (value, color, spawn weight)  -> gold is rarest
COIN_TYPES = {
    "bronze": {"value": 1, "color": (205, 127, 50),  "weight": 60},
    "silver": {"value": 3, "color": (192, 192, 200), "weight": 28},
    "gold":   {"value": 5, "color": (255, 215, 0),   "weight": 12},
}


class Coin:
    def __init__(self, x, y, radius=12, kind="bronze"):
        self.x = x
        self.y = y
        self.radius = radius
        self.kind = kind
        self.value = COIN_TYPES[kind]["value"]
        self.color = COIN_TYPES[kind]["color"]

    def get_rect(self):
        return pygame.Rect(
            int(self.x - self.radius), int(self.y - self.radius),
            self.radius * 2, self.radius * 2,
        )

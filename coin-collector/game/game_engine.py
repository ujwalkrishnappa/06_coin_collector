"""
GameEngine: owns the player, coins, obstacles, lives and the round timer.

Task 1: collected coins are removed (and respawned) so each scores once.
Task 2: three coin types (bronze/silver/gold) with different values.
Task 3: bouncing obstacles; touching one costs a life, followed by a
        short invulnerability window so one touch = one life.
Task 4: 30-second round; ends on time-out or 0 lives; press R to restart.
"""

import random
import pygame

from game.player import Player
from game.coin import Coin, COIN_TYPES
from game.obstacle import Obstacle
from game.collection import check_collection, check_obstacle_hit
from game.renderer import WIDTH, HEIGHT

NUM_COINS = 6
NUM_OBSTACLES = 3
START_LIVES = 3
ROUND_SECONDS = 30
INVULN_MS = 1200          # grace period after being hit
SAFE_DISTANCE = 120       # spawn objects at least this far from the player


class GameEngine:
    def __init__(self):
        self.restart()

    # ---------- setup / reset ----------
    def restart(self):
        self.player = Player(x=WIDTH / 2, y=HEIGHT / 2)
        self.score = 0
        self.lives = START_LIVES
        self.game_over = False
        self.end_reason = ""
        self.round_start = pygame.time.get_ticks()
        self.time_left = float(ROUND_SECONDS)
        self.invuln_until = 0
        self.obstacles = [self._random_obstacle() for _ in range(NUM_OBSTACLES)]
        self.coins = [self._random_coin() for _ in range(NUM_COINS)]

    def _far_from_player(self, x, y):
        return abs(x - self.player.x) > SAFE_DISTANCE or abs(y - self.player.y) > SAFE_DISTANCE

    def _random_coin(self):
        kinds = list(COIN_TYPES)
        weights = [COIN_TYPES[k]["weight"] for k in kinds]
        kind = random.choices(kinds, weights=weights)[0]
        x = random.randint(30, WIDTH - 30)
        y = random.randint(30, HEIGHT - 30)
        return Coin(x=x, y=y, radius=12, kind=kind)

    def _random_obstacle(self):
        size = 32
        while True:
            x = random.randint(size, WIDTH - size)
            y = random.randint(size, HEIGHT - size)
            if self._far_from_player(x, y):
                break
        vx = random.choice([-1, 1]) * random.randint(2, 4)
        vy = random.choice([-1, 1]) * random.randint(2, 4)
        return Obstacle(x, y, vx, vy, size)

    # ---------- input ----------
    def handle_event(self, event):
        if event.type == pygame.KEYDOWN and event.key == pygame.K_r and self.game_over:
            self.restart()

    def handle_input(self, keys_pressed):
        if self.game_over:
            return
        dx = dy = 0
        if keys_pressed[pygame.K_UP]:
            dy -= self.player.speed
        if keys_pressed[pygame.K_DOWN]:
            dy += self.player.speed
        if keys_pressed[pygame.K_LEFT]:
            dx -= self.player.speed
        if keys_pressed[pygame.K_RIGHT]:
            dx += self.player.speed
        self.player.move(dx, dy, WIDTH, HEIGHT)

    # ---------- per-frame update ----------
    def update(self):
        if self.game_over:
            return

        now = pygame.time.get_ticks()

        # Timer (Task 4)
        elapsed = (now - self.round_start) / 1000.0
        self.time_left = max(0.0, ROUND_SECONDS - elapsed)
        if self.time_left <= 0:
            self._end_round("Time's up!")
            return

        # Coins (Task 1 + 2): score once, remove, respawn a new one
        for coin in check_collection(self.player, self.coins):
            self.score += coin.value
            self.coins.remove(coin)
            self.coins.append(self._random_coin())

        # Obstacles (Task 3)
        for obstacle in self.obstacles:
            obstacle.update(WIDTH, HEIGHT)
        if now >= self.invuln_until and check_obstacle_hit(self.player, self.obstacles):
            self.lives -= 1
            self.invuln_until = now + INVULN_MS
            if self.lives <= 0:
                self._end_round("Out of lives!")

    def _end_round(self, reason):
        self.game_over = True
        self.end_reason = reason

    # ---------- drawing ----------
    def draw(self, surface, font):
        from game import renderer
        now = pygame.time.get_ticks()
        invulnerable = (not self.game_over) and now < self.invuln_until
        renderer.draw_scene(surface, self.player, self.coins,
                            self.obstacles, blink=invulnerable and (now // 100) % 2 == 0)
        renderer.draw_hud(surface, font, self.score, self.lives, self.time_left)
        if self.game_over:
            renderer.draw_game_over(surface, font, self.score, self.end_reason)

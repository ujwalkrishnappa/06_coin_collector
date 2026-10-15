"""
renderer: all pygame drawing lives here, kept separate from game logic.
"""

import pygame

WIDTH, HEIGHT = 700, 500
WINDOW_SIZE = (WIDTH, HEIGHT)

COLOR_BG = (35, 45, 35)
COLOR_PLAYER = (80, 180, 255)
COLOR_OBSTACLE = (220, 60, 60)
COLOR_TEXT = (255, 255, 255)
COLOR_BANNER = (255, 220, 80)


def draw_scene(surface, player, coins, obstacles=(), blink=False):
    surface.fill(COLOR_BG)
    for coin in coins:
        pygame.draw.circle(surface, coin.color, (int(coin.x), int(coin.y)), coin.radius)
        pygame.draw.circle(surface, (0, 0, 0), (int(coin.x), int(coin.y)), coin.radius, 2)
    for obstacle in obstacles:
        pygame.draw.rect(surface, COLOR_OBSTACLE, obstacle.get_rect())
    if not blink:  # player flickers while invulnerable
        pygame.draw.rect(surface, COLOR_PLAYER, player.get_rect(), border_radius=4)


def draw_text(surface, font, text, pos, color=COLOR_TEXT):
    surface.blit(font.render(text, True, color), pos)


def draw_hud(surface, font, score, lives, time_left):
    draw_text(surface, font, f"Score: {score}", (10, 10))
    draw_text(surface, font, f"Lives: {lives}", (10, 38))
    timer_color = (255, 90, 90) if time_left <= 5 else COLOR_TEXT
    text = f"Time: {int(time_left) + (1 if time_left % 1 else 0)}"
    surf = font.render(text, True, timer_color)
    surface.blit(surf, (surface.get_width() - surf.get_width() - 10, 10))


def draw_banner(surface, font, text, dy=0):
    surf = font.render(text, True, COLOR_BANNER)
    rect = surf.get_rect(center=(surface.get_width() // 2,
                                 surface.get_height() // 2 + dy))
    surface.blit(surf, rect)


def draw_game_over(surface, font, score, reason):
    overlay = pygame.Surface(surface.get_size(), pygame.SRCALPHA)
    overlay.fill((0, 0, 0, 160))
    surface.blit(overlay, (0, 0))
    draw_banner(surface, font, "GAME OVER - " + reason, -40)
    draw_banner(surface, font, f"Final Score: {score}", 0)
    draw_banner(surface, font, "Press R to play again", 40)

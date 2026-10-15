"""
collection: figures out which coins / obstacles the player touches.
"""


def check_collection(player, coins):
    """
    Returns the list of coins the player is currently overlapping.
    (The engine removes each one right after scoring it.)
    """
    player_rect = player.get_rect()
    return [coin for coin in coins if player_rect.colliderect(coin.get_rect())]


def check_obstacle_hit(player, obstacles):
    """Returns True if the player overlaps any obstacle."""
    player_rect = player.get_rect()
    return any(player_rect.colliderect(o.get_rect()) for o in obstacles)

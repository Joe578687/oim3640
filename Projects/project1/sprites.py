import random
from constants import (
    SCREEN_WIDTH,
    SCREEN_HEIGHT,
    PLAYER_SPEED,
    BULLET_SPEED,
    ENEMY_SPEED,
    BOSS_SPEED,
    PLAYER_CHAR,
    BULLET_CHAR,
    ENEMY_CHAR,
    BOSS_CHAR,
    GAME_TOP,
    GAME_BOTTOM,
)


class Player:
    def __init__(self):
        self.x = SCREEN_WIDTH // 2
        self.y = GAME_BOTTOM
        self.health = 3
        self.char = PLAYER_CHAR

    def move_left(self):
        if self.x > 1:
            self.x -= PLAYER_SPEED

    def move_right(self):
        if self.x < SCREEN_WIDTH - 2:
            self.x += PLAYER_SPEED

    def shoot(self):
        return Bullet(self.x, self.y - 1)

    def take_damage(self):
        self.health -= 1

    def is_alive(self):
        return self.health > 0


class Enemy:
    def __init__(self):
        self.x = random.randint(1, SCREEN_WIDTH - 2)
        self.y = GAME_TOP
        self.speed = ENEMY_SPEED
        self.char = ENEMY_CHAR
        self.alive = True

    def update(self):
        self.y += self.speed
        if self.y > GAME_BOTTOM:
            self.alive = False

    def is_alive(self):
        return self.alive


class Boss:
    def __init__(self):
        self.x = SCREEN_WIDTH // 2
        self.y = GAME_TOP + 2
        self.speed = BOSS_SPEED
        self.char = BOSS_CHAR
        self.alive = True

    def update(self):
        self.y += self.speed
        if self.y > GAME_BOTTOM:
            self.alive = False

    def is_alive(self):
        return self.alive


class Bullet:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.speed = BULLET_SPEED
        self.char = BULLET_CHAR
        self.alive = True

    def update(self):
        self.y -= self.speed
        if self.y < GAME_TOP:
            self.alive = False

    def is_alive(self):
        return self.alive

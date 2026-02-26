import os
import time
import threading
from constants import (
    SCREEN_WIDTH,
    SCREEN_HEIGHT,
    ENEMY_SPAWN_INTERVAL,
    ENEMY_POINTS,
    BOSS_POINTS,
    BOSS_WAVE_INTERVAL,
    GAME_TOP,
    GAME_BOTTOM,
)
from sprites import Player, Enemy, Boss, Bullet


class Game:
    def __init__(self):
        self.player = Player()
        self.enemies = []
        self.bosses = []
        self.bullets = []
        
        self.score = 0
        self.running = True
        self.game_over = False
        self.spawn_timer = 0
        self.wave = 1
        
        self.keys_pressed = set()
        self.listen_thread = None

    def handle_input(self):
        """Listen for keyboard input in background"""
        try:
            import keyboard
            
            def listener():
                while self.running:
                    if keyboard.is_pressed('left'):
                        self.player.move_left()
                    if keyboard.is_pressed('right'):
                        self.player.move_right()
                    if keyboard.is_pressed('space'):
                        bullet = self.player.shoot()
                        self.bullets.append(bullet)
                        self.keys_pressed.discard('space')  # Prevent rapid fire
                    if keyboard.is_pressed('r') and self.game_over:
                        self.reset_game()
                    time.sleep(0.05)
            
            self.listen_thread = threading.Thread(target=listener, daemon=True)
            self.listen_thread.start()
        except ImportError:
            print("Install keyboard library: pip install keyboard")
            self.running = False

    def update(self):
        if self.game_over:
            return

        # Update bullets
        for bullet in self.bullets[:]:
            bullet.update()
            if not bullet.is_alive():
                self.bullets.remove(bullet)

        # Update enemies
        for enemy in self.enemies[:]:
            enemy.update()
            if not enemy.is_alive():
                self.enemies.remove(enemy)

        # Update bosses
        for boss in self.bosses[:]:
            boss.update()
            if not boss.is_alive():
                self.bosses.remove(boss)

        # Check bullet-enemy collisions
        for bullet in self.bullets[:]:
            for enemy in self.enemies[:]:
                if bullet.x == enemy.x and bullet.y == enemy.y:
                    self.bullets.remove(bullet)
                    self.enemies.remove(enemy)
                    self.score += ENEMY_POINTS
                    break

        # Check bullet-boss collisions
        for bullet in self.bullets[:]:
            for boss in self.bosses[:]:
                if bullet.x == boss.x and bullet.y == boss.y:
                    self.bullets.remove(bullet)
                    self.bosses.remove(boss)
                    self.score += BOSS_POINTS
                    self.wave += 1
                    break

        # Check enemy-player collisions
        for enemy in self.enemies[:]:
            if enemy.x == self.player.x and enemy.y == self.player.y:
                self.player.take_damage()
                self.enemies.remove(enemy)
                if not self.player.is_alive():
                    self.game_over = True

        # Check boss-player collisions
        for boss in self.bosses[:]:
            if boss.x == self.player.x and boss.y == self.player.y:
                self.player.take_damage()
                self.bosses.remove(boss)
                if not self.player.is_alive():
                    self.game_over = True

        # Spawn enemies
        self.spawn_timer += 1
        if self.spawn_timer > ENEMY_SPAWN_INTERVAL:
            if self.wave % BOSS_WAVE_INTERVAL == 0 and len(self.bosses) == 0:
                self.bosses.append(Boss())
            else:
                self.enemies.append(Enemy())
            self.spawn_timer = 0

    def draw(self):
        """Render game to terminal"""
        # Clear screen
        os.system('cls' if os.name == 'nt' else 'clear')

        # Create game grid
        grid = []
        for y in range(SCREEN_HEIGHT):
            row = [' '] * SCREEN_WIDTH
            grid.append(row)

        # Draw borders
        for y in range(SCREEN_HEIGHT):
            grid[y][0] = '|'
            grid[y][SCREEN_WIDTH - 1] = '|'

        # Draw top and bottom borders
        for x in range(SCREEN_WIDTH):
            if y == 0 or y == SCREEN_HEIGHT - 1:
                grid[0][x] = '-'
                grid[SCREEN_HEIGHT - 1][x] = '-'

        # Draw player
        if 0 <= self.player.y < SCREEN_HEIGHT and 0 <= self.player.x < SCREEN_WIDTH:
            grid[self.player.y][self.player.x] = self.player.char

        # Draw enemies
        for enemy in self.enemies:
            if 0 <= enemy.y < SCREEN_HEIGHT and 0 <= enemy.x < SCREEN_WIDTH:
                grid[enemy.y][enemy.x] = enemy.char

        # Draw bosses
        for boss in self.bosses:
            if 0 <= boss.y < SCREEN_HEIGHT and 0 <= boss.x < SCREEN_WIDTH:
                grid[boss.y][boss.x] = boss.char

        # Draw bullets
        for bullet in self.bullets:
            if 0 <= bullet.y < SCREEN_HEIGHT and 0 <= bullet.x < SCREEN_WIDTH:
                grid[bullet.y][bullet.x] = bullet.char

        # Print grid
        for row in grid:
            print(''.join(row))

        # Print HUD
        print(f"Score: {self.score} | Health: {self.player.health} | Wave: {self.wave}")

        # Print game over screen
        if self.game_over:
            print("\n" + "="*40)
            print("GAME OVER")
            print(f"Final Score: {self.score}")
            print("Press R to Restart or Ctrl+C to Exit")
            print("="*40)

    def reset_game(self):
        """Reset game state"""
        self.player = Player()
        self.enemies = []
        self.bosses = []
        self.bullets = []
        self.score = 0
        self.game_over = False
        self.spawn_timer = 0
        self.wave = 1

    def run(self):
        """Main game loop"""
        print("Starting Space Invaders Terminal Edition...")
        print("Controls: LEFT/RIGHT arrow keys to move, SPACE to shoot")
        print("Press R to restart when game is over")
        time.sleep(2)

        self.handle_input()

        try:
            while self.running:
                self.update()
                self.draw()
                time.sleep(0.05)  # ~20 FPS for terminal
        except KeyboardInterrupt:
            print("\n\nGame Exited!")
        finally:
            self.running = False

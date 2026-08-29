# config.py
import pygame

pygame.init()

SCREEN_WIDTH = 400
SCREEN_HEIGHT = 600
SAVE_FILE = "highscore.json"

COLORS = {
    "CAVE_BG": (32, 28, 38),        
    "ROCK_BASE": (42, 36, 50),      
    "ROCK_MID": (78, 68, 92),       
    "STALACTITE": (140, 125, 160),  
    "CRYSTAL": (0, 255, 190),       
    "GRID_LINE": (45, 38, 55),      
    "LANTERN_GLOW": (255, 200, 60), 
    "BAT_BODY": (90, 65, 115),      
    "BAT_WING": (55, 40, 70),       
    "DRAGON_BODY": (230, 80, 60),   
    "DIAMOND": (30, 230, 250),      
    "TEXT": (240, 240, 245),
    "MAGMA": (255, 70, 0),          # Mới: Màu đá mắc-ma rơi
    "SHIELD_GLOW": (0, 190, 255)    # Mới: Màu khiên năng lượng bảo vệ
}

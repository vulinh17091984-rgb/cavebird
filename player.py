# player.py - ĐỒNG BỘ VẬT LÝ THEO THỜI GIAN THỰC
import pygame
import math
import random
import json
import os
from config import SCREEN_HEIGHT, COLORS, SAVE_FILE
from audio import play_sfx, sound_flap
from particles import particle_sys

class CaveSkinManager:
    def __init__(self):
        self.current_skin = 0
        self.unlocked_dragon = False
        self.dragon_cost = 15
        self.total_diamonds = 0
        self.high_score = 0
        self.load_game_data()

    def buy_dragon_skin(self):
        if not self.unlocked_dragon and self.total_diamonds >= self.dragon_cost:
            self.total_diamonds -= self.dragon_cost
            self.unlocked_dragon = True
            self.current_skin = 1
            self.save_game_data()
            return True
        return False

    def load_game_data(self):
        if os.path.exists(SAVE_FILE):
            try:
                with open(SAVE_FILE, "r") as f:
                    data = json.load(f)
                    self.high_score = data.get("high_score", 0)
                    self.total_diamonds = data.get("total_diamonds", 0)
                    self.unlocked_dragon = data.get("unlocked_dragon", False)
                    self.current_skin = data.get("current_skin", 0)
            except:
                pass

    def save_game_data(self):
        data = {
            "high_score": self.high_score,
            "total_diamonds": self.total_diamonds,
            "unlocked_dragon": self.unlocked_dragon,
            "current_skin": self.current_skin
        }
        try:
            with open(SAVE_FILE, "w") as f:
                json.dump(data, f)
        except:
            pass

skin_shop = CaveSkinManager()

class CavePlayer:
    def __init__(self):
        self.default_x = 80
        self.x = self.default_x
        self.y = SCREEN_HEIGHT // 2
        self.radius = 12
        self.gravity = 13.68          # Trọng lực chuẩn hóa theo giây
        self.velocity = 0
        self.jump_strength = -230.0    # Lực nhảy chuẩn hóa theo giây
        self.anim_timer = 0
        self.skin = skin_shop.current_skin
        self.angle = 0
        self.sprite_surf = pygame.Surface((80, 80), pygame.SRCALPHA).convert_alpha()
        self.has_shield = False 
        self.stumble_timer = 0
        self.is_dead = False
        self.trail_timer = 0

    def trigger_stumble(self):
        if self.is_dead: return
        self.stumble_timer = 35 

    def update_dt(self, is_playing, dt):
        if self.is_dead: return

        if is_playing:
            self.velocity += self.gravity * dt * 60
            self.y += self.velocity * dt
            self.anim_timer += 18.0 * dt
            
            # Khống chế loạng choạng vấp dây theo time thực
            if self.stumble_timer > 0:
                self.stumble_timer -= 60 * dt
                if self.stumble_timer > 28:
                    target_angle = 24.0
                    self.angle += (target_angle - self.angle) * 27.0 * dt
                elif self.stumble_timer > 12:
                    shake_wave = math.sin(self.stumble_timer * 0.6) * (self.stumble_timer * 0.8)
                    self.angle = shake_wave
                else:
                    target_angle = -20.0
                    self.angle += (target_angle - self.angle) * 9.0 * dt
            else:
                target_angle = -(self.velocity / 60) * 3.5
                target_angle = max(-35, min(25, target_angle))
                self.angle += (target_angle - self.angle) * 10.8 * dt
            
            if self.x < self.default_x: self.x += 30.0 * dt
            elif self.x > self.default_x: self.x -= 30.0 * dt
            
            # Khống chế nhịp độ sinh hạt đuôi để mượt điện thoại
            self.trail_timer += 60 * dt
            if self.trail_timer >= 4:
                p_color = COLORS["CRYSTAL"] if self.skin == 1 else COLORS["BAT_BODY"]
                particle_sys.spawn(self.x - 10, self.y, p_color, 1)
                self.trail_timer = 0

    def flap(self):
        if self.is_dead: return
        self.velocity = self.jump_strength
        if self.stumble_timer > 0:
            self.stumble_timer = min(self.stumble_timer, 8)
        play_sfx(sound_flap)

    def draw(self, surface):
        self.sprite_surf.fill((0, 0, 0, 0)) 
        wing_offset = int(math.sin(self.anim_timer) * 14)
        cx, cy = 40, 40
        
        if self.skin == 0:
            pygame.draw.polygon(self.sprite_surf, COLORS["BAT_WING"], [(cx, cy), (cx - 24, cy - 15 + wing_offset), (cx - 12, cy + 5)])
            pygame.draw.polygon(self.sprite_surf, COLORS["BAT_WING"], [(cx, cy), (cx - 24, cy + 15 - wing_offset), (cx - 12, cy - 5)])
            pygame.draw.circle(self.sprite_surf, COLORS["BAT_BODY"], (cx, cy), self.radius + 2)
            pygame.draw.polygon(self.sprite_surf, COLORS["BAT_BODY"], [(cx - 4, cy - 10), (cx - 8, cy - 20), (cx, cy - 12)]) 
            pygame.draw.polygon(self.sprite_surf, COLORS["BAT_BODY"], [(cx + 4, cy - 10), (cx + 8, cy - 20), (cx, cy - 12)]) 
            pygame.draw.circle(self.sprite_surf, (240, 240, 100), (cx + 5, cy - 3), 3)
            pygame.draw.circle(self.sprite_surf, (240, 240, 100), (cx + 5, cy + 3), 3)
        else:
            pygame.draw.polygon(self.sprite_surf, (180, 40, 30), [(cx - 5, cy), (cx - 25, cy - 18 + wing_offset), (cx - 10, cy + 8)])
            pygame.draw.circle(self.sprite_surf, COLORS["DRAGON_BODY"], (cx, cy), self.radius + 2)
            pygame.draw.circle(self.sprite_surf, COLORS["DRAGON_BODY"], (cx + 8, cy - 4), 8) 
            pygame.draw.circle(self.sprite_surf, (255, 255, 255), (cx + 10, cy - 6), 3) 
            pygame.draw.circle(self.sprite_surf, (0, 0, 0), (cx + 11, cy - 6), 1)
            pygame.draw.polygon(self.sprite_surf, (240, 180, 30), [(cx + 14, cy - 2), (cx + 22, cy + 2), (cx + 10, cy + 4)]) 

        rotated_surf = pygame.transform.rotate(self.sprite_surf, self.angle)
        new_rect = rotated_surf.get_rect(center=(int(self.x), int(self.y)))
        surface.blit(rotated_surf, new_rect.topleft)

        if self.has_shield and not self.is_dead:
            t = pygame.time.get_ticks() / 100
            shield_radius = self.radius + 12 + int(math.sin(t) * 2)
            pygame.draw.circle(surface, COLORS["SHIELD_GLOW"], (int(self.x), int(self.y)), shield_radius, 2)

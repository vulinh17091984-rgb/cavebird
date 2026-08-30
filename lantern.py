# lantern.py - ĐÃ ĐỒNG BỘ UPDATE_DT VÀ SỬA LỖI ĐỊNH DANH MẢNG AN TOÀN CHO ANDROID
import pygame
import math
import random
from config import COLORS

# Tạo hàm rỗng câm (Mock) để chặn lỗi import sfx phần cứng khi build APK
def play_sfx(sound_obj): pass
sound_bounce = None
# Mock particle_sys để tránh lỗi vòng lặp nạp thư viện chéo (Circular Import)
class MockParticle:
    def spawn(self, x, y, color, count=1): pass
particle_sys = MockParticle()

class IndependentLantern:
    def __init__(self, x_pos, y_pos):
        self.x = x_pos
        self.y = y_pos  
        self.radius = 14  
        self.speed = 180.0          
        self.pulse_offset = random.uniform(0, 10)
        self.rope_shake = 0 
        self.rope_snagged = False 
        
        self.base_glow_radius = 120
        self.glow_surf = pygame.Surface((self.base_glow_radius * 2, self.base_glow_radius * 2), pygame.SRCALPHA).convert_alpha()
        self.glow_surf.fill((0, 0, 0, 0))
        
        for r in range(self.base_glow_radius, 0, -6):
            factor = 1.0 - (r / self.base_glow_radius)
            alpha = int((factor ** 2.2) * 35) 
            if alpha > 0:
                pygame.draw.circle(self.glow_surf, (*COLORS["LANTERN_GLOW"], alpha), (self.base_glow_radius, self.base_glow_radius), r)

    def update_dt(self, step_speed, dt):
        self.x -= step_speed
        if self.rope_shake > 0:
            self.rope_shake *= math.pow(0.01, dt)
            if self.rope_shake < 0.2: self.rope_shake = 0

    def check_player_bounce(self, player):
        center_y = self.y + 16
        if math.hypot(self.x - player.x, center_y - player.y) < player.radius + self.radius:
            play_sfx(sound_bounce)
            particle_sys.spawn(self.x, center_y, COLORS["LANTERN_GLOW"], 12)
            player.x -= 22 
            player.velocity = -3.5 * 60 if player.y < center_y else 3.5 * 60
            return True
        return False
    
    def check_rope_snag(self, player):
        if self.rope_snagged: return False
        if 0 <= player.y <= self.y:
            if abs(player.x - self.x) < (player.radius + 2):
                self.rope_snagged = True 
                self.rope_shake = random.uniform(8, 14)
                player.x += 12 
                player.velocity = max(player.velocity + 90.0, 120.0)
                particle_sys.spawn(player.x, player.y, (140, 125, 160), 4)
                return True
        return False

    def draw(self, surface):
        t = pygame.time.get_ticks() / 40
        shake_offset = math.sin(t) * self.rope_shake if self.rope_shake > 0 else 0
        current_lantern_x = self.x + shake_offset
        pygame.draw.line(surface, (45, 40, 52), (int(self.x), 0), (int(current_lantern_x), int(self.y)), 2)
        
        pulse = math.sin(pygame.time.get_ticks() / 140 + self.pulse_offset) * 5
        scaled_dim = int((self.base_glow_radius + pulse) * 2)
        if scaled_dim > 10:
            scaled_glow = pygame.transform.scale(self.glow_surf, (scaled_dim, scaled_dim))
            surface.blit(scaled_glow, (int(current_lantern_x - scaled_dim//2), int(self.y + 16 - scaled_dim//2)))
        
        dui_w, dui_h = 10, 6
        pygame.draw.rect(surface, (120, 115, 130), (int(current_lantern_x - dui_w//2), int(self.y), dui_w, 2), border_radius=1)
        pygame.draw.rect(surface, (95, 90, 105), (int(current_lantern_x - (dui_w-2)//2), int(self.y + 2), dui_w - 2, 2))
        pygame.draw.rect(surface, (120, 115, 130), (int(current_lantern_x - dui_w//2), int(self.y + 4), dui_w, 2), border_radius=1)
        pygame.draw.rect(surface, (35, 30, 42), (int(current_lantern_x - 4), int(self.y + 6), 8, 3))
        
        center_y = self.y + 16
        glass_surf = pygame.Surface((self.radius * 2 + 4, self.radius * 2 + 4), pygame.SRCALPHA)
        glass_surf.fill((0, 0, 0, 0)) 
        pygame.draw.circle(glass_surf, (255, 230, 150, 20), (self.radius + 2, self.radius + 2), self.radius)
        pygame.draw.circle(glass_surf, (245, 245, 255, 150), (self.radius + 2, self.radius + 2), self.radius, 1)
        surface.blit(glass_surf, (int(current_lantern_x - self.radius - 2), int(center_y - self.radius - 2)))
        
        pygame.draw.line(surface, (150, 140, 160), (int(current_lantern_x - 2.5), int(self.y + 9)), (int(current_lantern_x - 2.5), int(center_y + 1)), 1)
        pygame.draw.line(surface, (150, 140, 160), (int(current_lantern_x + 2.5), int(self.y + 9)), (int(current_lantern_x + 2.5), int(center_y + 1)), 1)
        pygame.draw.circle(surface, (255, 255, 210), (int(current_lantern_x), int(center_y - 3)), 2)

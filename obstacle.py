# obstacle.py - MÃ NGUỒN HOÀN CHỈNH ĐÃ SỬA LỖI MẢNG THAM SỐ RANDOM
import pygame
import math
import random
from config import SCREEN_HEIGHT, COLORS
from particles import particle_sys

class StalactiteObstacle:
    def __init__(self, x_pos):
        self.x = x_pos
        self.gap = 165              # Khoảng trống an toàn chuẩn 165 pixel
        self.speed = 180.0          # Vận tốc pixel chạy trong 1 giây thực tế (180px/s)
        self.passed = False         

       
        # ĐÃ VÁ LỖI CÚ PHÁP: Điền đầy đủ mảng chỉ mục lựa chọn [0, 1, 2] cho hang đá
        self.spawn_style = random.choices([0, 1, 2], weights=[0.2, 0.2, 0.6])[0]


        self.top_width = random.randint(70, 145)  
        self.bot_width = random.randint(70, 145)  
        
        # Khoảng lệch trục X giữa khối trên và khối dưới
        self.bot_offset_x = random.randint(-95, 95)

        # Khống chế không gian đường đi, sửa triệt để lỗi đường đi bé xíu
        if self.spawn_style == 0:   # CHỈ CÓ KHỐI TRÊN
            self.top_height = random.randint(150, SCREEN_HEIGHT - 220)
            self.bottom_y = SCREEN_HEIGHT + 500  
        elif self.spawn_style == 1: # CHỈ CÓ KHỐI DƯỚI
            self.top_height = -500               
            self.bottom_y = random.randint(220, SCREEN_HEIGHT - 150)
        else:                       # CÓ CẢ HAI KHỐI LỆCH NHAU
            min_height = 80
            max_height = SCREEN_HEIGHT - self.gap - 100
            self.top_height = random.randint(min_height, max_height)
            self.bottom_y = self.top_height + self.gap

        # Số lượng đầu nhánh dựa theo độ rộng khối đá
        self.top_head_count = random.randint(2, 4) if self.top_width < 100 else random.randint(3, 5)
        self.bot_head_count = random.randint(2, 4) if self.bot_width < 100 else random.randint(3, 5)

        self.top_block_style = random.randint(0, 1)
        self.bot_block_style = random.randint(0, 1)

        # --- SINH VÁCH TRẦN HANG (KHÔNG LÀM ĐÈ LỐI ĐI) ---
        self.top_outline = []
        if self.spawn_style in (0, 2): 
            self.top_outline.append((self.x, 0))
            seg_w_top = self.top_width / self.top_head_count
            for i in range(self.top_head_count):
                hx = self.x + i * seg_w_top + seg_w_top / 2
                hy = self.top_height if i == self.top_head_count // 2 else random.randint(int(self.top_height * 0.55), int(self.top_height * 0.80))
                r_w = seg_w_top * 0.38
                self.top_outline.append((hx - r_w * 1.4 - random.uniform(0.5, 1.5), hy * 0.35))
                self.top_outline.append((hx - r_w * 1.15 + random.uniform(0.2, 1.0), hy * 0.6))
                self.top_outline.append((hx - r_w - random.uniform(0.5, 1.2), hy * 0.8))
                if self.top_block_style == 0: 
                    self.top_outline.append((hx - r_w * 0.5, hy - 2))
                    self.top_outline.append((hx, hy))
                    self.top_outline.append((hx + r_w * 0.5, hy - 2))
                else: 
                    self.top_outline.append((hx, hy))
                self.top_outline.append((hx + r_w + random.uniform(0.5, 1.2), hy * 0.8))
                self.top_outline.append((hx + r_w * 1.15 - random.uniform(0.2, 1.0), hy * 0.6))
                self.top_outline.append((hx + r_w * 1.4 + random.uniform(0.5, 1.5), hy * 0.35))
            self.top_outline.append((self.x + self.top_width, 0))

        # --- SINH VÁCH ĐÁY HANG ---
        self.bot_outline = []
        if self.spawn_style in (1, 2): 
            bot_start_x = self.x + (self.bot_offset_x if self.spawn_style == 2 else 0)
            self.bot_outline.append((bot_start_x, SCREEN_HEIGHT))
            seg_w_bot = self.bot_width / self.bot_head_count
            bot_h = SCREEN_HEIGHT - self.bottom_y
            for i in range(self.bot_head_count):
                hx = bot_start_x + i * seg_w_bot + seg_w_bot / 2
                hy = self.bottom_y if i == self.bot_head_count // 2 else SCREEN_HEIGHT - random.randint(int(bot_h * 0.55), int(bot_h * 0.80))
                r_w = seg_w_bot * 0.38
                self.bot_outline.append((hx - r_w * 1.4 - random.uniform(0.5, 1.5), SCREEN_HEIGHT - (SCREEN_HEIGHT - hy) * 0.35))
                self.bot_outline.append((hx - r_w * 1.15 + random.uniform(0.2, 1.0), SCREEN_HEIGHT - (SCREEN_HEIGHT - hy) * 0.6))
                self.bot_outline.append((hx - r_w - random.uniform(0.5, 1.2), SCREEN_HEIGHT - (SCREEN_HEIGHT - hy) * 0.8))
                if self.bot_block_style == 0: 
                    self.bot_outline.append((hx - r_w * 0.5, hy + 2))
                    self.bot_outline.append((hx, hy))
                    self.bot_outline.append((hx + r_w * 0.5, hy + 2))
                else: 
                    self.bot_outline.append((hx, hy))
                self.bot_outline.append((hx + r_w + random.uniform(0.5, 1.2), SCREEN_HEIGHT - (SCREEN_HEIGHT - hy) * 0.8))
                self.bot_outline.append((hx + r_w * 1.15 - random.uniform(0.2, 1.0), SCREEN_HEIGHT - (SCREEN_HEIGHT - hy) * 0.6))
                self.bot_outline.append((hx + r_w * 1.4 + random.uniform(0.5, 1.5), SCREEN_HEIGHT - (SCREEN_HEIGHT - hy) * 0.35))
            self.bot_outline.append((bot_start_x + self.bot_width, SCREEN_HEIGHT))

        self.top_crystals = []
        if len(self.top_outline) > 0: self._generate_static_crystals(self.top_outline, self.top_crystals, True, self.top_width)
        self.bot_crystals = []
        if len(self.bot_outline) > 0: self._generate_static_crystals(self.bot_outline, self.bot_crystals, False, self.bot_width)

        self.diamond_collected = False
        self.has_diamond = random.random() < 0.55
        self.diamond_x = self.x + self.top_width // 2 if self.spawn_style in (0, 2) else self.x + self.bot_width // 2
        self.diamond_y = self.top_height + 50 if self.spawn_style == 0 else (self.bottom_y - 50 if self.spawn_style == 1 else self.top_height + (self.gap // 2))

    def _generate_static_crystals(self, outline_pts, target_list, is_top, current_width):
        cx_local = current_width / 2
        base_x = self.x if is_top else (self.x + (self.bot_offset_x if self.spawn_style == 2 else 0))
        for idx, (px, py) in enumerate(outline_pts[2:-2]):
            rel_px = px - base_x
            if (idx + int(self.x)) % 3 == 0:
                f_rel_x = rel_px + (cx_local - rel_px) * 0.35
                f_y = py * random.uniform(0.65, 0.85) if is_top else SCREEN_HEIGHT - (SCREEN_HEIGHT - py) * random.uniform(0.65, 0.85)
                if 12 < f_rel_x < (current_width - 12):
                    target_list.append((f_rel_x, f_y, (f_rel_x * 0.04 + f_y * 0.04), COLORS["CRYSTAL"] if random.random() < 0.60 else (240, 245, 255)))

    def update_dt(self, step_speed):
        self.x -= step_speed
        self.diamond_x -= step_speed
        if len(self.top_outline) > 0: self.top_outline = [(px - step_speed, py) for px, py in self.top_outline]
        if len(self.bot_outline) > 0: self.bot_outline = [(px - step_speed, py) for px, py in self.bot_outline]

    def _draw_seamless_rock(self, surface, outline_pts, crystal_list, current_width, is_top):
        if len(outline_pts) < 3: return
        pygame.draw.polygon(surface, COLORS["ROCK_BASE"], outline_pts)
        mid_pts = []
        base_x = self.x if is_top else (self.x + (self.bot_offset_x if self.spawn_style == 2 else 0))
        cx = base_x + current_width / 2
        for px, py in outline_pts:
            if py == 0 or py == SCREEN_HEIGHT: mid_pts.append((px, py))
            else: mid_pts.append((px + 4 if px < cx else px - 4, py))
        if len(mid_pts) > 2: pygame.draw.polygon(surface, COLORS["ROCK_MID"], mid_pts)

        high_pts = []
        for px, py in outline_pts:
            if py == 0 or py == SCREEN_HEIGHT: high_pts.append((px, py))
            else: high_pts.append((px + 8 if px < cx else px - 8, py))
        if len(high_pts) > 2: pygame.draw.polygon(surface, COLORS["STALACTITE"], high_pts)

        t = pygame.time.get_ticks()
        for rel_x, cy, wave_offset, c_color in crystal_list:
            actual_x = base_x + rel_x
            pulse = math.sin(t / 950 + wave_offset)
            crystal_alpha = int(95 + pulse * 45)
            if crystal_alpha > 0:
                glow_r = 3 + int(abs(pulse) * 1.5)
                glow_surf = pygame.Surface((glow_r * 2, glow_r * 2), pygame.SRCALPHA)
                pygame.draw.circle(glow_surf, (*c_color, crystal_alpha), (glow_r, glow_r), glow_r)
                surface.blit(glow_surf, (int(actual_x - glow_r), int(cy - glow_r)))

    def draw(self, surface):
        if self.spawn_style in (0, 2): self._draw_seamless_rock(surface, self.top_outline, self.top_crystals, self.top_width, True)
        if self.spawn_style in (1, 2): self._draw_seamless_rock(surface, self.bot_outline, self.bot_crystals, self.bot_width, False)
        if self.has_diamond and not self.diamond_collected:
            t = pygame.time.get_ticks() / 200
            pulse_y = self.diamond_y + math.sin(t) * 5
            d_pts = [(self.diamond_x, pulse_y - 8), (self.diamond_x + 6, pulse_y), (self.diamond_x, pulse_y + 8), (self.diamond_x - 6, pulse_y)]
            pygame.draw.polygon(surface, COLORS["DIAMOND"], d_pts)

    def _dist_to_segment(self, cx, cy, p1, p2):
        x1, y1 = p1
        x2, y2 = p2
        dx, dy = x2 - x1, y2 - y1
        if dx == 0 and dy == 0: return math.hypot(cx - x1, cy - y1)
        t = max(0.0, min(1.0, ((cx - x1) * dx + (cy - y1) * dy) / (dx * dx + dy * dy)))
        return math.hypot(cx - (x1 + t * dx), cy - (y1 + t * dy))

    def check_collision_precise(self, px, py, pradius):
        if self.spawn_style == 0: 
            if px + pradius < self.x or px - pradius > self.x + self.top_width: return False
            for i in range(len(self.top_outline) - 1):
                if self._dist_to_segment(px, py, self.top_outline[i], self.top_outline[i+1]) < pradius: return True
        elif self.spawn_style == 1: 
# obstacle.py - PHẦN 2: DRAW PHÂN LỚP ĐÁ VÀ KIỂM TRA VA CHẠM KHÔNG BỊ TRÀN Ô
    def _draw_seamless_rock(self, surface, outline_pts, crystal_list, current_width, is_top):
        if len(outline_pts) < 3: return
        pygame.draw.polygon(surface, COLORS["ROCK_BASE"], outline_pts)
        mid_pts = []
        base_x = self.x if is_top else (self.x + (self.bot_offset_x if self.spawn_style == 2 else 0))
        cx = base_x + current_width / 2
        for px, py in outline_pts:
            if py == 0 or py == SCREEN_HEIGHT: mid_pts.append((px, py))
            else: mid_pts.append((px + 4 if px < cx else px - 4, py))
        if len(mid_pts) > 2: pygame.draw.polygon(surface, COLORS["ROCK_MID"], mid_pts)

        high_pts = []
        for px, py in outline_pts:
            if py == 0 or py == SCREEN_HEIGHT: high_pts.append((px, py))
            else: high_pts.append((px + 8 if px < cx else px - 8, py))
        if len(high_pts) > 2: pygame.draw.polygon(surface, COLORS["STALACTITE"], high_pts)

        t = pygame.time.get_ticks()
        for rel_x, cy, wave_offset, c_color in crystal_list:
            actual_x = base_x + rel_x
            pulse = math.sin(t / 950 + wave_offset)
            crystal_alpha = int(95 + pulse * 45)
            if crystal_alpha > 0:
                glow_r = 3 + int(abs(pulse) * 1.5)
                glow_surf = pygame.Surface((glow_r * 2, glow_r * 2), pygame.SRCALPHA)
                pygame.draw.circle(glow_surf, (*c_color, crystal_alpha), (glow_r, glow_r), glow_r)
                surface.blit(glow_surf, (int(actual_x - glow_r), int(cy - glow_r)))

    def draw(self, surface):
        if self.spawn_style in (0, 2): self._draw_seamless_rock(surface, self.top_outline, self.top_crystals, self.top_width, True)
        if self.spawn_style in (1, 2): self._draw_seamless_rock(surface, self.bot_outline, self.bot_crystals, self.bot_width, False)
        if self.has_diamond and not self.diamond_collected:
            t = pygame.time.get_ticks() / 200
            pulse_y = self.diamond_y + math.sin(t) * 5
            d_pts = [(self.diamond_x, pulse_y - 8), (self.diamond_x + 6, pulse_y), (self.diamond_x, pulse_y + 8), (self.diamond_x - 6, pulse_y)]
            pygame.draw.polygon(surface, COLORS["DIAMOND"], d_pts)

    def _dist_to_segment(self, cx, cy, p1, p2):
        x1, y1 = p1
        x2, y2 = p2
        dx, dy = x2 - x1, y2 - y1
        if dx == 0 and dy == 0: return math.hypot(cx - x1, cy - y1)
        t = max(0.0, min(1.0, ((cx - x1) * dx + (cy - y1) * dy) / (dx * dx + dy * dy)))
        return math.hypot(cx - (x1 + t * dx), cy - (y1 + t * dy))

    def check_collision_precise(self, px, py, pradius):
        # 1. KIỂM TRA VA CHẠM KHỐI TRÊN
        if self.spawn_style == 0: 
            if px + pradius < self.x or px - pradius > self.x + self.top_width: return False
            for i in range(len(self.top_outline) - 1):
                if self._dist_to_segment(px, py, self.top_outline[i], self.top_outline[i+1]) < pradius: return True
        # 2. KIỂM TRA VA CHẠM KHỐI DƯỚI
        elif self.spawn_style == 1: 
            if px + pradius < self.x or px - pradius > self.x + self.bot_width: return False
            for i in range(len(self.bot_outline) - 1):
                if self._dist_to_segment(px, py, self.bot_outline[i], self.bot_outline[i+1]) < pradius: return True
        # 3. KIỂM TRA VA CHẠM CẢ HAI KHỐI LỆCH NHAU
        else: 
            min_bx = min(self.x, self.x + self.bot_offset_x)
            max_bx = max(self.x + self.top_width, self.x + self.bot_offset_x + self.bot_width)
            if px + pradius < min_bx or px - pradius > max_bx: return False
            for i in range(len(self.top_outline) - 1):
                if self._dist_to_segment(px, py, self.top_outline[i], self.top_outline[i+1]) < pradius: return True
            for i in range(len(self.bot_outline) - 1):
                if self._dist_to_segment(px, py, self.bot_outline[i], self.bot_outline[i+1]) < pradius: return True
        return False

    def check_diamond_pickup(self, player_x, player_y, player_radius):
        if self.has_diamond and not self.diamond_collected:
            if math.hypot(self.diamond_x - player_x, self.diamond_y - player_y) < player_radius + 8:
                self.diamond_collected = True
                particle_sys.spawn(self.diamond_x, self.diamond_y, COLORS["DIAMOND"], 12)
                return True
        return False

class FallingMagma:
    def __init__(self):
        self.x = random.randint(140, 380) 
        self.y = 20 
        self.radius = random.randint(6, 10)
        self.speed_y = random.uniform(90.0, 330.0) 
        self.speed_x = random.uniform(-48.0, -12.0)
        self.active = True

    def update_dt(self, dt):
        self.x += self.speed_x * dt
        self.y += self.speed_y * dt
        if random.random() < 15.0 * dt:
            particle_sys.spawn(self.x, self.y, COLORS["MAGMA"], 1)
        if self.y > SCREEN_HEIGHT:
            self.active = False
            particle_sys.spawn(self.x, self.y, COLORS["MAGMA"], 6) 

    def draw(self, surface):
        if not self.active: return
        pygame.draw.circle(surface, COLORS["MAGMA"], (int(self.x), int(self.y)), self.radius)
        pygame.draw.circle(surface, (255, 200, 50), (int(self.x), int(self.y)), self.radius - 3)

    def check_collision(self, player):
        if not self.active: return False
        if math.hypot(self.x - player.x, self.y - player.y) < self.radius + player.radius:
            self.active = False
            return True
        return False

class ShieldPowerUp:
    def __init__(self, x_pos, y_pos):
        self.x = x_pos
        self.y = y_pos
        self.radius = 12
        self.speed = 180.0
        self.collected = False

    def update_dt(self, step_speed):
        self.x -= step_speed

    def draw(self, surface):
        if self.collected: return
        t = pygame.time.get_ticks() / 150
        pulse_r = self.radius + math.sin(t) * 3
        pygame.draw.circle(surface, COLORS["SHIELD_GLOW"], (int(self.x), int(self.y)), int(pulse_r), 2)
        pts = [(self.x, self.y - 6), (self.x + 6, self.y + 4), (self.x - 6, self.y + 4)]
        pygame.draw.polygon(surface, (255, 255, 255), pts)

    def check_pickup(self, player):
        if self.collected: return False
        if math.hypot(self.x - player.x, self.y - player.y) < self.radius + player.radius:
            self.collected = True
            particle_sys.spawn(self.x, self.y, COLORS["SHIELD_GLOW"], 15) 
            return True
        return False

# particles.py - ĐÃ TỐI ƯU OBJECT POOLING CHO TẤT CẢ ĐIỆN THOẠI ANDROID
import pygame
import random

class CaveParticle:
    def __init__(self):
        self.x = 0
        self.y = 0
        self.vx = 0
        self.vy = 0
        self.radius = 0
        self.alpha = 0
        self.fade_speed = 0
        self.color = (0, 0, 0)
        self.active = False 

    def activate(self, x, y, color):
        self.x = x
        self.y = y
        self.vx = random.uniform(-1.5, -0.5)
        self.vy = random.uniform(-0.8, 0.8)
        self.radius = random.randint(2, 4) 
        self.alpha = 255
        self.fade_speed = random.randint(12, 20) 
        self.color = color
        self.active = True

    def update_dt(self, dt):
        if not self.active: return
        # Tính toán chuyển động hạt mượt mà theo giây thực tế
        self.x += self.vx * 60 * dt
        self.y += self.vy * 60 * dt
        self.alpha -= self.fade_speed * 60 * dt
        if self.radius > 0.1:
            self.radius -= 0.08 * 60 * dt
            
        if self.alpha <= 0 or self.radius <= 0:
            self.active = False

    def draw(self, surface):
        if not self.active or self.alpha <= 0: return
        r_int = int(self.radius)
        if r_int <= 0: return
        
        p_surf = pygame.Surface((r_int * 2, r_int * 2), pygame.SRCALPHA)
        pygame.draw.circle(p_surf, (*self.color, int(max(0, min(255, self.alpha)))), (r_int, r_int), r_int)
        surface.blit(p_surf, (int(self.x - r_int), int(self.y - r_int)))

class ParticleManager:
    def __init__(self):
        # Pool sẵn 50 hạt cố định từ đầu game
        self.pool_size = 50
        self.particles = [CaveParticle() for _ in range(self.pool_size)]

    def spawn(self, x, y, color, count=1):
        safe_count = min(count, 8) # Khống chế số lượng nổ hạt vừa phải trên di động
        spawned = 0
        for p in self.particles:
            if not p.active:
                p.activate(x, y, color)
                spawned += 1
                if spawned >= safe_count:
                    break

    def update_dt(self, dt):
        for p in self.particles:
            if p.active:
                p.update_dt(dt)

    def draw(self, surface):
        for p in self.particles:
            if p.active:
                p.draw(surface)

particle_sys = ParticleManager()

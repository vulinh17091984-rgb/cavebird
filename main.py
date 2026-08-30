# main.py - PHẦN 1: KHỞI TẠO HỆ THỐNG & ĐỒ HỌA NỀN ĐỒNG BỘ ĐIỆN THOẠI
import pygame
import random
import sys
import math
import gc # Nhập thư viện dọn rác hệ thống RAM
from config import SCREEN_WIDTH, SCREEN_HEIGHT, COLORS
# --- ĐÃ ÉP TẮT LỆNH QUÉT MIXER ĐỂ ROBOT ĐÓNG GÓI APK THÀNH CÔNG RỰC RỠ ---
def play_sfx(sound_obj): pass
sound_hit = sound_coin = sound_score = sound_bounce = sound_flap = None
from particles import particle_sys
from player import CavePlayer, skin_shop
from lantern import IndependentLantern
from obstacle import StalactiteObstacle, FallingMagma, ShieldPowerUp

pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.RESIZABLE)
display_surf = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Cave Bird: Anh Sang Khe Da")

# --- ĐÃ ÉP ĐƯỜNG DẪN FONT THỰC TẾ ĐỂ CHẠY MƯỢT TRÊN ANDROID ---
font_hud = pygame.font.Font("font.ttf", 24)
font_menu = pygame.font.Font("font.ttf", 16)
font_logo = pygame.font.Font("font.ttf", 38)

STATE_MENU, STATE_PLAYING, STATE_GAMEOVER = 0, 1, 2
game_state = STATE_MENU
clock = pygame.time.Clock()

is_wave_surging = False
wave_surge_timer = 0

def draw_cave_background(surface, is_playing, current_water_level, current_score):
    surface.fill(COLORS["CAVE_BG"])
    global is_wave_surging
    grid_w = 60
    for r in range(0, SCREEN_HEIGHT, grid_w):
        offset = (pygame.time.get_ticks() // 22) % grid_w if is_playing else 0
        for c in range(-offset, SCREEN_WIDTH + grid_w, grid_w):
            pygame.draw.rect(surface, COLORS["GRID_LINE"], (c, r, grid_w, grid_w), 1)
            
    water_y = SCREEN_HEIGHT - current_water_level
    t = pygame.time.get_ticks() / 130
    amplitude_modifier = 28.0 + math.sin(t * 0.5) * 8.0 if is_wave_surging else 6.0 + math.sin(t * 0.2) * 3.0
    global_bobbing = math.cos(t * 1.5) * 16.0 if is_wave_surging else math.cos(t * 0.8) * 3.0
    
    water_poly = []
    # TỐI ƯU: Tăng bước nhảy lên 40 để làm phẳng bớt điểm neo sóng nước, giải phóng CPU di động
    for x in range(0, SCREEN_WIDTH + 10, 40): 
        wave_1 = math.sin(x * 0.014 + t * 0.8)
        wave_2 = math.cos(x * 0.04 - t * 1.3)
        total_wave_noise = (wave_1 * wave_2) * amplitude_modifier
        water_poly.append((x, water_y + total_wave_noise + global_bobbing))
        
    water_poly.append((SCREEN_WIDTH, SCREEN_HEIGHT))
    water_poly.append((0, SCREEN_HEIGHT))
    
    water_surf = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
    pygame.draw.polygon(water_surf, (*COLORS["DIAMOND"], 140), water_poly)
    surface.blit(water_surf, (0, 0))
# main.py - PHẦN 2: QUẢN LÝ THỰC THỂ & XỬ LÝ SỰ KIỆN
player = CavePlayer()
pipes = []
independent_lanterns = []
falling_magmas = []
shield_items = []

score = 0
water_level = 40
magma_spawn_timer = 0
shake_timer = 0
shake_intensity = 0
running = True
gameover_input_lock = 0

def spawn_anchored_lantern(pipe_obj):
    return IndependentLantern(pipe_obj.x + random.randint(15, 35), random.randint(100, 210))

def reset_game():
    global player, pipes, independent_lanterns, falling_magmas, shield_items
    global score, water_level, magma_spawn_timer, game_state, is_wave_surging, wave_surge_timer, gameover_input_lock
    player = CavePlayer()
    first_pipe = StalactiteObstacle(SCREEN_WIDTH + 80)
    max_right_1 = first_pipe.x + (first_pipe.top_width if first_pipe.spawn_style in (0, 2) else first_pipe.bot_offset_x + first_pipe.bot_width)
    second_pipe = StalactiteObstacle(max_right_1 + random.randint(90, 125))
    pipes = [first_pipe, second_pipe]
    independent_lanterns = [spawn_anchored_lantern(first_pipe), spawn_anchored_lantern(second_pipe)]
    falling_magmas.clear()
    shield_items.clear()
    magma_spawn_timer = 0
    score = 0
    water_level = 40
    is_wave_surging = False
    wave_surge_timer = 0
    gameover_input_lock = 0 
    game_state = STATE_PLAYING

def handle_events():
    global running, game_state, gameover_input_lock
    for event in pygame.event.get():
        if event.type == pygame.QUIT: running = False
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            real_w, real_h = screen.get_size()
            scale_ratio = min(real_w / SCREEN_WIDTH, real_h / SCREEN_HEIGHT)
            mx = int((event.pos[0] - (real_w - int(SCREEN_WIDTH * scale_ratio)) // 2) / scale_ratio)
            my = int((event.pos[1] - (real_h - int(SCREEN_HEIGHT * scale_ratio)) // 2) / scale_ratio)
            if game_state == STATE_PLAYING: player.flap()
            elif game_state == STATE_MENU:
                if 20 <= mx <= 180 and 20 <= my <= 55:
                    if not skin_shop.unlocked_dragon: skin_shop.buy_dragon_skin()
                    else:
                        skin_shop.current_skin = 1 if skin_shop.current_skin == 0 else 0
                        skin_shop.save_game_data()
                else: reset_game()
            elif game_state == STATE_GAMEOVER and gameover_input_lock <= 0: reset_game()
        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            if game_state == STATE_PLAYING: player.flap()
            elif game_state == STATE_MENU: reset_game()
            elif game_state == STATE_GAMEOVER and gameover_input_lock <= 0: reset_game()
# main.py - PHẦN 3: LOGIC VÒNG LẶP CHÍNH CHUẨN HOÁ THEO TIME ĐỒNG BỘ
def trigger_game_over():
    global game_state, shake_timer, shake_intensity, score, gameover_input_lock
    player.is_dead = True
    p_body_color = COLORS["DRAGON_BODY"] if player.skin == 1 else COLORS["BAT_BODY"]
    particle_sys.spawn(player.x, player.y, p_body_color, 25)
    particle_sys.spawn(player.x, player.y, COLORS["STALACTITE"], 15)
    play_sfx(sound_hit)
    shake_timer, shake_intensity = 25, 8 
    if score > skin_shop.high_score: skin_shop.high_score = score
    skin_shop.save_game_data() 
    gameover_input_lock = 45
    game_state = STATE_GAMEOVER

def update_game_logic_dt(dt):
    global water_level, magma_spawn_timer, shake_timer, shake_intensity, game_state, score
    global is_wave_surging, wave_surge_timer
    
    step_speed = 180.0 * dt
    
    if score > 0 and score % 5 == 0:
        water_level += ((115 + int(math.sin(pygame.time.get_ticks() / 180) * 12)) - water_level) * 3.0 * dt
    else: water_level += (40 - water_level) * 1.8 * dt 

    if not is_wave_surging and random.random() < 0.48 * dt:
        is_wave_surging, wave_surge_timer = True, random.randint(90, 150)
    elif is_wave_surging:
        wave_surge_timer -= 60 * dt
        if wave_surge_timer <= 0: is_wave_surging = False

    t_wave = pygame.time.get_ticks() / 130
    amp_mod = 28.0 + math.sin(t_wave * 0.5) * 8.0 if is_wave_surging else 6.0 + math.sin(t_wave * 0.2) * 3.0
    glob_bob = math.cos(t_wave * 1.5) * 16.0 if is_wave_surging else math.cos(t_wave * 0.8) * 3.0
    w1 = math.sin(player.x * 0.014 + t_wave * 0.8)
    w2 = math.cos(player.x * 0.04 - t_wave * 1.3)
    exact_water_surface_y = (SCREEN_HEIGHT - water_level) + (w1 * w2) * amp_mod + glob_bob

    if player.y - 12 <= 0 or player.y + 12 >= exact_water_surface_y:
        trigger_game_over(); return

    for lantern in independent_lanterns:
        lantern.update_dt(step_speed, dt)
        if lantern.check_player_bounce(player): shake_timer, shake_intensity = 12, 5  
        elif lantern.check_rope_snag(player):
            if shake_timer == 0: shake_timer, shake_intensity = 4, 1  
            player.velocity = min(player.velocity + 18.0, 72.0) 
            player.x += 240.0 * dt  
            player.trigger_stumble() 

    if len(independent_lanterns) > 0 and independent_lanterns[0].x < -90: independent_lanterns.pop(0)

    if score > 3:
        magma_spawn_timer += 60 * dt
        if magma_spawn_timer > random.randint(70, 130):
            falling_magmas.append(FallingMagma())
            magma_spawn_timer = 0

    for magma in falling_magmas[:]:
        magma.update_dt(dt)
        if not magma.active: falling_magmas.remove(magma); continue
        if magma.y >= exact_water_surface_y:
            magma.active = False
            particle_sys.spawn(magma.x, magma.y, COLORS["DIAMOND"], 6)
            falling_magmas.remove(magma); continue
        if magma.check_collision(player):
            if player.has_shield:
                player.has_shield, shake_timer, shake_intensity = False, 15, 5
                play_sfx(sound_bounce)
            else: trigger_game_over(); return
            falling_magmas.remove(magma)

    for shield in shield_items[:]:
        shield.update_dt(step_speed)
        if shield.x < -40: shield_items.remove(shield)
        elif shield.check_pickup(player):
            player.has_shield = True
            play_sfx(sound_coin)
            shield_items.remove(shield)
        
    for pipe in pipes:
        pipe.update_dt(step_speed)
        if pipe.check_collision_precise(player.x, player.y, player.radius):
            if player.has_shield:
                player.has_shield, player.x, player.velocity, shake_timer, shake_intensity = False, player.x - 20, -90.0, 20, 6
                play_sfx(sound_hit)
                particle_sys.spawn(player.x, player.y, COLORS["SHIELD_GLOW"], 15)
            else: trigger_game_over(); return

        if pipe.check_diamond_pickup(player.x, player.y, player.radius):
            play_sfx(sound_coin)
            skin_shop.total_diamonds += 1
            skin_shop.save_game_data() 
            
        if not pipe.passed and pipe.x + 30 < player.x:
            pipe.passed, score = True, score + 1
            play_sfx(sound_score)
            
    if len(pipes) > 0:
        last_p = pipes[-1]
        max_right_edge = last_p.x + (last_p.top_width if last_p.spawn_style in (0, 2) else last_p.bot_offset_x + last_p.bot_width)
        if max_right_edge < (SCREEN_WIDTH + 140):
            new_pipe = StalactiteObstacle(max_right_edge + random.randint(90, 125))
            pipes.append(new_pipe)
            independent_lanterns.append(spawn_anchored_lantern(new_pipe))
            if random.random() < 0.25: shield_items.append(ShieldPowerUp(new_pipe.x - 20, random.randint(140, 390)))

    if len(pipes) > 0 and pipes[0].x < -240: pipes.pop(0)
# main.py - PHẦN 4: GIAO DIỆN UI & VÒNG LẶP CHẠY GAME CHÍNH ĐIỆN THOẠI
def render_graphics():
    draw_cave_background(display_surf, game_state == STATE_PLAYING, water_level, score)
    if game_state in (STATE_PLAYING, STATE_GAMEOVER):
        for lantern in independent_lanterns: lantern.draw(display_surf)
    for pipe in pipes: pipe.draw(display_surf)
    for shield in shield_items: shield.draw(display_surf)
    for magma in falling_magmas: magma.draw(display_surf)
    particle_sys.draw(display_surf) 
    player.draw(display_surf)

    if game_state == STATE_PLAYING:
        display_surf.blit(font_hud.render(f"DIEM: {score}", True, COLORS["TEXT"]), (20, 20))
        display_surf.blit(font_hud.render(f"x {skin_shop.total_diamonds}", True, COLORS["TEXT"]), (SCREEN_WIDTH - 90, 20))
    elif game_state == STATE_MENU:
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        overlay.fill((15, 12, 20, 225))
        display_surf.blit(overlay, (0, 0))
        shop_btn_txt = f"MUA RONG ({skin_shop.dragon_cost}💎)" if not skin_shop.unlocked_dragon else ("DUNG DOI" if skin_shop.current_skin == 1 else "DUNG RONG")
        display_surf.blit(font_menu.render(shop_btn_txt, True, COLORS["TEXT"]), (30, 28))
        display_surf.blit(font_hud.render(f"{skin_shop.total_diamonds}", True, COLORS["DIAMOND"]), (SCREEN_WIDTH - 32, 24))
        display_surf.blit(font_logo.render("CAVE BIRD", True, COLORS["DIAMOND"]), (95, SCREEN_HEIGHT // 3 - 30))
        display_surf.blit(font_menu.render("BAM HOAC CLICK MAN HINH DE BAY", True, COLORS["TEXT"]), (60, SCREEN_HEIGHT // 2 + 10))
    elif game_state == STATE_GAMEOVER:
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        overlay.fill((35, 15, 25, 195))
        display_surf.blit(overlay, (0, 0))
        display_surf.blit(font_logo.render("DA DE COI!", True, (255, 65, 65)), (95, SCREEN_HEIGHT // 3 - 20))
        display_surf.blit(font_hud.render(f"DIEM: {score}  |  KY LUC: {skin_shop.high_score}", True, COLORS["TEXT"]), (60, SCREEN_HEIGHT // 2 - 20))
        if gameover_input_lock <= 0: display_surf.blit(font_menu.render("CHAM MAN HINH DE CHOI LAI", True, (220, 220, 220)), (100, SCREEN_HEIGHT // 2 + 40))

# --- VÒNG LẶP CHẠY GAME CHÍNH ĐỒNG BỘ DELTA TIME ---
while running:
    # Trích xuất số mili-giây trôi qua đổi ra giây thực tế
    dt = clock.tick(60) / 1000.0
    if dt > 0.1: dt = 0.1 # Khóa trần chống văng bản đồ khi đứng máy
    
    player.skin = skin_shop.current_skin 
    handle_events()
    
    player.update_dt(game_state == STATE_PLAYING, dt)
    particle_sys.update_dt(dt)
    
    if game_state == STATE_PLAYING:
        update_game_logic_dt(dt)
    elif game_state == STATE_GAMEOVER and gameover_input_lock > 0:
        gameover_input_lock -= 60 * dt
        
    render_graphics()
    
    render_offset_x = random.randint(-shake_intensity, shake_intensity) if shake_timer > 0 else 0
    render_offset_y = random.randint(-shake_intensity, shake_intensity) if shake_timer > 0 else 0
    if shake_timer > 0: shake_timer -= 60 * dt

    real_w, real_h = screen.get_size()
    scale_ratio = min(real_w / SCREEN_WIDTH, real_h / SCREEN_HEIGHT)
    new_w, new_h = int(SCREEN_WIDTH * scale_ratio), int(SCREEN_HEIGHT * scale_ratio)
    scaled_surf = pygame.transform.smoothscale(display_surf, (new_w, new_h))
    
    screen.fill((0, 0, 0))
    screen.blit(scaled_surf, ((real_w - new_w) // 2 + render_offset_x, (real_h - new_h) // 2 + render_offset_y))
    pygame.display.flip()
    
    # 🌟 HIỆU NĂNG ANDROID: Kích hoạt dọn rác bộ nhớ đệm RAM để máy chạy nhẹ tênh
    gc.collect()

pygame.quit()
sys.exit()

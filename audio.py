# audio.py
import pygame
import math
import random

pygame.mixer.init()

def generate_sound(freq, duration_ms, wave_type="sine", volume=0.2):
    sample_rate = 22050
    n_samples = int(sample_rate * (duration_ms / 1000.0))
    buf = bytearray()
    for i in range(n_samples):
        t = float(i) / sample_rate
        if wave_type == "sine":
            val = int(127.0 * math.sin(2.0 * math.pi * freq * t)) + 128
        elif wave_type == "square":
            val = 190 if math.sin(2.0 * math.pi * freq * t) > 0 else 60
        else:
            val = random.randint(60, 190)
        buf.append(val)
    try:
        sound = pygame.mixer.Sound(buffer=bytes(buf))
        sound.set_volume(volume)
        return sound
    except:
        return None

# Bộ hiệu ứng âm thanh điện tử arcade độc quyền
sound_flap = generate_sound(350, 70, "sine", volume=0.25)
sound_score = generate_sound(950, 90, "square", volume=0.15)
sound_hit = generate_sound(100, 300, "noise", volume=0.3)
sound_coin = generate_sound(1200, 70, "sine", volume=0.2) 
sound_bounce = generate_sound(600, 120, "sine", volume=0.25)

def play_sfx(sound_obj):
    if sound_obj: sound_obj.play()

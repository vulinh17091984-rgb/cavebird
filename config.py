# config.py - MÃ NGUỒN CẤU HÌNH ĐÃ SỬA LỖI TRÀN Ô CHAT VÀ LƯU FILE ANDROID
import os

# 1. ĐỊNH DẠNG KÍCH THƯỚC MÀN HÌNH ẢO
SCREEN_WIDTH = 400
SCREEN_HEIGHT = 600

# 2. TỰ ĐỘNG CHUYỂN VÙNG LƯU FILE ĐIỂM CAO SANG BỘ NHỚ AN TOÀN CỦA ANDROID
try:
    from android import storage
    SAVE_FILE = os.path.join(storage.get_internal_storage_dir(), "save_data.json")
except ImportError:
    SAVE_FILE = "save_data.json"

# 3. BẢNG MÀU SẮC ĐỒ HỌA CHUẨN
COLORS = {
    "CAVE_BG": (24, 20, 32),
    "GRID_LINE": (32, 28, 44),
    "ROCK_BASE": (48, 42, 58),
    "ROCK_MID": (68, 60, 82),
    "STALACTITE": (95, 84, 115),
    "CRYSTAL": (0, 225, 200),
    "DIAMOND": (0, 190, 255),
    "MAGMA": (255, 65, 30),
    "SHIELD_GLOW": (0, 255, 120),
    "LANTERN_GLOW": (255, 185, 45),
    "BAT_BODY": (115, 100, 135),
    "BAT_WING": (75, 65, 95),
    "DRAGON_BODY": (230, 55, 40),
    "TEXT": (245, 240, 255)
}

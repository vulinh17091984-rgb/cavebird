# config.py - TOÀN BỘ MÃ NGUỒN CẤU HÌNH ĐÃ SỬA LỖI LƯU FILE TRÊN ANDROID
import os

# 1. ĐỊNH DẠNG KÍCH THƯỚC MÀN HÌNH ẢO (VIRTUAL RESOLUTION)
SCREEN_WIDTH = 400
SCREEN_HEIGHT = 600

# 2. ĐÃ SỬA LỖI: TỰ ĐỘNG CHUYỂN VÙNG LƯU FILE ĐIỂM CAO SANG BỘ NHỚ AN TOÀN CỦA ANDROID
try:
    from android import storage
    # Nếu chạy trên điện thoại Android, lưu vào thư mục nội bộ của App để tránh bị hệ thống chặn
    SAVE_FILE = os.path.join(storage.get_internal_storage_dir(), "save_data.json")
except ImportError:
    # Nếu chạy trên Laptop/PC, lưu file trực tiếp tại thư mục chứa code game
    SAVE_FILE = "save_data.json"

# 3. BẢNG MÀU SẮC ĐỒ HỌA CHUẨN (TỐI ƯU HIỂN THỊ HANG ĐÁ TỰ NHIÊN)
COLORS = {
    "CAVE_BG": (24, 20, 32),          # Màu nền hang đá tối
    "GRID_LINE": (32, 28, 44),        # Màu lưới Grid nền hành tinh
    "ROCK_BASE": (48, 42, 58),        # Màu vách vạt đá lớp gốc
    "ROCK_MID": (68, 60, 82),         # Màu vách vạt đá lớp giữa
    "STALACTITE": (95, 84, 115),       # Màu đỉnh nhọn thạch nhũ pha lê
    "CRYSTAL": (0, 225, 200),         # Màu hạt bụi ánh sáng tĩnh
    "DIAMOND": (0, 190, 255),         # Màu kim cương xanh dương tỏa sáng
    "MAGMA": (255, 65, 30),           # Màu khối magma dung nham rơi
    "SHIELD_GLOW": (0, 255, 120),     # Màu vòng bảo vệ phản quang xanh lá
    "LANTERN_GLOW": (255, 185, 45),    # Màu quầng sáng lồng đèn Wolfram tỏa nhẹ
    "BAT_BODY": (115, 100, 135),       # Màu cơ thể dơi mặc định
    "BAT_WING": (75, 65, 95),         # Màu cánh dơi mặc định
    "DRAGON_BODY": (230, 55, 40),      # Màu rồng rực lửa khi mở khóa
    "TEXT": (245, 240, 255)           # Màu chữ giao diện hiển thị
}

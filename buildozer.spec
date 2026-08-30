[app]
# (PHẦN 1/2) - THÔNG TIN TỰA GAME VÀ PHIÊN BẢN HỆ THỐNG
title = Cave Bird
package.name = cavebird
package.domain = org.game
source.dir = .

# Cho phép robot quét gom cả file mã nguồn .py và file phông chữ .ttf vào game
source.include_exts = py, ttf
version = 1.0

# KHÓA CỨNG: Ép lõi pygame chuẩn di động và tắt bỏ các thư viện sdl2 mở rộng gây lỗi
requirements = python3, pygame==2.6.0

orientation = portrait
fullscreen = 1

# CẤU HÌNH VÀNG: Ép robot dùng bộ Android NDK 25c ổn định tuyệt đối cho Pygame
android.api = 31
android.minapi = 21
android.ndk = 25c
android.build_tools_version = 31.0.0

# Khóa cố định phiên bản Command Line Tools của Google để có file sdkmanager chuẩn
android.meta_data = "android.sdk_cmdline_tools_version=11.0"
android.skip_update = False
android.accept_sdk_license = True
# (PHẦN 2/2) - CẤP QUYỀN HỆ THỐNG VÀ PHÂN LỚP ĐÓNG GÓI CHIP
# ĐÃ SỬA LỖI CHÍ MẠNG: Mở quyền truy cập bộ nhớ để game được phép tạo file lưu điểm cao
android.permissions = android.permission.WRITE_EXTERNAL_STORAGE, android.permission.READ_EXTERNAL_STORAGE

# Chỉ định kiến trúc chip 64-bit arm64-v8a thông dụng trên mọi dòng máy Android hiện nay
android.archs = arm64-v8a

# Cho phép game tự động bật chế độ gỡ lỗi khi xuất file cài đặt APK
android.debug = 1

[buildozer]
log_level = 2
warn_on_root = 1

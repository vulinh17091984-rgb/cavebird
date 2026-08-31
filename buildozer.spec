[app]
title = Cave Bird
package.name = cavebird
package.domain = org.vulinh
source.dir = .
source.include_exts = py,png,jpg,jpeg,ttf,wav,mp3
version = 1.0.0

# Sử dụng thư viện Kivy đồ họa di động chính thức để đóng gói tự động sạch lỗi C
requirements = python3, kivy

orientation = portrait
fullscreen = 1
android.permissions = INTERNET

# Sử dụng kho SDK/NDK mặc định an toàn của máy ảo GitHub Actions
android.sdk_path = /usr/local/lib/android/sdk
android.ndk_path = /usr/local/lib/android/sdk/ndk/25.2.9519653

# Chỉ định duy nhất một kiến trúc chip 64-bit giúp tối ưu RAM máy chủ
android.archs = arm64-v8a

android.api = 33
android.minapi = 21
android.enable_androidx = True
android.release_artifact = apk
android.debug_artifact = apk

[buildozer]
# ĐỔI THÀNH 0: Tắt toàn bộ 30.000 dòng log debug làm nghẽn hiển thị của GitHub Actions
# Nếu có lỗi sập ngầm, hệ thống sẽ in trực tiếp lỗi [ERROR] ra màn hình ngay lập tức
log_level = 0
warn_on_root = 1

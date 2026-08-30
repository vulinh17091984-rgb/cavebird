[app]
title = Cave Bird
package.name = cavebird
package.domain = org.game
source.dir = .
source.include_exts = py, ttf
version = 1.0

requirements = python3, pygame==2.6.0
orientation = portrait
fullscreen = 1

# --- ÉP PHIÊN BẢN CHUẨN ĐỂ KHÔNG BỊ MẤT ĐƯỜNG DẪN SDKMANAGER ---
android.api = 31
android.minapi = 21
android.ndk = 25c
android.build_tools_version = 31.0.0
# Khóa cố định Command Line Tools bản 11.0 của Google (bản lưu file sdkmanager ở vị trí truyền thống)
android.meta_data = "android.sdk_cmdline_tools_version=11.0"
android.skip_update = False
android.accept_sdk_license = True

android.archs = arm64-v8a

[buildozer]
log_level = 2
warn_on_root = 1

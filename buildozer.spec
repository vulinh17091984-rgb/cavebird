[app]
title = Cave Bird
package.name = cavebird
package.domain = org.game
source.dir = .
source.include_exts = py,png,jpg,ttf,json,wav,mp3
version = 1.0

requirements = python3,pygame
orientation = portrait
fullscreen = 1

# --- ĐÃ ÉP PHIÊN BẢN 31 SIÊU ỔN ĐỊNH ĐỂ SỬA DỨT ĐIỂM LỖI ĐƯỜNG DẪN SDK ---
android.api = 31
android.minapi = 21
android.ndk = 23b
android.build_tools_version = 31.0.0
android.skip_update = False
android.accept_sdk_license = True

android.archs = arm64-v8a

[buildozer]
log_level = 2
warn_on_root = 1

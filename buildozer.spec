[app]
title = Cave Bird
package.name = cavebird
package.domain = org.vulinh
source.dir = .
source.include_exts = py,png,jpg,jpeg,ttf,wav,mp3
version = 1.0.0

# Yêu cầu cài đặt bắt buộc cho game Pygame thuần (p4a sẽ tự cấu hình jni cho SDL2)
requirements = python3, pygame==2.6.0

orientation = portrait
fullscreen = 1
android.permissions = INTERNET
android.api = 33
android.minapi = 21
android.ndk = 25c
android.archs = arm64-v8a
android.enable_androidx = True
android.release_artifact = apk
android.debug_artifact = apk

[buildozer]
log_level = 2
warn_on_root = 1

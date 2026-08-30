[app]
title = Cave Bird
package.name = cavebird
package.domain = org.vulinh
source.dir = .
source.include_exts = py,png,jpg,jpeg,ttf,wav,mp3
version = 1.0.0

# Sử dụng thư viện pygame chuẩn cho Android
requirements = python3, pygame==2.6.0

orientation = portrait
fullscreen = 1
android.permissions = INTERNET

# CẤU HÌNH BỘ CÔNG CỤ SDK ỔN ĐỊNH - KHÔNG ĐƯỢC VIẾT TRÙNG LẶP
android.api = 33
android.build_tools_version = 34.0.0
android.minapi = 21
android.ndk = 25c
android.archs = arm64-v8a
android.enable_androidx = True

# Định dạng xuất file cài đặt
android.release_artifact = apk
android.debug_artifact = apk

[buildozer]
log_level = 2
warn_on_root = 1

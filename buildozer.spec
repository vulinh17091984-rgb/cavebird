[app]
title = Cave Bird
package.name = cavebird
package.domain = org.vulinh
source.dir = .
source.include_exts = py,png,jpg,jpeg,ttf,wav,mp3
version = 1.0.0

# ĐỔI SANG PYGAME 2.5.2: Phiên bản ổn định nhất cho Android, cam kết vượt qua lỗi compile create
requirements = python3, pygame==2.5.2

orientation = portrait
fullscreen = 1
android.permissions = INTERNET

# ÉP SỬ DỤNG KHO SDK/NDK CHUẨN CÓ SẴN CỦA MÁY ẢO GITHUB ACTIONS
android.sdk_path = /usr/local/lib/android/sdk
android.ndk_path = /usr/local/lib/android/sdk/ndk/25.2.9519653

# CHỈ ĐỊNH DUY NHẤT KIẾN TRÚC CHIP 64-BIT
android.archs = arm64-v8a

android.api = 33
android.minapi = 21
android.enable_androidx = True
android.release_artifact = apk
android.debug_artifact = apk

[buildozer]
log_level = 2
warn_on_root = 1

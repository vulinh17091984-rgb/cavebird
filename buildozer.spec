[app]
title = Cave Bird
package.name = cavebird
package.domain = org.game
source.dir = .
source.include_exts = py, ttf
version = 1.0

# KHÓA CỐ ĐỊNH: Rút gọn yêu cầu để robot đám mây đóng gói mượt mà, không đi tìm file rác
requirements = python3, pygame==2.6.0

orientation = portrait
fullscreen = 1

android.api = 31
android.minapi = 21
android.ndk = 25c
android.build_tools_version = 31.0.0
android.meta_data = "android.sdk_cmdline_tools_version=11.0"
android.skip_update = False
android.accept_sdk_license = True
android.permissions = android.permission.WRITE_EXTERNAL_STORAGE, android.permission.READ_EXTERNAL_STORAGE
android.archs = arm64-v8a
android.debug = 1

[buildozer]
log_level = 2
warn_on_root = 1

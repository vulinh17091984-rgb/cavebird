[app]
title = Cave Bird
package.name = cavebird
package.domain = org.game
source.dir = .
source.include_exts = py,png,jpg,ttf,json,wav,mp3
version = 1.0

# BẮT BUỘC: Khai báo thư viện Pygame thay vì Kivy
requirements = python3,pygame

orientation = portrait
fullscreen = 1
android.archs = arm64-v8a

[buildozer]
log_level = 2
warn_on_root = 1

[app]

# (str) Title of your application
title = Cave Bird

# (str) Package name
package.name = cavebird

# (str) Package domain (needed for android packaging)
package.domain = org.vulinh

# (str) Source code where the main.py lives
source.dir = .

# (list) Source files to include (let empty to include all the files)
source.include_exts = py,png,jpg,jpeg,ttf,wav,mp3

# (str) Application versioning (method 1)
version = 1.0.0

# (list) Application requirements
# Đổi sang kivy để tối ưu hóa render đồ họa trên Android, tránh lỗi NDK của pygame
requirements = python3,kivy

# (str) Custom source folders for requirements
# requirements.source.kivy = ../../kivy

# (list) Garden requirements
#garden_requirements =

# (str) Presplash of the application
#presplash.filename = %(source.dir)s/data/presplash.png

# (str) Icon of the application
#icon.filename = %(source.dir)s/data/icon.png

# (str) Supported orientations (valid options are: landscape, portrait, portrait-reverse, landscape-reverse)
orientation = portrait

# (list) List of service to declare
#services =

#
# Android specific
#

# (bool) Indicate if the application should be fullscreen or not
fullscreen = 1

# (list) Permissions
android.permissions = INTERNET

# (int) Target Android API, should be as high as possible.
android.api = 33

# (int) Minimum API your APK will support.
android.minapi = 21

# (int) Android SDK version to use
#android.sdk = 33

# (str) Android NDK version to use
android.ndk = 25c

# (bool) Use --private data storage (True) or --dir public storage (False)
android.private_storage = True

# (str) Android NDK directory (if empty, it will be automatically downloaded.)
#android.ndk_path =

# (str) Android SDK directory (if empty, it will be automatically downloaded.)
#android.sdk_path =

# (str) ANT directory (if empty, it will be automatically downloaded.)
#android.ant_path =

# (list) Android architectures to build for (e.g. armeabi-v7a, arm64-v8a, x86, x86_64)
android.archs = arm64-v8a

# (bool) Enable AndroidX support. Required when modern libraries are used.
android.enable_androidx = True

# (bool) Skip byte compile for .py files
#android.skip_byte_compile = False

# (str) Format used to package the app for release mode (aab or apk or aar)
android.release_artifact = apk

# (str) Format used to package the app for debug mode (aab or apk or aar)
android.debug_artifact = apk

#
# Python for android (p4a) specific
#

# (str) python-for-android branch to use, defaults to master
#p4a.branch = master

# (str) python-for-android git clone directory (if empty, it will be automatically cloned from github)
#p4a.source_dir =

# (str) The directory in which python-for-android should look for your own recipes (if any)
#p4a.local_recipes =

# (str) Filename to the hook script
#p4a.hook =


#
# Buildozer section
#

[buildozer]

# (int) Log level (0 = error only, 1 = info, 2 = debug and error)
# Đặt thành 2 để hiển thị log chi tiết nhất, giúp debug lỗi mạng/RAM dễ dàng
log_level = 2

# (int) Display warning if buildozer is run as root (0 = False, 1 = True)
warn_on_root = 1

# (str) Path to build artifact storage, its default is <source.dir>/.buildozer
# build_dir = ./.buildozer

# (str) Path to bin directory, its default is <source.dir>/bin
# bin_dir = ./bin

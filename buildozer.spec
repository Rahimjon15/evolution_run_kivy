[app]
title = Evolution Run
package.name = evolution_run
package.domain = org.rahimjon.run
source.dir = .
source.include_exts = py,png,jpg,kv,ogg,wav,mp3
version = 1.2.0

fullscreen = 1
orientation = landscape

android.archs = armeabi-v7a, arm64-v8a
android.api = 35
android.minapi = 21
android.ndk = 21e
android.ndk_path = /mnt/c/Users/VIRA/Android/ndk/android-ndk-r21e

android.sdk_path = /mnt/c/Users/VIRA/Android
android.sdk_api = 35

android.build_mode = release
android.gradle_dependencies = com.android.support:multidex:1.0.3

# Включаем сборку App Bundle
android.aab = True

# Иконки/сплеш — пока пусто
icon.filename = %(source.dir)s/data/icon.png
presplash.filename = %(source.dir)s/data/presplash.png

requirements = python3,kivy

[buildozer]
log_level = 2
warn_on_root = 0











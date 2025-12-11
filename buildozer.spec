
[app]
title = Evolution Run
package.name = evolution_run
package.domain = org.rahimjon.run
source.dir = .
source.include_exts = py,png,jpg,kv,ogg,wav,mp3
version = 1.2.0

fullscreen = 1
orientation = landscape

# Архитектуры
android.archs = armeabi-v7a, arm64-v8a

# Buildozer поддерживает максимум 33 — используем его
android.api = 33
android.minapi = 21
android.sdk_api = 33
android.ndk = 23b

# Не указываем локальные пути!
# android.ndk_path =
# android.sdk_path =

android.build_mode = release

# Современный multidex
android.gradle_dependencies = androidx.multidex:multidex:2.0.1

# Включаем сборку AAB
android.aab = True

# Иконки
icon.filename = %(source.dir)s/data/icon.png
presplash.filename = %(source.dir)s/data/presplash.png

requirements = kivy, cython

# Вставляем targetSdkVersion = 35 ПРИНУДИТЕЛЬНО
android.add_gradle_dependencies = com.android.tools.build:gradle:8.1.1
android.gradle_options = -Pandroid.injected.build.model.only.versioned=3
android.add_src = True

# Ключевая строка!
android.extra_gradle_options = 
    android.compileSdkVersion=35
    android.defaultConfig.targetSdkVersion=35

[buildozer]
log_level = 2
warn_on_root = 0










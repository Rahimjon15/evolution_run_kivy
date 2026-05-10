

[app]
title = Evolution Run
package.name = evolution_run
package.domain = org.rahimjon.run
source.dir = .
source.include_exts = py,png,jpg,kv,ttf,otf,mp3,wav,ogg,txt,json
version = 1.2.0

fullscreen = 1
orientation = landscape

# Архитектуры (убрал armeabi-v7a для скорости сборки)
android.archs = arm64-v8a

# Упрощённые настройки SDK (без конфликтов)
android.api = 30
android.minapi = 21
android.sdk = 30
android.ndk = 25c

# Обязательные требования (добавил plyer и android)
requirements = python3,kivy,plyer,android,hostpython3

# Иконки (проверьте, что файлы реально существуют в папке data)
icon.filename = data/icon.png
presplash.filename = data/presplash.png

# Разрешения
android.permissions = INTERNET,ACCESS_FINE_LOCATION,ACCESS_COARSE_LOCATION

# Остальное убираем (слишком сложные настройки ломают сборку)
android.gradle_dependencies =
android.add_gradle_dependencies =
android.gradle_options =
android.extra_gradle_options =

[buildozer]
log_level = 2
warn_on_root = 0








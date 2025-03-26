[app]
title = Snake Game
package.name = snakegame
package.domain = org.snakegame
source.dir = .
source.include_exts = py,png,jpg,kv,atlas
version = 1.0

# Requirements
requirements = python3,kivy==2.0.0,pillow,sdl2_ttf==2.0.15,sdl2_image==2.0.5,sdl2_mixer==2.0.0

# (str) Presplash of the application
presplash.filename = %(source.dir)s/icon.png

# (str) Icon of the application
icon.filename = %(source.dir)s/icon.png

# (str) Supported orientation (one of landscape, sensorLandscape, portrait or all)
orientation = portrait

# (bool) Indicate if the application should be fullscreen or not
fullscreen = 0

# Android configuration
android.api = 33
android.minapi = 21
android.ndk = 25.2.9519653
android.ndk_api = 21
android.archs = armeabi-v7a, arm64-v8a
android.build_tools_version = 33.0.0

android.skip_update = True
android.accept_sdk_license = True
android.allow_backup = True
android.permissions = INTERNET
android.gradle_dependencies = org.jetbrains.kotlin:kotlin-stdlib-jdk7:1.3.72

# iOS specific
ios.kivy_ios_url = https://github.com/kivy/kivy-ios
ios.kivy_ios_branch = master
ios.ios_deploy_url = https://github.com/phonegap/ios-deploy
ios.ios_deploy_branch = 1.10.0

[buildozer]
log_level = 2
warn_on_root = 1

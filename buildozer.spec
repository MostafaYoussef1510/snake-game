[app]
title = Snake Game
package.name = snakegame
package.domain = org.snakegame
source.dir = .
source.include_exts = py,png,jpg,kv,atlas
version = 1.0

requirements = python3,kivy==2.1.0,pillow

orientation = portrait
fullscreen = 0
android.arch = armeabi-v7a

# Android specific
android.permissions = INTERNET
android.api = 27
android.minapi = 21
android.sdk = 20
android.ndk = 23b
android.accept_sdk_license = True
android.gradle_dependencies = org.jetbrains.kotlin:kotlin-stdlib-jdk7:1.3.72

# iOS specific
ios.kivy_ios_url = https://github.com/kivy/kivy-ios
ios.kivy_ios_branch = master
ios.ios_deploy_url = https://github.com/phonegap/ios-deploy
ios.ios_deploy_branch = 1.10.0

[buildozer]
log_level = 2
warn_on_root = 1

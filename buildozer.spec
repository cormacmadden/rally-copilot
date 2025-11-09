[app]
title = Rally Copilot
package.name = rallycopilot
package.domain = org.rallycopilot

source.dir = .
source.include_exts = py,png,jpg,kv,atlas

version = 0.1
requirements = python3,kivy==2.2.1,kivymd,plyer

orientation = portrait
fullscreen = 0

# Android permissions
android.permissions = INTERNET,ACCESS_FINE_LOCATION,ACCESS_COARSE_LOCATION,FOREGROUND_SERVICE

# Android architecture
android.archs = arm64-v8a,armeabi-v7a

# Python for Android configuration
p4a.branch = master
p4a.bootstrap = sdl2

# iOS permissions
ios.kivy_ios_url = https://github.com/kivy/kivy-ios
ios.kivy_ios_branch = master
ios.ios_deploy_url = https://github.com/phonegap/ios-deploy
ios.ios_deploy_branch = 1.10.0

[buildozer]
log_level = 2
warn_on_root = 0

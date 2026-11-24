[app]
title = MAXDIS
package.name = maxdis
package.domain = id.arinex

source.dir = .
source.include_exts = py,png,jpg,jpeg,kv,atlas,json,ttf
source.exclude_dirs = tests,bin,venv,.venv,.buildozer,__pycache__

version = 2.5.6

# pyjnius & android sudah otomatis ikut saat build Android.
requirements = python3,kivy==2.3.0

orientation = portrait
fullscreen = 0

# Warna layar splash = warna header (#e51b23)
presplash.color = #e51b23

# Aktifkan setelah file gambarnya ada di folder assets/
#icon.filename = %(source.dir)s/assets/logo-192.png
#presplash.filename = %(source.dir)s/assets/logo-192.png

# INTERNET            : buka tautan Rak + cek status online
# ACCESS_NETWORK_STATE: status jaringan
android.permissions = INTERNET,ACCESS_NETWORK_STATE

android.api = 34
android.minapi = 24
android.archs = arm64-v8a, armeabi-v7a
android.accept_sdk_license = True
android.allow_backup = True

[buildozer]
log_level = 2
warn_on_root = 1

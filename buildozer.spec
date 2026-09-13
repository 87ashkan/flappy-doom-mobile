[app]

# (str) Title of your application
title = Flappy Doom

# (str) Package name
package.name = flappydoom

# (str) Package domain (needed for android packaging)
package.domain = org.flappy

# (str) Source directory where the main.py file is located
source.dir = .

# (list) Source files to include (let it empty to include all files)
source.include_exts = py,png,jpg,ttf,wav,mp3,json

# (list) List of inclusions using pattern matching
source.include_patterns = assets/*

# (str) Application versioning
version = 1.0

# (list) Application requirements
requirements = python3,pygame

# (str) Supported orientation (landscape, portrait or all)
orientation = landscape

# (int) Fullscreen (1 = yes, 0 = no)
fullscreen = 1

# (list) Permissions
android.permissions = WAKE_LOCK

# (str) Android SDK version to use
android.api = 33

# (str) Minimum API version
android.minapi = 21

# (int) Automatically accept SDK license agreements
android.accept_sdk_license = True

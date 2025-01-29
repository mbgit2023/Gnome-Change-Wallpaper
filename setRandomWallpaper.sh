# Script called by the crond

#!/bin/bash

PID=$(pgrep gnome-session | head -1)
if [ -z "$PID" ]; then
    exit 1
fi

export DBUS_SESSION_BUS_ADDRESS=$(grep -z DBUS_SESSION_BUS_ADDRESS /proc/$PID/environ | cut -d= -f2-)
PYTHON=$(which python3)
if [ -z "$PYTHON" ]; then
    exit 1
fi

BASE_DIR="$HOME/Gnome-Change-Wallpaper"
SET_WALLPAPER_SCRIPT="$BASE_DIR/setwallpaper.py"

if [ ! -f "$SET_WALLPAPER_SCRIPT" ]; then
    exit 1
fi

$PYTHON "$SET_WALLPAPER_SCRIPT"
if [ $? -ne 0 ]; then
    exit 1
fi

exit 0

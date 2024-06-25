# Script called by the crond

PID=`pgrep gnome-session | head -1`
export DBUS_SESSION_BUS_ADDRESS=`grep -z DBUS_SESSION_BUS_ADDRESS /proc/$PID/environ | cut -d= -f2-`

python=`which python3`
$python ~/GnomeChangeWallpaper/setwallpaper.py

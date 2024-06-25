#!/bin/bash

echo ""
echo "Gnome Change Wallpaper Installer"
echo ""

DESTINATION="$HOME"
mkdir -p ${DESTINATION}

# Find __ARCHIVE__ maker, read archive content and decompress it
ARCHIVE=$(awk '/^__ARCHIVE__/ {print NR + 1; exit 0; }' "${0}")
tail -n+${ARCHIVE} "${0}" | tar xpJv -C ${DESTINATION}

$HOME/GnomeChangeWallpaper/install.sh

echo "Go into the folder ~/GnomeChangeWallpaper and execute"
echo "./gnomechangewall.sh"

echo ""
echo "Installation complete."
echo ""

exit 0

__ARCHIVE__

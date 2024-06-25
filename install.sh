#!/usr/bin/zsh

GREEN='\033[1;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

clear

# install the dependencies
echo -e "${YELLOW}\nInstalling the dependencies..\n"
echo -e "$NC Installing libxcb-curso0"
sudo apt install libxcb-cursor0
echo -e "$NC"
echo -e "${GREEN}\nLib: libxcb-curso0 installed\n"
echo -e "$NC Installing PyQt6"
pip install pyqt6
echo -e "${GREEN} \nModule: PyQt6 installed\n"
echo -e "$NC Installing Pillow"
pip install pillow
echo -e "${GREEN} \nModule: Pillow installed\n"

# Checks for the permissions
echo "${YELLOW}Check for scripts execution permissions"
for file in `ls ./*.sh`
do
  if [[ -x $file ]]
  then
    echo -e "${GREEN} File: $file OK"
  else
    chmod 755 $file
  fi
done

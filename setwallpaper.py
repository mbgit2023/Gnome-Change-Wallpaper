import os
import subprocess

path=os.path.dirname(__file__)

f = open(fr"{path}/changewallpaper", "r")
line = f.readline()
f.close()

folder=line.split("'")[1]

if not os.path.isfile(fr'{path}/fileList'):
    f=open(fr'{path}/fileList', 'w')
    f.close()

list = []
with open(fr'{path}/fileList') as f:
   list = f.read().splitlines()

filecount=0
for fileimg in os.listdir(folder):
    filecount=filecount+1

while True:
    p = subprocess.run(["/bin/zsh", fr"{path}/selectRandWall.sh", folder], capture_output=True)
    file=str(p.stdout).split("'")[1].split("\\")[0]
    if file not in list:
        f=open(fr'{path}/fileList', 'a')
        f.write(f"{file}\n")
        f.close()
        break
    if filecount == len(list):
        os.unlink(fr'{path}/fileList')
        break

uri=fr"file://{folder}/{file}"

p=subprocess.run(["/usr/bin/gsettings", "set", "org.gnome.desktop.background", "picture-uri", fr"'{uri}'"], capture_output=True)
q=subprocess.run(["/usr/bin/gsettings", "set", "org.gnome.desktop.background", "picture-uri-dark", fr"'{uri}'"], capture_output=True)



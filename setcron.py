import os
import subprocess
import sys

path=os.path.dirname(__file__)

f = open("./changewallpaper", "r")
line = f.readline()
f.close()

folder=line.split("'")[1]
time=line.split("'")[2].strip()

python = sys.executable
zsh='/usr/bin/zsh'
setbackground = fr'{path}/setRandomWallpaper.sh'
crontabfile = './chgwallcron'
crontabstring=""

if time == "1 min":
    crontabstring = fr"* * * * * {zsh} '{setbackground}'"
if time == "5 min":
    crontabstring = fr"*/5 * * * * {zsh} '{setbackground}'"
elif time == "15 min":
    crontabstring = fr"*/115 * * * * {zsh} '{setbackground}'"
elif time == "30 min":
    crontabstring = fr"*/30 * * * * {zsh} '{setbackground}'"
elif time == "1 hour":
    crontabstring = fr"0 * * * * {zsh} '{setbackground}'"
elif time == "3 hours":
    crontabstring = fr"0 */3 * * * {zsh} '{setbackground}'"
elif time == "6 hours":
    crontabstring = fr"0 */6 * * * {zsh} '{setbackground}'"
elif time == "12 hours":
    crontabstring = fr"0 */12 * * * {zsh} '{setbackground}'"
elif time == "1 day":
    crontabstring = fr"0 10 * * * {zsh} '{setbackground}'"
elif time == "1 week":
    p=subprocess.run([python, "./getweekday.py"], capture_output=True)
    weekday = p.stdout
    crontabstring = f"* * * * {int(weekday)} {python} '{setbackground}'"

f = open(crontabfile, "w")
f.write(crontabstring)
f.write("\n")
f.close()

subprocess.run(["crontab", crontabfile])
subprocess.run(["/usr/bin/zsh", "./setRandomWallpaper.sh"])
# Creates a file containing the list of the image files found in the selected folder

import os
import sys

f = open("./foldercontent.lst", "w")
for file in os.listdir(sys.argv[1]):
    f.write(file)
    f.write("\n")

f.close()
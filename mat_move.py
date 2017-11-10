import os
import shutil
import re
import sys
if sys.version_info[0] >= 3:
    raise Exception("Must be using Python 2")

print "This program stores Participant Matlab Data (log.txt files)"
print "into folders organised by participant number"

# The absolute path of the folder housing all participant Matlab Data log.txt files
start_path = "/home/burleigh/Desktop/FCTM_S_Data/matlab_data"
pathA = start_path + "/A"
pathB = start_path + "/B"

# The path of the folder containing participant folders (17271, etc...)
end_path = "/home/burleigh/Desktop/FCTM_S_Data"

# Regular expression denoting participant format
# i.e 17271 = '\d{5}'
regex = '\d{5}'

# start in path A
for f in os.listdir(pathA):
    participant = re.search(regex, f).group(0)
    if participant in f:
        if os.path.isdir(pathA + '/' + f):  # ensuring we only work on folders
            for files in os.listdir(pathA + '/' + f):
                if files[-7:] == "log.txt":  # ensuring we only work on the right text files
                    temp_path = end_path + '/' + participant + '/bh/' + participant + '_A'
                    if not os.path.exists(temp_path):  # make sure we have the folder we output to
                        os.makedirs(temp_path)  # or make it
                    shutil.copy(pathA + '/' + f + '/' + files, temp_path)

# then repeat for B
for f in os.listdir(pathB):
    participant = re.search(regex, f).group(0)
    if participant in f:
        if os.path.isdir(pathB + '/' + f):  # ensuring we only work on folders
            for files in os.listdir(pathB + '/' + f):
                if files[-7:] == "log.txt":  # ensuring we only work on the right text files
                    temp_path = end_path + '/' + participant + '/bh/' + participant + '_B'
                    if not os.path.exists(temp_path):  # make sure we have the folder we output to
                        os.makedirs(temp_path)  # or make it
                    shutil.copy(pathA + '/' + f + '/' + files, temp_path)

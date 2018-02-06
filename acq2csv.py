from shutil import move
import bioread
import csv
import os
import re
import sys
if sys.version_info[0] >= 3:
    raise Exception("Must be using Python 2")

print "This program takes the absolute directory of a series of .acq files"
print "and returns them all as .csv files organised into folders."

# CUSTOM HEADERS DEFINED BELOW #
# change these values to edit custom headers in the csv

custom_headers = [
    None,
    "CH14",
    "CH28",
    "CH29",
    "CH30",
    "CH31",
    "CH32",
    "CH35"
]

# Path to all .acq files (files should not be within sub-folders
acq_path = "/home/burleigh/Documents/FCTM_Bx_Data/PartBio2"
#acq_path = "C:/Users/zacha/Documents/LSU/Greening Lab/Subject Data/Participant_Biopac_Data"

# Include time stamps?
times = False

# Include headers?
head = False

# Regular expression denoting participant format
# i.e 17271 = '\d{5}'
regex = '\d{5}'


# The below functions convert Biopac .acq files to readable .csv files
def write_text(datafile, out_stream, channel_indexes, missing_val):
    writer = csv.writer(out_stream, delimiter=str(","))
    if not channel_indexes:
        channel_indexes = range(len(datafile.channels))
    chans = [datafile.channels[i] for i in channel_indexes]
    if times and head:  # if user wants time stamps and custom headers
        headers = ["time (s)"] + [
            "{0} ({1})".format(c.name, c.units) for c in chans]
        headers = [s.encode('utf-8') for s in headers]
        writer.writerow(custom_headers)
        writer.writerow(headers)
        for i, t in enumerate(datafile.time_index):
            rd = [t] + [data_or_blank(c, i, missing_val) for c in chans]
            writer.writerow(rd)
    elif times and not head:  # if user wants only time stamps
        for i, t in enumerate(datafile.time_index):
            rd = [t] + [data_or_blank(c, i, missing_val) for c in chans]
            writer.writerow(rd)
    elif head and not times:
        headers = ["{0} ({1})".format(c.name, c.units) for c in chans]
        headers = [s.encode('utf-8') for s in headers]
        writer.writerow(custom_headers)
        writer.writerow(headers)
        for i, t in enumerate(datafile.time_index):
            rd = [data_or_blank(c, i, missing_val) for c in chans]  # ignore time (t)
            writer.writerow(rd)
    else:  # user wants none
        for i, t in enumerate(datafile.time_index):
            rd = [data_or_blank(c, i, missing_val) for c in chans]  # ignore time (t)
            writer.writerow(rd)


def data_or_blank(channel, index, missing_val):
    ci = index // channel.frequency_divider
    if index % channel.frequency_divider == 0 and ci < channel.point_count:
        return channel.data[ci]
    return missing_val


def search(array, term):
    results = []
    for element in array:
	if term in element:
	    results.append(element)
    return results


# Store .csv files in a CSV sub folder to be found later
for f in os.listdir(acq_path):
    if os.path.isfile(acq_path + '/' + f):  # ensuring we only work on files
        if f[-4:] == ".acq":  # ensuring we only work on .acq files
            print("Opening {}".format(acq_path + '/' + f))
            acquisition = bioread.read(acq_path + '/' + f)  # read the .acq file

            participant = re.search(regex, f).group(0)  # just participant number
            filename = f[:-4]  # filename without file extension
            print("Participant #{}, Filename {}".format(participant, filename))
            print("Writing to {}".format(filename + '.csv', 'w'))
            output = open(filename + '.csv', 'w')

            write_text(acquisition, output, None, None)
            print("Done")
            print("")
            if not os.path.exists(acq_path + "/CSV"):
                os.makedirs(acq_path + "/CSV")
            move(filename + '.csv', acq_path + '/CSV/' + filename + '.csv')


# Find the subject folder and put the csv files there
# Be sure to prompt first to ensure we're using the right folder
path = "/".join(acq_path.split("/")[:-1])  # change path to one directory up from acq path
csv_path = acq_path + "/CSV"
participants = []
filenames = []
for root, dirs, files in os.walk(csv_path):
    for name in files:
        filenames.append(name)  # now have array of file names
        participants.append(re.search(regex, name).group(0))  # now have array of participant numbers

os.chdir(path)
for num in participants:
    assoc_files = search(filenames, num)  # an array to put filenames containing the participant number
    if os.path.isdir(path + '/' + num):  # participant folder exists already
	if not os.path.isdir(path + '/' + num + '/scr'):
	    os.makedirs(path + '/' + num + "/scr")  # ensure scr folder is there too
	for name in assoc_files:
            try:
		move(csv_path + '/' + name, path + '/' + num + "/scr")  # move files
	    except:
		pass
    else:
    #elif not os.path.isdir(path + '/' + num):  # if participant folder doesn't already exist
	os.makedirs(path + '/' + num)  # make it
	os.makedirs(path + '/' + num + "/scr")   # and its sub folder
	for name in assoc_files:
	    try:
		move(csv_path + '/' + name, path + '/' + num + "/scr")  # move files
	    except:
		pass
	os.rmdir(csv_path)


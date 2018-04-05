#!/usr/bin/env python
import csv
import datetime as dt
from collections import OrderedDict
import subprocess
import sys

if len(sys.argv) != 4:
    print 'Error incorrect arguments.'
else:
    outfile = open(sys.argv[3], 'w')
    last_line = subprocess.check_output(["tail", "-1", sys.argv[1]]).split(',')[1:3]
    end_time = dt.datetime.strptime(str(last_line), "['%Y-%m-%d', '%H:%M:%S']")  # capture last time recorded in the log file.
    reader = csv.reader(open(sys.argv[1], 'rb'))
    next(reader)
    ongoing = OrderedDict()
    stamp = int(open(sys.argv[2], 'r').read())
    for counter, row in enumerate(reader):
        if counter == 0:
            current = dt.datetime.strptime(row[1] + row[2], '%Y-%m-%d%H:%M:%S') # record current time being scanned.
        if dt.datetime.strptime(row[1] + row[2], '%Y-%m-%d%H:%M:%S') == end_time:  # if last recorded time is reached.
            current = dt.datetime.strptime(row[1] + row[2], '%Y-%m-%d%H:%M:%S')
            if row[0] in ongoing: # if ip already exists
                ongoing[row[0]][2] += 1
                ongoing[row[0]][1] = current
            else: # else add new ip to dictionary
                ongoing[row[0]] = [current, current, 1]
            for rowl in reader: # process ips from here on as single time.
                if rowl[0] in ongoing: # if ip already exists
                    ongoing[rowl[0]][2] += 1
                    ongoing[rowl[0]][1] = current
                else: # else add new ip to dictionary
                    ongoing[rowl[0]] = [current, current, 1]
            for j in ongoing.keys(): # remove all ips from dictionary and display.
                outfile.write('%s,%s,%s,%d,%d\n' % (
                    j, ongoing[j][0], ongoing[j][1], int((ongoing[j][1] - ongoing[j][0]).total_seconds()) + 1,
                    ongoing[j][2]))
                ongoing.pop(j, None)
        if current == dt.datetime.strptime(row[1] + row[2], '%Y-%m-%d%H:%M:%S'): # if no change in time.
            if row[0] in ongoing: # if ip already exists
                ongoing[row[0]][2] += 1
                ongoing[row[0]][1] = current
            else: # else add new ip to dictionary
                ongoing[row[0]] = [current, current, 1]

        else: # if time changes.
            current = dt.datetime.strptime(row[1] + row[2], '%Y-%m-%d%H:%M:%S')
            if row[0] in ongoing: # if ip already exists
                ongoing[row[0]][2] += 1
                ongoing[row[0]][1] = current
            else: # else add new ip to dictionary
                ongoing[row[0]] = [current, current, 1]
            for j in ongoing.keys(): # check if inactivity period is reached by any ip.
                if j != row[0]:
                    if current - ongoing[j][1] >= dt.timedelta(seconds=stamp): # if inactivity reached remove ip from dictionary and write.
                        outfile.write('%s,%s,%s,%d,%d\n' % (
                            j, ongoing[j][0], ongoing[j][1],
                            int((ongoing[j][1] - ongoing[j][0]).total_seconds()) + 1,
                            ongoing[j][2]))
                        ongoing.pop(j, None)

    outfile.close()

# Approach
I have designed a simple approach using OrderedDictionary data structure in Python. The source code is provided with helpful comments explaining the algorithm designed. In this submission I also use datetime library to compute sessions for each ip address based on the inactivity period. 

The code is written clean with comments and requires no additional documentation to understand the logic. This program does not require any exotic library or any other dependencies except the default packages defined in Python. The code has been written for Python version 2.7.12. 

The algorithm has been tested for multiple testcases designed by varying number of lines in the log file and also changing the inactivity period, in addition to the default input test case given in the problem. The testcases were built using the EDGAR dataset: https://www.sec.gov/dera/data/edgar-log-file-data-set.html. The program performed well and handles large input as well (see testcases).

To execute the program the default instructions given in the problem works best:
#!/bin/bash
#
python ./src/sessionization.py ./input/log.csv ./input/inactivity_period.txt ./output/sessionization.txt

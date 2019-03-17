

#*************************************************************************
# Calculate second lowest cost silver plan (SLCSP)
# date: 12/31/18
# version: 0.4
# author: Lakshmi Narasimha vedantam (Dundi)
#
# required: three csv files
# output: results.csv
# see NOTES file for more info
#************************************************************************

import sys,os



#******************************************************************************
# readfile:
#  	utility function to read a file and create a dictionary
# 	filename	: file to be read
# 	skipfirstline	: skip header
#	keyindex	: which of the columns to be used for dictionary key
#	keepindex	: keep column index - used for skipping over data for 
#			  plans other than Silver
#	keepvalue	: keep only the rows that have this value
# 
#******************************************************************************

def readfile(filename, skipfirstline, keyindex, keepindex, keepvalue):
        dict={}
        with open(filename) as fp:
		if( skipfirstline == True):
			line = fp.readline()
                line = fp.readline()
                while line:
                        a = line.strip().split(',')
			if( keepindex >= 0 ):
				if ( a[keepindex] == keepvalue ):
					dict[a[keyindex]]=a
			else:
				dict[a[keyindex]] = a;
                       	line = fp.readline()
                return dict

#*******************************************************************************
# readfilearr:
#      utility function to read a file and create an array
#      filename        : file to be read
# 
#*******************************************************************************

def readfilearr(filename):
        with open(filename) as fp:
                arr = fp.readlines()
                return arr


#
# read the three files
#

zips = readfilearr('zips.csv');
plans = readfilearr('plans.csv') #, 0,2,"Silver");
slcsp = readfile('slcsp.csv', True, 0,-1,"");

#
# out dictionary keeps the second lowest rate values
# min dictionary keeps the lowest rate values
#
out = {}
min = {}

#
# For each value in the slcsp.csv file
#	get the match from the zips array
#	using state code and rate area, match the row from plans csv
#	if the matching rate is less than min value for the zip code, store it in min dictionary
#	else if the matching rate is less than out value for the zip code, store it in out dictionary
#	this ensures out dictionary contains only the second lowest rate
#
#
for silverplan in slcsp:
	for zipentry in zips:
		a = zipentry.split(',');
		if ( silverplan == a[0]):
			for plan in plans:
				b = plan.split(',');
				if ( b[2] == 'Silver' and b[1] == a[1] and b[4] == a[4]):
						if( min.get(a[0]) == None ):
							min[a[0]] = float(b[3])
						else:
							outval = out.get(a[0]);
							minval = min.get(a[0]);
							matchval = float(b[3]);
							if( matchval < minval ):
								min[a[0]] = matchval;
							elif ( outval == None or matchval < outval ):
								out[a[0]] = matchval;


#
# print output to stdout
# use os.linesep to avoid windows/linux cr/lf problems
#

f = open("results.csv", "w")
f.write( "zipcode,rate" + os.linesep)
with open("slcsp.csv") as fp:
	line = fp.readline()
	line = fp.readline()
        while line:
        	silverplan = line.strip().split(',')
		if out.get(silverplan[0]) == None:
			f.write(silverplan[0]+','+os.linesep);
		else:
			f.write(silverplan[0]+ ',' + '{0:.2f}'.format(out.get(silverplan[0]))+os.linesep)
		line = fp.readline()
fp.close()
f.close();
print "wrote to results.csv file"


# ******************************************************************************************
# unit tests:
# 1) for each zip code in the slcsp.csv file
#	grep zipcode zip.csv and get the state code and rate area
#	grep, awk and sort to see if the value for each zip code is indeed 
#	the 2nd lowest value:
#	cat plans.csv | grep WI | grep ,9 | grep Silver | awk -F, '{print $4}' | sort -n
# 2) verify the slcsp.csv and the results.csv files are in the same order and all the zip codes covered.
#	cat slcsp.csv | cut -f1 -d"," > /tmp/inputorder
#	cat results.csv | cut -f1 -d"," > /tmp/resultsorder
#	diff /tmp/inputorder /tmp/resultsorder
#

# ******************************************************************************************

#!/usr/bin/python

# download raw data file

import subprocess
import urllib2

# download latest copy, it's updated every 5 min

f = urllib2.urlopen("http://services.swpc.noaa.gov/text/aurora-nowcast-map.txt")
data = f.read()

with open("/tmp/aurora-nowcast-map.txt", "wb") as code:
    code.write(data)

# long and lat for Lulea
location = "Lulea"
lat = 22.15317360
lon = 65.58388960 

# count which col and row, row is offset by 17 lines because of help text
# also it starts on -90. 
x = int(round(lat / 0.32846715))
y = int(round((lon + 90) / 0.3515625 + 17))

aurora_value = int(subprocess.check_output( ["awk 'FNR == %i {print $%i}' /tmp/aurora-nowcast-map.txt" % (y, x)],shell=True ))

# display forcast, higher number is better
print "Location: " + location
print "Latitute: " + str(lat) + ", col: " + str(int(x))
print "Longitute: " + str(lon) + ", row: " + str(int(y))
print "Probability of Visible Aurora: %i percentage" % (aurora_value)

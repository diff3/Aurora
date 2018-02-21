#!/usr/bin/python

import subprocess
import urllib2
import ConfigParser
import sys
import getopt

Config = ConfigParser.ConfigParser()

aurora_url = ""
location = ""
lat = ""
lon = ""
save = ""
name = ""

if not location:
    location = "location"

def config( file ):
    global aurora_url
    global location
    global lat
    global lon
    global save
    global name

    Config.read( file )
    Config.read("config.ini")

    aurora_url = Config.get('aurora','url')
    save = Config.get('aurora','save_loc')
    name = Config.get( location,'name')
    lat = float(Config.get(location,'lat'))
    lon = float(Config.get(location,'lon'))

# download latest copy, it's updated every 5 min
# it's a 30 min forcast
def download_aurora( url_to_file ):
    global save

    f = urllib2.urlopen( url_to_file )
    data = f.read()

    with open( save, "wb") as code:
        code.write(data)

# all calculations
def count_percentage():
    global location
    global lat
    global lon
    global save
    global name

    print float(lat)
    # count which col and row, row is offset by 17 lines because of help text
    # also it starts on -90.
    x = int(round(lat / 0.32846715))
    y = int(round((lon + 90) / 0.3515625 + 17))

    aurora_value = int(subprocess.check_output( ["awk 'FNR == %i {print $%i}' %s" % (y, x, save)],shell=True ))

    # display forcast, higher number is better
    print "Location: " + name
    print "Latitute: " + str(lat) + ", col: " + str(int(x))
    print "Longitute: " + str(lon) + ", row: " + str(int(y))
    print "Probability of Visible Aurora: %i percentage" % (aurora_value)

def main(argv):
    global save

    config( "config.ini" )

#TODO Add special configs to lat lon location save url and help
    try:
        opts, args = getopt.getopt(argv,"hi:o:",["ifile=","ofile="])
    except getopt.GetoptError:
        print 'test.py -i <inputfile> -o <outputfile>'
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print 'test.py -i <inputfile> -o <outputfile>'
            sys.exit()
        elif opt in ("-i", "--ifile"):
            inputfile = arg
        elif opt in ("-o", "--ofile"):
            save = arg

    print ''

    download_aurora( aurora_url )
    count_percentage()

if __name__ == "__main__":
        main( sys.argv[1:] )

#!/usr/bin/python

import subprocess
import urllib2
import ConfigParser
import sys
import getopt

Config = ConfigParser.ConfigParser()

class aurora(object):
    """A class for calculation of aurora probability, it's a learn by doing project"""

    def __init__(self, file, location):
        """ Init config """

        self.location = location
        self.save_loc = ""
        self.save = ""
        self.name = ""
        self.lat = ""
        self.lon = ""
        self.url = ""
        self.aurora_value = ""
        self.x = ""
        self.y = ""
        self.file = file

        self.load_aurora_config(self.file, self.location)
        self.download_aurora_raw_data()
        self.calculate_aurora_probability()

    def download_aurora_raw_data(self):
        """ downloads 30 min forecast, it's updates every 5 minues """

        f = urllib2.urlopen( self.url )
        data = f.read()

        with open( self.save_loc, "wb") as code:
            code.write(data)

    def load_aurora_config(self,file, location):
        """ read and process config.ini file """

        Config.read( file )
        self.url = Config.get('aurora','url')
        self.save_loc = Config.get('aurora','save_loc')
        self.name = Config.get( location,'name')
        self.lat = float(Config.get(location,'lat'))
        self.lon = float(Config.get(location,'lon'))

    def calculate_aurora_probability(self):
        """ count which col and row, row is offset by 17 lines because of help text also it starts on -90. """

        self.x = int(round(self.lat / 0.32846715))
        self.y = int(round((self.lon + 90) / 0.3515625 + 17))

        self.aurora_value = int(subprocess.check_output( ["awk 'FNR == %i {print $%i}' %s" % (self.y, self.x, self.save_loc)],shell=True ))

    def print_result(self):
        """ display forcast, higher number is better """

        print "Location: " + self.name
        print "Latitute: " + str(self.lat) + ", col: " + str(int(self.x))
        print "Longitute: " + str(self.lon) + ", row: " + str(int(self.y))
        print "Probability of Visible Aurora: %i percentage" % (self.aurora_value)

def main(argv):

    try:
        opts, args = getopt.getopt(argv,"hil:o:",["ifile=","ofile=","location="])
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
        elif opt in ("-l", "--location"):
            location = arg

    print ''

    a = aurora("config.ini", "lulea")
    a.print_result()

if __name__ == "__main__":
    main( sys.argv[1:] )

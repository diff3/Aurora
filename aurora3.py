#!/usr/bin/python

import subprocess
import urllib2
import ConfigParser
import sys
import getopt

Config = ConfigParser.ConfigParser()

def load_aurora_config(file, location):
    Config.read( file )
    Config.read("config.ini")
    configure = dict()

    configure['url'] = Config.get('aurora','url')
    configure['save_loc'] = Config.get('aurora','save_loc')
    configure['name'] = Config.get( location,'name')
    configure['lat'] = float(Config.get(location,'lat'))
    configure['lon'] = float(Config.get(location,'lon'))

    return configure

def download_aurora_raw_data(url, save):
    # downloads 30 min forecast
    # it's updates every 5 minues

    f = urllib2.urlopen( url )
    data = f.read()

    with open( save, "wb") as code:
        code.write(data)

def calculate_aurora_probability( configure ):
    # count which col and row, row is offset by 17 lines because of help text
    # also it starts on -90.
    x = int(round(configure['lat'] / 0.32846715))
    y = int(round((configure['lon'] + 90) / 0.3515625 + 17))

    aurora_value = int(subprocess.check_output( ["awk 'FNR == %i {print $%i}' %s" % (y, x, configure['save_loc'])],shell=True ))

    # display forcast, higher number is better
    print "Location: " + configure['name']
    print "Latitute: " + str(configure['lat']) + ", col: " + str(int(x))
    print "Longitute: " + str(configure['lon']) + ", row: " + str(int(y))
    print "Probability of Visible Aurora: %i percentage" % (aurora_value)

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

    if not location:
        location = "default"

    configure = load_aurora_config( "config.ini", location)

    download_aurora_raw_data( configure['url'], configure['save_loc'] )
    calculate_aurora_probability( configure )

if __name__ == "__main__":
    main( sys.argv[1:] )

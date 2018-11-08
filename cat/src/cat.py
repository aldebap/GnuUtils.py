#!	/usr/bin/python

################################################################################
#	cat.py  -  Nov-08-2018 by aldebap
#
#	Python version of GNU Linux cat utility
################################################################################

import argparse
import sys

#	function to concatenate a file to standard output

def concatenateFile( _fileHandler ):

    while True:
        byte = _fileHandler.read( 1 )
        if '' == byte:
            break

        sys.stdout.write( byte )

#	entry point

if __name__ == '__main__':

    #	parse command line interface arguments
    parser = argparse.ArgumentParser( description='A Phyton implementation of GNU Linux cat utility' )

    parser.add_argument( dest='fileNames', nargs='*' )

    args = parser.parse_args()

    #   read the input file and concatenate to stdout
    if 0 == len( args.fileNames ):
        concatenateFile( sys.stdin )
    else:
        for fileName in args.fileNames:
            with open( fileName, 'r' ) as inputFile:
                concatenateFile( inputFile )
                inputFile.close()

#!	/usr/bin/python

################################################################################
#	cut.py  -  Nov-12-2018 by aldebap
#
#	Python version of GNU Linux cut utility
################################################################################

import argparse
import sys
import os.path

#   constants to options

#	function to cut lines from a file to standard output

def cutLines( _fileHandler, _options ):

    line = ''

    while True:
        byte = _fileHandler.read( 1 )
        if '' == byte:
            break

        if '\n' == byte:
            sys.stdout.write( line + '\n' )
            line = ''
            continue

        line = line + byte

#	entry point

def main():

    #	parse command line interface arguments
    parser = argparse.ArgumentParser( description='A Phyton implementation of GNU Linux cat utility' )

    parser.add_argument( '--version', dest='version', action='store_true', help='output version information and exit' )

    parser.add_argument( dest='fileNames', nargs='*' )

    args = parser.parse_args()

    if True == args.version:
        print 'This is free software: you are free to change and redistribute it.'
        print 'Written by Aldebaran Perseke (github.com/aldebap)'
        return

    #   read the input file and concatenate to stdout
    if 0 == len( args.fileNames ):
        concatenateFile( sys.stdin, options )
    else:
        for fileName in args.fileNames:
            if '-' == fileName:
                concatenateFile( sys.stdin, options )
            else:
                if os.path.isfile( fileName ):
                    with open( fileName, 'r' ) as inputFile:
                        concatenateFile( inputFile, options )
                        inputFile.close()
                else:
                    sys.stderr.write( parser.prog + ': ' + fileName + ': No such file or directory\n' )

#	entry point

if __name__ == '__main__':
    main()

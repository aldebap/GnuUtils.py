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

BYTES = 'bytes'

#	function to cut lines from a file to standard output

def cutLines( _fileHandler, _options ):

    line = ''

    while True:
        byte = _fileHandler.read( 1 )
        if '' == byte:
            break

        if '\n' == byte:
            if BYTES in _options:
                if len( line ) >= int( _options[ BYTES ] ):
                    sys.stdout.write( line[ int( _options[ BYTES ] ) - 1 ] + '\n' )
                else:
                    sys.stdout.write( '\n' )
            else:
                sys.stdout.write( line + '\n' )
            line = ''
            continue

        line = line + byte

#	entry point

def main():

    #	parse command line interface arguments
    parser = argparse.ArgumentParser( description='A Phyton implementation of GNU Linux cut utility' )

    parser.add_argument( '-b', '--bytes=', dest='bytes', action='store', help='select only these bytes' )
    parser.add_argument( '--version', dest='version', action='store_true', help='output version information and exit' )

    parser.add_argument( dest='fileNames', nargs='*' )

    args = parser.parse_args()

    if True == args.version:
        print 'This is free software: you are free to change and redistribute it.'
        print 'Written by Aldebaran Perseke (github.com/aldebap)'
        return

    #   set the options
    options = {}

    if 0 <= len( args.bytes ):
        options[ BYTES ] = args.bytes

    #   read the input file and cut lines to stdout
    if 0 == len( args.fileNames ):
        cutLines( sys.stdin, options )
    else:
        for fileName in args.fileNames:
            if '-' == fileName:
                cutLines( sys.stdin, options )
            else:
                if os.path.isfile( fileName ):
                    with open( fileName, 'r' ) as inputFile:
                        cutLines( inputFile, options )
                        inputFile.close()
                else:
                    sys.stderr.write( parser.prog + ': ' + fileName + ': No such file or directory\n' )

#	entry point

if __name__ == '__main__':
    main()

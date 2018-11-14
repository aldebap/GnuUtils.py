#!	/usr/bin/python

################################################################################
#	cut.py  -  Nov-12-2018 by aldebap
#
#	Python version of GNU Linux cut utility
################################################################################

import argparse
import os.path
import re
import sys

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
                for range in _options[ BYTES ]:
                    if 0 == range[ 1 ]:
                        sys.stdout.write( line[ range[ 0 ]: ] )
                    else:
                        sys.stdout.write( line[ range[ 0 ]:range[ 1 ] ] )
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
    parser.add_argument( '-n', dest='ignored', action='store_true', help='(ignored)' )
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
        #   TODO: check if there's only digits and hifens
        options[ BYTES ] = []
        for range in re.split( r',', args.bytes ):
            if not '-' in range:
                options[ BYTES ].append( [ int( range ) - 1, int( range ) ] )
            else:
            #   TODO: check if there's only one hifen
                if '-' == range[ 0 ]:
                    options[ BYTES ].append( [ 0, int( range[ 1: ] ) ] )
                else:
                    if '-' == range[ len( range ) - 1 ]:
                        options[ BYTES ].append( [ int( range[ :len( range ) -1 ] ) - 1, 0 ] )
                    else:
                        options[ BYTES ].append( [ int( range[ :range.index( '-' ) ] ) - 1, int( range[ range.index( '-' ) + 1: ] ) ] )
            #   TODO: check if there first index is lower than the second index
        sys.stderr.write( '[debug] bytes: ' + " ".join( map( str, options[ BYTES ] ) ) + '\n' )

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

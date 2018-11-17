#!	/usr/bin/python3

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
CHARACTERS = 'characters'
FIELDS = 'fields'
DELIMITER = 'delimiter'
OUTPUT_DELIMITER = 'outputDelimiter'

#	function to cut lines from a file to standard output

def cutLines( _fileHandler, _options ):

    line = ''

    while True:
        byte = _fileHandler.read( 1 )
        if '' == byte:
            #   if there's a last line without a LF, make it be processed
            if 0 == len( line ):
                break
            else:
                byte = '\n'

        if '\n' == byte:
            if BYTES in _options:
                for range in _options[ BYTES ]:
                    if 0 == range[ 1 ]:
                        sys.stdout.write( line[ range[ 0 ]: ] )
                    else:
                        sys.stdout.write( line[ range[ 0 ]:range[ 1 ] ] )
            elif CHARACTERS in _options:
                for range in _options[ CHARACTERS ]:
                    if 0 == range[ 1 ]:
                        sys.stdout.write( line[ range[ 0 ]: ] )
                    else:
                        sys.stdout.write( line[ range[ 0 ]:range[ 1 ] ] )
            elif FIELDS in _options:
                firstField = True
                fields = line.split( _options[ DELIMITER ] )
                for range in _options[ FIELDS ]:
                    cutFields = []
                    if 0 == range[ 1 ]:
                        cutFields = fields[ range[ 0 ]: ]
                    else:
                        cutFields = fields[ range[ 0 ]:range[ 1 ] ]

                    for field in cutFields:
                        if True == firstField:
                            sys.stdout.write( field )
                        else:
                            sys.stdout.write( _options[ OUTPUT_DELIMITER ] + field )
                        firstField = False
            else:
                sys.stdout.write( line )
            sys.stdout.write( '\n' )
            line = ''
            continue

        line = line + byte

#   parse an argument with a comma separated list of ranges

def parseRanges( _argsParse, _ranges ):

    rangeList = []

    for range in _ranges.split( ',' ):
        if not '-' in range:
            if not re.match( r'^\d+$', range ):
                _argsParse.error( 'invalid byte/character position "' + range + '"' )

            rangeList.append( [ int( range ) - 1, int( range ) ] )
        else:
            if not re.match( r'^\d*-\d+$', range ) and not re.match( r'^\d+-\d*$', range ):
                _argsParse.error( 'invalid byte/character range' )

            if '-' == range[ 0 ]:
                rangeList.append( [ 0, int( range[ 1: ] ) ] )
            else:
                if '-' == range[ len( range ) - 1 ]:
                    rangeList.append( [ int( range[ :len( range ) -1 ] ) - 1, 0 ] )
                else:
                    start = int( range[ :range.index( '-' ) ] ) - 1
                    end = int( range[ range.index( '-' ) + 1: ] )
                    if start > end:
                        _argsParse.error( 'invalid decreasing range' )

                    rangeList.append( [ start, end ] )

    return rangeList

#	entry point

def main():

    #	parse command line interface arguments
    parser = argparse.ArgumentParser( description='A Phyton implementation of GNU Linux cut utility' )

    parser.add_argument( '-b', '--bytes=', dest='bytes', action='store', help='select only these bytes' )
    parser.add_argument( '-c', '--characters=', dest='characters', action='store', help='select only these characters' )
    parser.add_argument( '-d', '--delimiter=', dest='delimiter', action='store', help='use DELIM instead of TAB for field delimiter' )
    parser.add_argument( '-f', '--fields=', dest='fields', action='store', help='select only these fields; also print any line that contains no delimiter character, unless the -s option is specified' )
    parser.add_argument( '-n', dest='ignored', action='store_true', help='(ignored)' )
    parser.add_argument( '--version', dest='version', action='store_true', help='output version information and exit' )

    parser.add_argument( dest='fileNames', nargs='*' )

    args = parser.parse_args()

    if True == args.version:
        sys.stdout.write( 'This is free software: you are free to change and redistribute it.' )
        sys.stdout.write( 'Written by Aldebaran Perseke (github.com/aldebap)' )
        return

    #   validate the options
    if args.bytes is None and args.characters is None and args.fields is None:
        parser.error( 'you must specify a list of bytes, characters, or fields' )

    if ( ( args.bytes is not None and args.characters is not None )
            or ( args.bytes is not None and args.fields is not None )
            or ( args.characters is not None and args.fields is not None ) ):
        parser.error( 'only one type of list may be specified' )

    if args.delimiter is not None and ( args.bytes is not None or args.characters is not None ):
        parser.error( 'an input delimiter may be specified only when operating on fields' )

    #   set the options
    options = {}

    if args.bytes is not None:
        options[ BYTES ] = parseRanges( parser, args.bytes )

    if args.characters is not None:
        options[ CHARACTERS ] = parseRanges( parser, args.characters )

    if args.fields is not None:
        options[ FIELDS ] = parseRanges( parser, args.fields )

    if args.delimiter is None:
        options[ DELIMITER ] = '\t'
    else:
        if 0 == len( args.delimiter ):
            parser.error( 'option requires an argument -- \'d\'' )
        elif 1 == len( args.delimiter ):
            options[ DELIMITER ] = args.delimiter
        else:
            parser.error( 'the delimiter must be a single character' )

    options[ OUTPUT_DELIMITER ] = options[ DELIMITER ]

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

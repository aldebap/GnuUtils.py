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
ONLY_DELIMITED = 'onlyDelimited'
OUTPUT_DELIMITER = 'outputDelimiter'
COMPLEMENT = 'complement'

#	function to cut lines from a file to standard output

def cutLines( _fileHandler, _options ):

    #   if cut fields option and an output delimiter is not set, make it the input delimiter
    if FIELDS in _options and OUTPUT_DELIMITER not in _options:
        _options[ OUTPUT_DELIMITER ] = _options[ DELIMITER ]

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
            result = ''

            #   cut selected bytes from the line
            if BYTES in _options:
                for range in _options[ BYTES ]:
                    if 0 == range[ 1 ]:
                        result = result + line[ range[ 0 ]: ]
                    else:
                        result = result + line[ range[ 0 ]:range[ 1 ] ]

            #   cut selected characters from the line
            elif CHARACTERS in _options:
                for range in _options[ CHARACTERS ]:
                    if 0 == range[ 1 ]:
                        result = result + line[ range[ 0 ]: ]
                    else:
                        result = result + line[ range[ 0 ]:range[ 1 ] ]

            #   cut selected fields from the line
            elif FIELDS in _options:
                if ONLY_DELIMITED in _options and -1 == line.find( _options[ DELIMITER ] ):
                    line = ''
                    continue

                fields = line.split( _options[ DELIMITER ] )
                for range in _options[ FIELDS ]:
                    cutFields = []
                    if 0 == range[ 1 ]:
                        cutFields = fields[ range[ 0 ]: ]
                    else:
                        cutFields = fields[ range[ 0 ]:range[ 1 ] ]

                    #   fields are separated by the output delimiter
                    for field in cutFields:
                        if 0 == len( result ):
                            result = field
                        else:
                            result = result + _options[ OUTPUT_DELIMITER ] + field

            #   if complement option wasn't chosen, print the result
            if COMPLEMENT not in _options:
                sys.stdout.write( result + '\n' )
            else:
                complementResult = ''

                #   complement result are all bytes in the line but those that were cut
                if BYTES in _options:
                    for byteAux in line:
                        if byteAux not in result:
                            complementResult = complementResult + byteAux

                #   complement result are all characters in the line but those that were cut
                elif CHARACTERS in _options:
                    for characterAux in line:
                        if characterAux not in result:
                            complementResult = complementResult + characterAux

                #   complement result are all fields in the line but those that were cut
                elif FIELDS in _options:
                    for field in line.split( _options[ DELIMITER ] ):
                        if -1 == result.find( field ):
                            if 0 == len( complementResult ):
                                complementResult = field
                            else:
                                complementResult = complementResult + _options[ OUTPUT_DELIMITER ] + field

                sys.stdout.write( complementResult + '\n' )

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
    parser.add_argument( '--complement', dest='complement', action='store_true', help='complement the set of selected bytes, characters or fields' )
    parser.add_argument( '-s', '--only-delimited', dest='onlyDelimited', action='store_true', help='complement the set of selected bytes, characters' )
    parser.add_argument( '--output-delimiter=', dest='outputDelimiter', action='store', help='use STRING as the output delimiter, the default is to use the input delimiter' )
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

    if True == args.onlyDelimited and ( args.bytes is not None or args.characters is not None ):
        parser.error( 'suppressing non-delimited lines makes sense only when operating on fields' )

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

    if True == args.complement:
        options[ COMPLEMENT ] = True

    if True == args.onlyDelimited:
        options[ ONLY_DELIMITED ] = True

    if args.outputDelimiter is not None:
        options[ OUTPUT_DELIMITER ] = args.outputDelimiter

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

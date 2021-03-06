#!	/usr/bin/python3

################################################################################
#	sort.py  -  Dec-10-2018 by aldebap
#
#	Python version of GNU Linux sort utility
################################################################################

import argparse
import os.path
import re
import sys

#   constants to options

IGNORE_LEADING_BLANKS = 'ignoreLeadingBlanks'
DICTIONARY_ORDER = 'dictionaryOrder'
IGNORE_CASE = 'ignoreCase'
REVERSE = 'reverse'

#	function to read lines from a file

def readFile( _fileHandler ):

    inputLines = []

    #   read the input file
    line = ''

    while True:
        byte = _fileHandler.read( 1 )
        if '' == byte:
            #   if there's a last line without a LF, make it be processed
            if 0 < len( line ):
                inputLines.append( line )
            break

        if '\n' == byte:
            inputLines.append( line )
            line = ''
            continue

        line = line + byte

    return inputLines

#	function to sort lines to standard output

def sortLines( _inputLines, _options ):

    #   sort the original input
    sortedLines = []
    dictionaryRegex = re.compile( '[^a-z^0-9]*' )

    for line in _inputLines:
        inserted = False

        addingLine = line
        if IGNORE_LEADING_BLANKS in _options:
            addingLine = addingLine.lstrip()
        if DICTIONARY_ORDER in _options:
            addingLine = dictionaryRegex.sub( '', addingLine )
        if IGNORE_CASE in _options:
            addingLine = addingLine.upper()

        if 0 < len( sortedLines ):
            for i in range( len( sortedLines ) ):
                comparingLine = sortedLines[ i ]
                if IGNORE_LEADING_BLANKS in _options:
                    comparingLine = comparingLine.lstrip()
                if DICTIONARY_ORDER in _options:
                    comparingLine = dictionaryRegex.sub( '', comparingLine )
                if IGNORE_CASE in _options:
                    comparingLine = comparingLine.upper()

                if comparingLine > addingLine:
                    sortedLines.insert( i, line )
                    inserted = True
                    break

        if False == inserted:
            sortedLines.append( line )

    #   print the ordered input
    lines = len( sortedLines )
    reverse = REVERSE in _options

    for i in range( lines ):
        if not reverse:
            sys.stdout.write( sortedLines[ i ] + '\n' )
        else:
            sys.stdout.write( sortedLines[ lines - i - 1 ] + '\n' )

#	entry point

def main():

    #	parse command line interface arguments
    parser = argparse.ArgumentParser( description='A Phyton implementation of GNU Linux sort utility' )

    parser.add_argument( '-b', '--ignore-leading-blanks', dest='ignoreLeadingBlanks', action='store_true', help='ignore leading blanks' )
    parser.add_argument( '-d', '--dictionary-order', dest='dictionaryOrder', action='store_true', help='consider only blanks and alphanumeric characters' )
    parser.add_argument( '-f', '--ignore-case', dest='ignoreCase', action='store_true', help='fold lower case to upper case characters' )
    parser.add_argument( '-w', '--reverse', dest='reverse', action='store_true', help='reverse the result of comparisons' )
    parser.add_argument( '--version', dest='version', action='store_true', help='output version information and exit' )

    parser.add_argument( dest='fileNames', nargs='*' )

    args = parser.parse_args()

    if True == args.version:
        sys.stdout.write( 'This is free software: you are free to change and redistribute it.\n' )
        sys.stdout.write( 'Written by Aldebaran Perseke (github.com/aldebap)\n' )
        return

    #   validate the options

    #   set the options
    options = {}

    if True == args.ignoreLeadingBlanks:
        options[ IGNORE_LEADING_BLANKS ] = True

    if True == args.dictionaryOrder:
        options[ DICTIONARY_ORDER ] = True

    if True == args.ignoreCase:
        options[ IGNORE_CASE ] = True

    if True == args.reverse:
        options[ REVERSE ] = True

    #   read the input file and cut lines to stdout
    inputLines = []

    if 0 == len( args.fileNames ):
        inputLines = readFile( sys.stdin )
    else:
        for fileName in args.fileNames:
            if '-' == fileName:
                inputLines = inputLines + readFile( sys.stdin )
            else:
                if os.path.isfile( fileName ):
                    with open( fileName, 'r' ) as inputFile:
                        inputLines = inputLines + readFile( inputFile )
                        inputFile.close()
                else:
                    sys.stderr.write( parser.prog + ': ' + fileName + ': No such file or directory\n' )

    sortLines( inputLines, options )

#	entry point

if __name__ == '__main__':
    main()

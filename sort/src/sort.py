#!	/usr/bin/python3

################################################################################
#	sort.py  -  Dec-10-2018 by aldebap
#
#	Python version of GNU Linux sort utility
################################################################################

import argparse
import os.path
import sys

#   constants to options

IGNORE_LEADING_BLANKS = 'ignoreLeadingBlanks'
IGNORE_CASE = 'ignoreCase'
REVERSE = 'reverse'

#	function to sort lines from a file to standard output

def sortFile( _fileHandler, _options ):

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

    #   sort the original input
    sortedLines = []

    for line in inputLines:
        inserted = False

        if 0 < len( sortedLines ):
            for i in range( len( sortedLines ) ):
                if sortedLines[ i ] > line:
                    sortedLines.insert( i, line )
                    inserted = True
                    break

        if False == inserted:
            sortedLines.append( line )

    #   print the ordered input
    for line in sortedLines:
        sys.stdout.write( line + '\n' )

#	entry point

def main():

    #	parse command line interface arguments
    parser = argparse.ArgumentParser( description='A Phyton implementation of GNU Linux sort utility' )

    parser.add_argument( '-b', '--ignore-leading-blanks', dest='ignoreLeadingBlanks', action='store_true', help='ignore leading blanks' )
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

    if True == args.ignoreCase:
        options[ IGNORE_CASE ] = True

    if True == args.reverse:
        options[ REVERSE ] = True

    #   read the input file and cut lines to stdout
    if 0 == len( args.fileNames ):
        sortFile( sys.stdin, options )
    else:
        for fileName in args.fileNames:
            if '-' == fileName:
                sortFile( sys.stdin, options )
            else:
                if os.path.isfile( fileName ):
                    with open( fileName, 'r' ) as inputFile:
                        sortFile( inputFile, options )
                        inputFile.close()
                else:
                    sys.stderr.write( parser.prog + ': ' + fileName + ': No such file or directory\n' )

#	entry point

if __name__ == '__main__':
    main()

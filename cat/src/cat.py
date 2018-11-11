#!	/usr/bin/python

################################################################################
#	cat.py  -  Nov-08-2018 by aldebap
#
#	Python version of GNU Linux cat utility
################################################################################

import argparse
import sys
import os.path

#   constants to options

SHOW_ENDS = 'showEnds'
SHOW_TABS = 'showTabs'
SHOW_NON_PRINTING = 'showNonPrinting'
NUMBER_NON_BLANK = 'numberNonBlank'
NUMBER = 'number'
SQUEEZE_BLANK = 'squeezeBlank'

#	function to concatenate a file to standard output

def concatenateFile( _fileHandler, _options ):

    line = ''
    lineNumber = 1
    previousLineBlank = False

    while True:
        byte = _fileHandler.read( 1 )
        if '' == byte:
            break

        if '\n' == byte:
            if '' == line and True == previousLineBlank and SQUEEZE_BLANK in _options:
                continue

            if '' == line:
                previousLineBlank = True
            else:
                previousLineBlank = False

            #   print a dollar sign in the end of a line
            if SHOW_ENDS in _options:
                line = line + '$'

            if NUMBER_NON_BLANK in _options:
                if '' == line or ( '$' == line and SHOW_ENDS in _options ):
                    sys.stdout.write( line + '\n' )
                else:
                    sys.stdout.write( format( lineNumber ) + ' ' + line + '\n' )
                    lineNumber = lineNumber + 1
            else:
                if NUMBER in _options:
                    sys.stdout.write( format( lineNumber ) + ' ' + line + '\n' )
                    lineNumber = lineNumber + 1
                else:
                    sys.stdout.write( line + '\n' )

            line = ''
            continue

        #   print a ^I instead of a TAB
        if '\t' == byte and SHOW_TABS in _options:
            line = line + '^I'
            continue

        #   the code bellow for non printing characters follows original cat source code (https://github.com/goj/coreutils/blob/rm-d/src/cat.c)
        if 32 > ord( byte ) and SHOW_NON_PRINTING in _options:
            line = line + '^I' + chr( ord( byte ) + ord( '@' ) )
            continue
        if 127 == ord( byte ) and SHOW_NON_PRINTING in _options:
            line = line + '^?'
            continue
        if 127 < ord( byte ) and SHOW_NON_PRINTING in _options:
            line = line + 'M-'
            if 128 + 32 <=  ord( byte ):
                if 128 + 127 > ord( byte ):
                    line = line + chr( ord( byte ) - 128 )
                else:
                    line = line + '^?'
            else:
                line = line + '^' + chr( ord( byte ) - 128 + 64 )
            continue

        line = line + byte

#	entry point

def main():

    #	parse command line interface arguments
    parser = argparse.ArgumentParser( description='A Phyton implementation of GNU Linux cat utility' )

    parser.add_argument( '-A', '--show-all', dest='comboAll', action='store_true', help='equivalent to -vET' )
    parser.add_argument( '-b', '--number-nonblank', dest='numberNonBlank', action='store_true', help='number nonempty output lines, overrides -n' )
    parser.add_argument( '-e', dest='combo1', action='store_true', help='equivalent to -vE' )
    parser.add_argument( '-E', '--show-ends', dest='showEnds', action='store_true', help='display $ at end of each line' )
    parser.add_argument( '-n', '--number', dest='number', action='store_true', help='number all output lines' )
    parser.add_argument( '-s', '--squeeze-blank', dest='squeezeBlank', action='store_true', help='suppress repeated empty output lines' )
    parser.add_argument( '-t', dest='combo2', action='store_true', help='equivalent to -vT' )
    parser.add_argument( '-T', '--show-tabs', dest='showTabs', action='store_true', help='display TAB characters as ^I' )
    parser.add_argument( '-u', dest='ignored', action='store_true', help='(ignored)' )
    parser.add_argument( '-v', '--show-nonprinting', dest='showNonPrinting', action='store_true', help='use ^ and M- notation, except for LFD and TAB' )
    parser.add_argument( '--version', dest='version', action='store_true', help='output version information and exit' )

    parser.add_argument( dest='fileNames', nargs='*' )

    args = parser.parse_args()

    if True == args.version:
        print 'This is free software: you are free to change and redistribute it.'
        print 'Written by Aldebaran Perseke (github.com/aldebap)'
        return

    #   set the options
    options = {}

    if True == args.comboAll or True == args.combo1 or True == args.showEnds:
        options[ SHOW_ENDS ] = True

    if True == args.comboAll or True == args.combo2 or True == args.showTabs:
        options[ SHOW_TABS ] = True

    if True == args.comboAll or True == args.combo1 or True == args.combo2 or True == args.showNonPrinting:
        options[ SHOW_NON_PRINTING ] = True

    if True == args.numberNonBlank:
        options[ NUMBER_NON_BLANK ] = True

    if True == args.number:
        options[ NUMBER ] = True

    if True == args.squeezeBlank:
        options[ SQUEEZE_BLANK ] = True

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

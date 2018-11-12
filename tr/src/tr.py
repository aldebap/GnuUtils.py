#!	/usr/bin/python

################################################################################
#	tr.py  -  nov-10-2018 by aldebap
#
#	Python version of GNU Linux tr utility
################################################################################

import argparse
import sys

#   constants to options

SET1 = 'set1'
SET2 = 'set2'
COMPLEMENT = 'complement'
SQUEEZE = 'squeeze'

#	function to translate characters from standard input

def translateFromFile( _options ):

    set1 = _options[ SET1 ]
    set2 = _options[ SET2 ]
    previousByte = ''

    while True:
        byte = sys.stdin.read( 1 )
        if '' == byte:
            break

        if not byte in set1:
            if not SQUEEZE in _options:
                sys.stdout.write( byte )
            else:
                if byte in set2 and byte != previousByte:
                    sys.stdout.write( byte )
        else:
            if set1.index( byte ) + 1 < len( set2 ):
                if not SQUEEZE in _options or byte != previousByte:
                    sys.stdout.write( set2[ set1.index( byte ) ] )
            else:
                if not SQUEEZE in _options or byte != previousByte:
                    sys.stdout.write( set2[ len( set2 ) - 1 ] )

        previousByte = byte

#	function to delete characters from standard input

def deleteFromFile( _options ):

    while True:
        byte = sys.stdin.read( 1 )
        if '' == byte:
            break

        if not byte in _options[ SET1 ]:
            sys.stdout.write( byte )

#	entry point

def main():

    #	parse command line interface arguments
    parser = argparse.ArgumentParser( description='A Phyton implementation of GNU Linux tr utility' )

    parser.add_argument( '-c', '--complement', dest='complement', action='store_true', help='use the complement of SET1' )
    parser.add_argument( '-d', '--delete', dest='delete', action='store_true', help='delete characters in SET1, do not translate' )
    parser.add_argument( '-t', '--truncate-set1', dest='truncate', action='store_true', help='first truncate SET1 to length of SET2' )
    parser.add_argument( '-s', '--squeeze-repeats', dest='squeeze', action='store_true', help='replace each sequence of a repeated character that is listed in the last specified SET, with a single occurrence of that character' )

    parser.add_argument( dest='sets', nargs='*' )

    args = parser.parse_args()

    #   set the options
    options = {}

    if 0 >= len( args.sets ):
        parser.error( 'tr: missing operand' )
    else:
        options[ SET1 ] = args.sets[ 0 ]

        if 2 == len( args.sets ):
            options[ SET2 ] = args.sets[ 1 ]
        else:
            if 2 < len( args.sets ):
                parser.error( 'tr: extra  operand "' + args.sets[ 2 ] + '"' )

    if True == args.complement:
        options[ COMPLEMENT ] = True

    if True == args.squeeze:
        options[ SQUEEZE ] = True

    #   check for the required sets

    if True == args.delete and SET2 in options:
        parser.error( 'tr: extra  operand "' + options[ SET2 ] + '"' )

    if False == args.delete and not SET2 in options:
        parser.error( 'tr: missing  operand after "' + options[ SET1 ] + '"\nTwo strings must be given when translating.' )

    #   read the standard input and perform one of possible operations

    if True == args.delete:
        deleteFromFile( options )
    else:
        translateFromFile( options )

#	entry point

if __name__ == '__main__':
    main()

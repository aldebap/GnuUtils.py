#!	/usr/bin/python

################################################################################
#	tr.py  -  nov-10-2018 by aldebap
#
#	Python version of GNU Linux tr utility
################################################################################

import argparse
import sys

#   global options

complement = False

#	function to translate characters from standard input

def translateFromFile( _set1, _set2 ):

    while True:
        byte = sys.stdin.read( 1 )
        if '' == byte:
            break

        if not byte in _set1:
            sys.stdout.write( byte )
        else:
            if _set1.index( byte ) + 1 < len( _set2 ):
                sys.stdout.write( _set2[ _set1.index( byte ) ] )
            else:
                sys.stdout.write( _set2[ len( _set2 ) - 1 ] )

#	function to delete characters from standard input

def deleteFromFile( _set1 ):

    while True:
        byte = sys.stdin.read( 1 )
        if '' == byte:
            break

        if not byte in _set1:
            sys.stdout.write( byte )

#	entry point

def main():

    #	parse command line interface arguments
    parser = argparse.ArgumentParser( description='A Phyton implementation of GNU Linux tr utility' )

    parser.add_argument( '-c', '--complement', dest='complement', action='store_true', help='use the complement of SET1' )
    parser.add_argument( '-d', '--delete', dest='delete', action='store_true', help='delete characters in SET1, do not translate' )
    parser.add_argument( '-t', '--truncate-set1', dest='truncate', action='store_true', help='first truncate SET1 to length of SET2' )

    parser.add_argument( dest='sets', nargs='*' )

    args = parser.parse_args()

    #   set the global options
    if True == args.complement:
        complement = True

    #   check for the required sets

    if 1 > len( args.sets ):
        parser.error( 'tr: missing operand' )

    if True == args.delete and 1 != len( args.sets ):
        parser.error( 'tr: extra  operand "' + args.sets[ 1 ] + '"' )

    if False == args.delete and 2 > len( args.sets ):
        parser.error( 'tr: missing  operand after "' + args.sets[ 0 ] + '"\nTwo strings must be given when translating.' )

    if False == args.delete and 2 < len( args.sets ):
        parser.error( 'tr: extra  operand "' + args.sets[ 1 ] + '"' )

    #   read the standard input and perform one of possible operations

    if True == args.delete:
        deleteFromFile( args.sets[ 0 ] )
    else:
        translateFromFile( args.sets[ 0 ], args.sets[ 1 ] )
#	entry point

if __name__ == '__main__':
    main()

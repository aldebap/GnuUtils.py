#!	/usr/bin/python

################################################################################
#	wc.py  -  Oct-31-2018 by aldebap
#
#	Python version of Linux wc utility
################################################################################

import  argparse

#	entry point

if( __name__ == '__main__' ):

    #	parse command line interface arguments
    parser = argparse.ArgumentParser( description = 'A Phyton implementation of Linux wc utility' )

    parser.add_argument( '-c', '--bytes', dest='bytes', action='store_true', help='print the byte counts' )
    parser.add_argument( '-m', '--chars', dest='chars', action='store_true', help='print the character counts' )
    parser.add_argument( '-l', '--lines', dest='lines', action='store_true', help='print the newline counts' )
    parser.add_argument( '-w', '--words', dest='words', action='store_true', help='print the word counts' )

    args = parser.parse_args()

    #   read the input file and make the summarizations
    with open( 'somefile.txt', 'r' ) as inputFile:
        for line in inputFile:

    print '[WebServer] Starting the Web Server'

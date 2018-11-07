#!	/usr/bin/python

################################################################################
#	wc.py  -  Oct-31-2018 by aldebap
#
#	Python version of Linux wc utility
################################################################################

import argparse

#	function to make count on input file


def countFromFile(_fileHandler):
    byteCount = 0
    lineCount = 0

    while True:
        byte = _fileHandler.read(1)
        if '' == byte:
            break

        byteCount = byteCount + 1
        if '\n' == byte:
            lineCount = lineCount + 1

    print format(lineCount) + ' ' + format(byteCount)


#	entry point

if(__name__ == '__main__'):

    #	parse command line interface arguments
    parser = argparse.ArgumentParser(
        description='A Phyton implementation of Linux wc utility')

    parser.add_argument('-c', '--bytes', dest='bytes',
                        action='store_true', help='print the byte counts')
    parser.add_argument('-m', '--chars', dest='chars',
                        action='store_true', help='print the character counts')
    parser.add_argument('-l', '--lines', dest='lines',
                        action='store_true', help='print the newline counts')
    parser.add_argument('-w', '--words', dest='words',
                        action='store_true', help='print the word counts')

    args = parser.parse_args()

    #   read the input file and make the summarizations
    with open('/home/aldeba/.bashrc', 'r') as inputFile:
        countFromFile(inputFile)
        inputFile.close()
        print ' FileName\n'

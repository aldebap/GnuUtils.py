#!	/usr/bin/python

################################################################################
#	wc.py  -  Oct-31-2018 by aldebap
#
#	Python version of Linux wc utility
################################################################################

import argparse

#	function to make count on input file


def countFromFile(_fileHandler, _fileName):
    byteCount = 0
    wordCount = 0
    lineCount = 0
    token = False

    while True:
        byte = _fileHandler.read(1)
        if '' == byte:
            break

        byteCount = byteCount + 1
        if ' ' == byte or '\t' == byte or '\n' == byte:
            if True == token:
                wordCount = wordCount + 1
            token = False
        else:
            token = True

        if '\n' == byte:
            lineCount = lineCount + 1

    if '' == _fileName:
        print format(lineCount) + ' ' + format(wordCount) + \
            ' ' + format(byteCount)
    else:
        print format(lineCount) + ' ' + format(wordCount) + \
            ' ' + format(byteCount) + ' ' + _fileName


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

    parser.add_argument(dest='fileNames', nargs='*')

    args = parser.parse_args()

    #   read the input file and make the summarizations
    if 0 == len(args.fileNames):
        countFromFile(StandardError, '')
    else:
        for fileName in args.fileNames:
            with open(fileName, 'r') as inputFile:
                countFromFile(inputFile, fileName)
                inputFile.close()

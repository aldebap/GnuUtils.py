#!	/usr/bin/python

################################################################################
#	wc.py  -  Oct-31-2018 by aldebap
#
#	Python version of GNU Linux wc utility
################################################################################

import argparse
import sys

#   global options

showByteCount = False
showWordCount = False
showLineCount = False

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

    result = ' '
    if True == showLineCount:
        result = result + format(lineCount) + ' '
    if True == showWordCount:
        result = result + format(wordCount) + ' '
    if True == showByteCount:
        result = result + format(byteCount) + ' '

    if '' == _fileName:
        print result
    else:
        print result + _fileName


#	entry point

if(__name__ == '__main__'):

    #	parse command line interface arguments
    parser = argparse.ArgumentParser( description='A Phyton implementation of GNU Linux wc utility')

    parser.add_argument('-c', '--bytes', dest='bytes', action='store_true', help='print the byte counts')
    parser.add_argument('-m', '--chars', dest='chars', action='store_true', help='print the character counts')
    parser.add_argument('-l', '--lines', dest='lines', action='store_true', help='print the newline counts')
    parser.add_argument('-w', '--words', dest='words', action='store_true', help='print the word counts')

    parser.add_argument(dest='fileNames', nargs='*')

    args = parser.parse_args()

    #   set the global options
    if True == args.bytes:
        showByteCount = True
    if True == args.words:
        showWordCount = True
    if True == args.lines:
        showLineCount = True

    if False == showByteCount and False == showWordCount and False == showLineCount:
        showByteCount = True
        showWordCount = True
        showLineCount = True

    #   read the input file and make the summarizations
    if 0 == len(args.fileNames):
        countFromFile(sys.stdin, '')
    else:
        for fileName in args.fileNames:
            with open(fileName, 'r') as inputFile:
                countFromFile(inputFile, fileName)
                inputFile.close()

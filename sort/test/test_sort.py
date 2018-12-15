#!	/usr/bin/python3

################################################################################
#	test_sort.py  -  Dec-11-2018 by aldebap
#
#	Unit tests for the Python version of GNU Linux sort utility
################################################################################

from io import StringIO
from unittest.mock import patch
import unittest
import os
import sys
import tempfile

import sort

#   Unit tests class

class test_sort( unittest.TestCase ):

    #   sort.readFile() function tests

    #   test readFile - 01. read standard input
    def test_readFile_stdin( self ):

        inputLines = []

        with patch( 'sys.stdin', new=StringIO( 'def\nabc\njkl\nghi' ) ) as mockStdin:
            inputLines = sort.readFile( sys.stdin )

        self.assertTrue( [ 'def', 'abc', 'jkl', 'ghi' ] == inputLines )

    #   test readFile - 02. read a single file
    def test_readFile_temporaryFile( self ):

        contentFile = tempfile.NamedTemporaryFile( delete=False )
        contentFile.write( b'def\nabc\njkl\nghi' )
        contentFile.close()

        with open( contentFile.name, 'r' ) as inputFile:
            inputLines = sort.readFile( inputFile )
            inputFile.close()

        self.assertTrue( [ 'def', 'abc', 'jkl', 'ghi' ] == inputLines )

    #   sort.sortLines() function tests

    #   test sortLines - 01. sort without options
    def test_sortLines_noOptions( self ):

        with patch( 'sys.stdout', new=StringIO() ) as mockStdout:
            inputLines = [ 'def', 'abc', 'jkl', 'ghi' ]
            options = {}

            sort.sortLines( inputLines, options )

        self.assertTrue( 'abc\ndef\nghi\njkl\n' == mockStdout.getvalue() )

    #   test main - 02. sort with leading blanks
    def test_sortLines_withLeadingBlanks( self ):

        with patch( 'sys.stdout', new=StringIO() ) as mockStdout:
            inputLines = [ ' def', '  abc', '   jkl', '    ghi' ]
            options = {}

            sort.sortLines( inputLines, options )

        self.assertTrue( '    ghi\n   jkl\n  abc\n def\n' == mockStdout.getvalue() )

    #   test sortLines - 03. sort ignore leading blanks
    def test_sortLines_ignoreLeadingBlanks( self ):

        with patch( 'sys.stdout', new=StringIO() ) as mockStdout:
            inputLines = [ ' def', '  abc', '   jkl', '    ghi' ]
            options = { 'ignoreLeadingBlanks': True }

            sort.sortLines( inputLines, options )

        self.assertTrue( '  abc\n def\n    ghi\n   jkl\n' == mockStdout.getvalue() )

    #   test main - 04. sort with case differences
    def test_sortLines_withCaseDifferences( self ):

        with patch( 'sys.stdout', new=StringIO() ) as mockStdout:
            inputLines = [ 'DEF', 'abc', 'JKL', 'ghi' ]
            options = {}

            sort.sortLines( inputLines, options )

        self.assertTrue( 'DEF\nJKL\nabc\nghi\n' == mockStdout.getvalue() )

    #   test sortLines - 05. sort ignore case
    def test_sortLines_ignoreCase( self ):

        with patch( 'sys.stdout', new=StringIO() ) as mockStdout:
            inputLines = [ 'DEF', 'abc', 'JKL', 'ghi' ]
            options = { 'ignoreCase': True }

            sort.sortLines( inputLines, options )

        self.assertTrue( 'abc\nDEF\nghi\nJKL\n' == mockStdout.getvalue() )

    #   test sortLines - 06. sort in the reverse order
    def test_sortLines_reverse( self ):

        with patch( 'sys.stdout', new=StringIO() ) as mockStdout:
            inputLines = [ 'def', 'abc', 'jkl', 'ghi' ]
            options = { 'reverse': True }

            sort.sortLines( inputLines, options )

#        sys.stderr.write( '[debug] result: \'' + mockStdout.getvalue() + '\'\n' )
        self.assertTrue( 'jkl\nghi\ndef\nabc\n' == mockStdout.getvalue() )

    #   sort.main() function tests

    #   test main - 01. check for no required options
    def test_main_withoutOptions( self ):

        with patch( 'sys.stdout', new=StringIO() ) as mockStdout:
            with patch( 'sys.stdin', new=StringIO( 'def\nabc\njkl\nghi' ) ) as mockStdin:
                sys.argv = [ 'sort' ]
                sort.main()

        self.assertTrue( 'abc\ndef\nghi\njkl\n' == mockStdout.getvalue() )

    #   test main - 02. check for version options
    def test_main_versionOption( self ):

        with patch( 'sys.stdout', new=StringIO() ) as mockStdout:
            sys.argv = [ 'sort', '--version' ]
            sort.main()

        self.assertTrue( -1 != mockStdout.getvalue().find( 'Written by Aldebaran Perseke' ) )

    #   test main - 03. check for invalid option only
    def test_main_invalidOptionOnly( self ):

        with patch( 'sys.stderr', new=StringIO() ) as mockStderr:
            with self.assertRaises( SystemExit ) as exit:
                sys.argv = [ 'sort', '-a' ]
                sort.main()

        self.assertEqual( exit.exception.code, 2 )
        self.assertTrue( -1 != mockStderr.getvalue().find( 'unrecognized arguments: -a' ) )

    #   test main - 04. check for invalid option
    def test_main_invalidOption( self ):

        with patch( 'sys.stderr', new=StringIO() ) as mockStderr:
            with self.assertRaises( SystemExit ) as exit:
                sys.argv = [ 'sort', '-a', '--reverse' ]
                sort.main()

        self.assertEqual( exit.exception.code, 2 )
        self.assertTrue( -1 != mockStderr.getvalue().find( 'unrecognized arguments: -a' ) )

    #   TODO: are there some tests in between ??

    #   test main - 22. check for no file names
    def test_main_noFileNames( self ):

        with patch( 'sys.stdout', new=StringIO() ) as mockStdout:
            with patch( 'sys.stdin', new=StringIO( 'def\nabc\njkl\nghi' ) ) as mockStdin:
                sys.argv = [ 'sort' ]
                sort.main()

        self.assertTrue( 'abc\ndef\nghi\njkl\n' == mockStdout.getvalue() )

    #   test main - 23. check for hifen as file name
    def test_main_hifenAsFileNames( self ):

        with patch( 'sys.stdout', new=StringIO() ) as mockStdout:
            with patch( 'sys.stdin', new=StringIO( 'def\njkl\nabc\nmno\nxyz\nghi' ) ) as mockStdin:
                sys.argv = [ 'sort', '-' ]
                sort.main()

        self.assertTrue( 'abc\ndef\nghi\njkl\nmno\nxyz\n' == mockStdout.getvalue() )

    #   test main - 24. check for file not found
    def test_main_invalidFileName( self ):

        #   remember, a temporary file is removed after it's closed
        invalidFile = tempfile.NamedTemporaryFile()
        invalidFileName = invalidFile.name
        invalidFile.write( b'abcdef\nghijklm\nnopqrs\ntuvwxyz' )
        invalidFile.close()

        with patch( 'sys.stderr', new=StringIO() ) as mockStderr:
            sys.argv = [ 'sort', invalidFileName ]
            sort.main()

        self.assertTrue( -1 != mockStderr.getvalue().find( 'No such file or directory' ) )

    #   test main - 25. check for single file name
    def test_main_singleFileName( self ):

        contentFile = tempfile.NamedTemporaryFile( delete=False )
        contentFile.write( b'def\njkl\nabc\nmno\nxyz\nghi' )
        contentFile.close()

        with patch( 'sys.stdout', new=StringIO() ) as mockStdout:
            sys.argv = [ 'sort', contentFile.name ]
            sort.main()

        self.assertTrue( 'abc\ndef\nghi\njkl\nmno\nxyz\n' == mockStdout.getvalue() )
        os.remove( contentFile.name )

    #   test main - 26. check for multiple file names
    def test_main_multipleFileNames( self ):

        firstContentFile = tempfile.NamedTemporaryFile( delete=False )
        firstContentFile.write( b'stuvwxyz\nmnopqr\n' )
        firstContentFile.close()

        secondContentFile = tempfile.NamedTemporaryFile( delete=False )
        secondContentFile.write( b'abcdef\nghijkl\n' )
        secondContentFile.close()

        with patch( 'sys.stdout', new=StringIO() ) as mockStdout:
            sys.argv = [ 'sort', firstContentFile.name, secondContentFile.name ]
            sort.main()

        self.assertTrue( 'abcdef\nghijkl\nmnopqr\nstuvwxyz\n' == mockStdout.getvalue() )
        os.remove( firstContentFile.name )
        os.remove( secondContentFile.name )

    #   test main - 27. check for multiple file names, one as hifen
    def test_main_singleFileNameAndHifen( self ):

        contentFile = tempfile.NamedTemporaryFile( delete=False )
        contentFile.write( b'stuvwxyz\nmnopqr\n' )
        contentFile.close()

        with patch( 'sys.stdout', new=StringIO() ) as mockStdout:
            with patch( 'sys.stdin', new=StringIO( 'abcdef\nghijkl\n' ) ) as mockStdin:
                sys.argv = [ 'sort', contentFile.name, '-' ]
                sort.main()

        self.assertTrue( 'abcdef\nghijkl\nmnopqr\nstuvwxyz\n' == mockStdout.getvalue() )
        os.remove( contentFile.name )

    #   test main - 28. check for no file names and ignore leading blanks option
    def test_main_stdin_ignoreLeadingBlanks( self ):

        with patch( 'sys.stdout', new=StringIO() ) as mockStdout:
            with patch( 'sys.stdin', new=StringIO( ' def\n  abc\n   jkl\n    ghi' ) ) as mockStdin:
                sys.argv = [ 'sort', '--ignore-leading-blanks' ]
                sort.main()

        self.assertTrue( '  abc\n def\n    ghi\n   jkl\n' == mockStdout.getvalue() )

    #   test main - 29. check for no file names and ignore case option
    def test_main_stdin_ignoreCase( self ):

        with patch( 'sys.stdout', new=StringIO() ) as mockStdout:
            with patch( 'sys.stdin', new=StringIO( 'DEF\nabc\nJKL\nghi' ) ) as mockStdin:
                sys.argv = [ 'sort', '--ignore-case' ]
                sort.main()

        self.assertTrue( 'abc\nDEF\nghi\nJKL\n' == mockStdout.getvalue() )

    #   test main - 30. check for no file names and reverse the order
    def test_main_stdin_reverse( self ):

        with patch( 'sys.stdout', new=StringIO() ) as mockStdout:
            with patch( 'sys.stdin', new=StringIO( 'def\nabc\njkl\nghi' ) ) as mockStdin:
                sys.argv = [ 'sort', '--reverse' ]
                sort.main()

        self.assertTrue( 'jkl\nghi\ndef\nabc\n' == mockStdout.getvalue() )

#	entry point

if __name__ == '__main__':
    unittest.main()

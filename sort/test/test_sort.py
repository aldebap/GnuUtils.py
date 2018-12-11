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

class test_cut( unittest.TestCase ):

    #   cut.sortFile() function tests

    #   test sortFile - 01. sort without options
    def test_sortFile_noOptions( self ):

        with patch( 'sys.stdout', new=StringIO() ) as mockStdout:
            inputFile = StringIO( 'abcdef\nghijklm\n' )
            options = {}

            sort.sortFile( inputFile, options )

        self.assertTrue( 'abcdef\nghijklm\n' == mockStdout.getvalue() )

    #   cut.main() function tests

    #   test main - 01. check for no required options
    def test_main_withoutOptions( self ):

        with patch( 'sys.stderr', new=StringIO() ) as mockStderr:
            with self.assertRaises( SystemExit ) as exit:
                sys.argv = [ 'sort' ]
                sort.main()

        self.assertEqual( exit.exception.code, 2 )
        self.assertTrue( -1 != mockStderr.getvalue().find( 'you must specify a list of bytes, characters, or fields' ) )

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

    #   TODO: there are some tests in between

    #   test main - 22. check for no file names
    def test_main_noFileNames( self ):

        with patch( 'sys.stdout', new=StringIO() ) as mockStdout:
            with patch( 'sys.stdin', new=StringIO( 'abcdef\nghijklm\nnopqrs\ntuvwxyz' ) ) as mockStdin:
                sys.argv = [ 'cut', '--bytes=2-3,6' ]
                sort.main()

        self.assertTrue( 'bcf\nhil\nops\nuvy\n' == mockStdout.getvalue() )

    #   test main - 23. check for hifen as file name
    def test_main_hifenAsFileNames( self ):

        with patch( 'sys.stdout', new=StringIO() ) as mockStdout:
            with patch( 'sys.stdin', new=StringIO( 'abcdef\nghijklm\nnopqrs\ntuvwxyz' ) ) as mockStdin:
                sys.argv = [ 'cut', '--characters=2-3,6', '-' ]
                sort.main()

        self.assertTrue( 'bcf\nhil\nops\nuvy\n' == mockStdout.getvalue() )

    #   test main - 24. check for file not found
    def test_main_invalidFileName( self ):

        #   remember, a temporary file is removed after it's closed
        invalidFile = tempfile.NamedTemporaryFile()
        invalidFileName = invalidFile.name
        invalidFile.write( b'abcdef\nghijklm\nnopqrs\ntuvwxyz' )
        invalidFile.close()

        with patch( 'sys.stderr', new=StringIO() ) as mockStderr:
            sys.argv = [ 'cut', '--characters=2-3,6', invalidFileName ]
            sort.main()

        self.assertTrue( -1 != mockStderr.getvalue().find( 'No such file or directory' ) )

    #   test main - 25. check for single file name
    def test_main_singleFileName( self ):

        contentFile = tempfile.NamedTemporaryFile( delete=False )
        contentFile.write( b'abc;def;ghi;jkl\nmno;pqr;stu;vwx;yz\n' )
        contentFile.close()

        with patch( 'sys.stdout', new=StringIO() ) as mockStdout:
            sys.argv = [ 'cut', '--fields=1,3-4', '--delimiter=;', contentFile.name ]
            sort.main()

        self.assertTrue( 'abc;ghi;jkl\nmno;stu;vwx\n' == mockStdout.getvalue() )
        os.remove( contentFile.name )

    #   test main - 26. check for multiple file names
    def test_main_multipleFileNames( self ):

        firstContentFile = tempfile.NamedTemporaryFile( delete=False )
        firstContentFile.write( b'abcdef\nghijkl\n' )
        firstContentFile.close()

        secondContentFile = tempfile.NamedTemporaryFile( delete=False )
        secondContentFile.write( b'mnopqr\nstuvwxyz\n' )
        secondContentFile.close()

        with patch( 'sys.stdout', new=StringIO() ) as mockStdout:
            sys.argv = [ 'cut', '--bytes=1,3-4', firstContentFile.name, secondContentFile.name ]
            sort.main()

        self.assertTrue( 'acd\ngij\nmop\nsuv\n' == mockStdout.getvalue() )
        os.remove( firstContentFile.name )
        os.remove( secondContentFile.name )

    #   test main - 27. check for multiple file names, one as hifen
    def test_main_singleFileNameAndHifen( self ):

        contentFile = tempfile.NamedTemporaryFile( delete=False )
        contentFile.write( b'abcdef\nghijkl\n' )
        contentFile.close()

        with patch( 'sys.stdout', new=StringIO() ) as mockStdout:
            with patch( 'sys.stdin', new=StringIO( 'mnopqr\nstuvwxyz\n' ) ) as mockStdin:
                sys.argv = [ 'cut', '--characters=1,3,5-6', contentFile.name, '-' ]
                sort.main()

        #   sys.stderr.write( '[debug] result: \'' + mockStdout.getvalue() + '\'\n' )
        self.assertTrue( 'acef\ngikl\nmoqr\nsuwx\n' == mockStdout.getvalue() )
        os.remove( contentFile.name )

#	entry point

if __name__ == '__main__':
    unittest.main()

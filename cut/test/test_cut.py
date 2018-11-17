#!	/usr/bin/python3

################################################################################
#	test_cut.py  -  Nov-15-2018 by aldebap
#
#	Unit tests for the Python version of GNU Linux cut utility
################################################################################

from io import StringIO
from unittest.mock import patch
import unittest
import sys

import cut

#   Unit tests class

class test_cut( unittest.TestCase ):

    #   cut.cutLine() function tests

    #   test cutLines - 01. cut a single line and column
    def test_cutLine_bytesSingleLineAndColumn01( self ):

        with patch( 'sys.stdout', new=StringIO() ) as mockStdout:
            inputFile = StringIO( 'abcdefghijklm\n' )
            options = { 'bytes': [ [ 3, 4 ] ] }

            cut.cutLines( inputFile, options )

        self.assertTrue( 'd\n' == mockStdout.getvalue() )

    #   test cutLines - 02. cut a single line (no LF) and column
    def test_cutLine_bytesSingleLineAndColumn02( self ):

        with patch( 'sys.stdout', new=StringIO() ) as mockStdout:
            inputFile = StringIO( 'abcdefghijklm' )
            options = { 'bytes': [ [ 3, 4 ] ] }

            cut.cutLines( inputFile, options )

        self.assertTrue( 'd\n' == mockStdout.getvalue() )

    #   test cutLines - 03. cut multiple lines and a single column
    def test_cutLine_bytesMultipleLinesAndSingleColumn01( self ):

        with patch( 'sys.stdout', new=StringIO() ) as mockStdout:
            inputFile = StringIO( 'abcdef\nghijklm\nnopqrs\ntuvwxyz\n' )
            options = { 'bytes': [ [ 3, 4 ] ] }

            cut.cutLines( inputFile, options )

        self.assertTrue( 'd\nj\nq\nw\n' == mockStdout.getvalue() )

    #   test cutLines - 04. cut multiple lines (no LF at the end) and a single column
    def test_cutLine_bytesMultipleLinesAndSingleColumn02( self ):

        with patch( 'sys.stdout', new=StringIO() ) as mockStdout:
            inputFile = StringIO( 'abcdef\nghijklm\nnopqrs\ntuvwxyz' )
            options = { 'bytes': [ [ 3, 4 ] ] }

            cut.cutLines( inputFile, options )

        self.assertTrue( 'd\nj\nq\nw\n' == mockStdout.getvalue() )

    #   test cutLines - 05. cut a single line and a range of colums starting from begin
    def test_cutLine_bytesSingleLineAndRangeFromBegin01( self ):

        with patch( 'sys.stdout', new=StringIO() ) as mockStdout:
            inputFile = StringIO( 'abcdefghijklm\n' )
            options = { 'bytes': [ [ 0, 4 ] ] }

            cut.cutLines( inputFile, options )

        self.assertTrue( 'abcd\n' == mockStdout.getvalue() )

    #   test cutLines - 06. cut a single line (no LF) and a range of colums starting from begin
    def test_cutLine_bytesSingleLineAndRangeFromBegin02( self ):

        with patch( 'sys.stdout', new=StringIO() ) as mockStdout:
            inputFile = StringIO( 'abcdefghijklm' )
            options = { 'bytes': [ [ 0, 4 ] ] }

            cut.cutLines( inputFile, options )

        self.assertTrue( 'abcd\n' == mockStdout.getvalue() )

    #   test cutLines - 07. cut multiple lines and a range of colums starting from begin
    def test_cutLine_bytesMultipleLinesAndRangeFromBegin01( self ):

        with patch( 'sys.stdout', new=StringIO() ) as mockStdout:
            inputFile = StringIO( 'abcdef\nghijklm\nnopqrs\ntuvwxyz\n' )
            options = { 'bytes': [ [ 0, 4 ] ] }

            cut.cutLines( inputFile, options )

        self.assertTrue( 'abcd\nghij\nnopq\ntuvw\n' == mockStdout.getvalue() )

    #   test cutLines - 08. cut multiple lines (no LF at the end) and a range of colums starting from begin
    def test_cutLine_bytesMultipleLinesAndRangeFromBegin02( self ):

        with patch( 'sys.stdout', new=StringIO() ) as mockStdout:
            inputFile = StringIO( 'abcdef\nghijklm\nnopqrs\ntuvwxyz' )
            options = { 'bytes': [ [ 0, 4 ] ] }

            cut.cutLines( inputFile, options )

        self.assertTrue( 'abcd\nghij\nnopq\ntuvw\n' == mockStdout.getvalue() )

    #   test cutLines - 09. cut a single line and a range of colums to the end
    def test_cutLine_bytesSingleLineAndRangeToEnd01( self ):

        with patch( 'sys.stdout', new=StringIO() ) as mockStdout:
            inputFile = StringIO( 'abcdefghijklm\n' )
            options = { 'bytes': [ [ 4, 0 ] ] }

            cut.cutLines( inputFile, options )

        self.assertTrue( 'efghijklm\n' == mockStdout.getvalue() )

    #   test cutLines - 06. cut a single line (no LF) and a range of colums to the end
    def test_cutLine_bytesSingleLineAndRangeToEnd02( self ):

        with patch( 'sys.stdout', new=StringIO() ) as mockStdout:
            inputFile = StringIO( 'abcdefghijklm' )
            options = { 'bytes': [ [ 4, 0 ] ] }

            cut.cutLines( inputFile, options )

        self.assertTrue( 'efghijklm\n' == mockStdout.getvalue() )

    #   test cutLines - 11. cut multiple lines and a range of colums to the end
    def test_cutLine_bytesMultipleLinesAndRangeToEnd01( self ):

        with patch( 'sys.stdout', new=StringIO() ) as mockStdout:
            inputFile = StringIO( 'abcdef\nghijklm\nnopqrs\ntuvwxyz\n' )
            options = { 'bytes': [ [ 4, 0 ] ] }

            cut.cutLines( inputFile, options )

        self.assertTrue( 'ef\nklm\nrs\nxyz\n' == mockStdout.getvalue() )

    #   test cutLines - 12. cut multiple lines (no LF at the end) and a range of colums to the end
    def test_cutLine_bytesMultipleLinesAndRangeToEnd02( self ):

        with patch( 'sys.stdout', new=StringIO() ) as mockStdout:
            inputFile = StringIO( 'abcdef\nghijklm\nnopqrs\ntuvwxyz' )
            options = { 'bytes': [ [ 4, 0 ] ] }

            cut.cutLines( inputFile, options )

        sys.stderr.write( '[debug] result: \'' + mockStdout.getvalue() + '\'\n' )
        self.assertTrue( 'ef\nklm\nrs\nxyz\n' == mockStdout.getvalue() )

    #   cut.parseRanges() function tests

    #   cut.main() function tests

    #   test cut - 01. check for no required options
    def test_withoutOptions( self ):

        with patch( 'sys.stderr', new=StringIO() ) as mockStderr:
            with self.assertRaises( SystemExit ) as exit:
                sys.argv = [ 'cut' ]
                cut.main()

            self.assertEqual( exit.exception.code, 2 )
            self.assertTrue( -1 != mockStderr.getvalue().find( 'you must specify a list of bytes, characters, or fields' ) )

    #   test cut - 02. check for version options
    def test_versionOption( self ):

        with patch( 'sys.stdout', new=StringIO() ) as mockStdout:
            sys.argv = [ 'cut', '--version' ]
            cut.main()

            self.assertTrue( -1 != mockStdout.getvalue().find( 'Written by Aldebaran Perseke' ) )

    #   test cut - 03. check for invalid option only
    def test_invalidOptionOnly( self ):

        with patch( 'sys.stderr', new=StringIO() ) as mockStderr:
            with self.assertRaises( SystemExit ) as exit:
                sys.argv = [ 'cut', '-a' ]
                cut.main()

            self.assertEqual( exit.exception.code, 2 )
            self.assertTrue( -1 != mockStderr.getvalue().find( 'unrecognized arguments: -a' ) )

    #   test cut - 04. check for the ignored option only
    def test_ignoredOptionOnly( self ):

        with patch( 'sys.stderr', new=StringIO() ) as mockStderr:
            with self.assertRaises( SystemExit ) as exit:
                sys.argv = [ 'cut', '-n' ]
                cut.main()

            self.assertEqual( exit.exception.code, 2 )
            self.assertTrue( -1 != mockStderr.getvalue().find( 'you must specify a list of bytes, characters, or fields' ) )

    #   test cut - 05. check for invalid option
    def test_invalidOption( self ):

        with patch( 'sys.stderr', new=StringIO() ) as mockStderr:
            with self.assertRaises( SystemExit ) as exit:
                sys.argv = [ 'cut', '-a', '--bytes=4' ]
                cut.main()

            self.assertEqual( exit.exception.code, 2 )
            self.assertTrue( -1 != mockStderr.getvalue().find( 'unrecognized arguments: -a' ) )

    #   test cut - 06. check for the ignored option
    def test_ignoredOption( self ):

        with patch( 'sys.stdout', new=StringIO() ) as mockStdout:
            with patch( 'sys.stdin', new=StringIO( 'abcdefghijklm\n' ) ) as mockStdin:
                sys.argv = [ 'cut', '-n', '-b4' ]
                cut.main()

        self.assertTrue( 'd\n' == mockStdout.getvalue() )

    #   test cut - 07. check for bytes and characters options together
    def test_bytesAndCharactersOptions( self ):

        with patch( 'sys.stderr', new=StringIO() ) as mockStderr:
            with self.assertRaises( SystemExit ) as exit:
                sys.argv = [ 'cut', '--bytes=4', '--characters=5' ]
                cut.main()

            self.assertEqual( exit.exception.code, 2 )
            self.assertTrue( -1 != mockStderr.getvalue().find( 'only one type of list may be specified' ) )

    #   test cut - 08. check for bytes and fields options together
    def test_bytesAndFieldsOptions( self ):

        with patch( 'sys.stderr', new=StringIO() ) as mockStderr:
            with self.assertRaises( SystemExit ) as exit:
                sys.argv = [ 'cut', '--bytes=4', '--fields=5' ]
                cut.main()

            self.assertEqual( exit.exception.code, 2 )
            self.assertTrue( -1 != mockStderr.getvalue().find( 'only one type of list may be specified' ) )

    #   test cut - 09. check for characters and fields options together
    def test_charactersAndFieldsOptions( self ):

        with patch( 'sys.stderr', new=StringIO() ) as mockStderr:
            with self.assertRaises( SystemExit ) as exit:
                sys.argv = [ 'cut', '--characters=4', '--fields=5' ]
                cut.main()

            self.assertEqual( exit.exception.code, 2 )
            self.assertTrue( -1 != mockStderr.getvalue().find( 'only one type of list may be specified' ) )

    #   test cut - 10. check for bytes and delimiter options together
    def test_bytesAndDelimiterOptions( self ):

        with patch( 'sys.stderr', new=StringIO() ) as mockStderr:
            with self.assertRaises( SystemExit ) as exit:
                sys.argv = [ 'cut', '--bytes=4', '--delimiter=;' ]
                cut.main()

            self.assertEqual( exit.exception.code, 2 )
            self.assertTrue( -1 != mockStderr.getvalue().find( 'an input delimiter may be specified only when operating on fields' ) )

    #   test cut - 11. check for bytes and characters options together
    def test_charactersAndDelimiterOptions( self ):

        with patch( 'sys.stderr', new=StringIO() ) as mockStderr:
            with self.assertRaises( SystemExit ) as exit:
                sys.argv = [ 'cut', '--characters=5', '--delimiter=;' ]
                cut.main()

            self.assertEqual( exit.exception.code, 2 )
            self.assertTrue( -1 != mockStderr.getvalue().find( 'an input delimiter may be specified only when operating on fields' ) )

    #   test cut - 12. check for missing parameter for bytes options
    def test_missingParameterForBytesOptions( self ):

        with patch( 'sys.stderr', new=StringIO() ) as mockStderr:
            with self.assertRaises( SystemExit ) as exit:
                sys.argv = [ 'cut', '--bytes=' ]
                cut.main()

            self.assertEqual( exit.exception.code, 2 )
            self.assertTrue( -1 != mockStderr.getvalue().find( 'argument -b/--bytes=: expected one argument' ) )

    #   test cut - 13. check for invalid parameter for bytes options
    def test_invalidParameterForBytesOptions( self ):

        with patch( 'sys.stderr', new=StringIO() ) as mockStderr:
            with self.assertRaises( SystemExit ) as exit:
                sys.argv = [ 'cut', '--bytes=a' ]
                cut.main()

#            sys.stdout.write( '[debug] result: \'' + mockStderr.getvalue() + '\'\n' )
            self.assertEqual( exit.exception.code, 2 )
            self.assertTrue( -1 != mockStderr.getvalue().find( 'invalid byte/character position "a"' ) )

#	entry point

if __name__ == '__main__':
    unittest.main()

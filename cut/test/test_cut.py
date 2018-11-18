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
    def test_cutLine_bytesSingleLineAndRangeFromBegin( self ):

        with patch( 'sys.stdout', new=StringIO() ) as mockStdout:
            inputFile = StringIO( 'abcdefghijklm\n' )
            options = { 'bytes': [ [ 0, 4 ] ] }

            cut.cutLines( inputFile, options )

        self.assertTrue( 'abcd\n' == mockStdout.getvalue() )

    #   test cutLines - 06. cut multiple lines and a range of colums starting from begin
    def test_cutLine_bytesMultipleLinesAndRangeFromBegin( self ):

        with patch( 'sys.stdout', new=StringIO() ) as mockStdout:
            inputFile = StringIO( 'abcdef\nghijklm\nnopqrs\ntuvwxyz\n' )
            options = { 'bytes': [ [ 0, 4 ] ] }

            cut.cutLines( inputFile, options )

        self.assertTrue( 'abcd\nghij\nnopq\ntuvw\n' == mockStdout.getvalue() )

    #   test cutLines - 07. cut a single line and a range of colums to the end
    def test_cutLine_bytesSingleLineAndRangeToEnd( self ):

        with patch( 'sys.stdout', new=StringIO() ) as mockStdout:
            inputFile = StringIO( 'abcdefghijklm\n' )
            options = { 'bytes': [ [ 4, 0 ] ] }

            cut.cutLines( inputFile, options )

        self.assertTrue( 'efghijklm\n' == mockStdout.getvalue() )

    #   test cutLines - 08. cut multiple lines and a range of colums to the end
    def test_cutLine_bytesMultipleLinesAndRangeToEnd( self ):

        with patch( 'sys.stdout', new=StringIO() ) as mockStdout:
            inputFile = StringIO( 'abcdef\nghijklm\nnopqrs\ntuvwxyz\n' )
            options = { 'bytes': [ [ 4, 0 ] ] }

            cut.cutLines( inputFile, options )

        self.assertTrue( 'ef\nklm\nrs\nxyz\n' == mockStdout.getvalue() )

    #   test cutLines - 09. cut a single line and a range of colums
    def test_cutLine_bytesSingleLineAndRange( self ):

        with patch( 'sys.stdout', new=StringIO() ) as mockStdout:
            inputFile = StringIO( 'abcdefghijklm\n' )
            options = { 'bytes': [ [ 4, 8 ] ] }

            cut.cutLines( inputFile, options )

        self.assertTrue( 'efgh\n' == mockStdout.getvalue() )

    #   test cutLines - 10. cut multiple lines and a range of colums
    def test_cutLine_bytesMultipleLinesAndRange( self ):

        with patch( 'sys.stdout', new=StringIO() ) as mockStdout:
            inputFile = StringIO( 'abcdef\nghijklm\nnopqrs\ntuvwxyz\n' )
            options = { 'bytes': [ [ 2, 5 ] ] }

            cut.cutLines( inputFile, options )

        self.assertTrue( 'cde\nijk\npqr\nvwx\n' == mockStdout.getvalue() )

    #   test cutLines - 11. cut multiple lines combining single column and a range from begin
    def test_cutLine_bytesMultipleLinesAndSingleColumnAndRangeFromBegin( self ):

        with patch( 'sys.stdout', new=StringIO() ) as mockStdout:
            inputFile = StringIO( 'abcdef\nghijklm\nnopqrs\ntuvwxyz' )
            options = { 'bytes': [ [ 5, 6 ], [ 0, 2 ] ] }

            cut.cutLines( inputFile, options )

        self.assertTrue( 'fab\nlgh\nsno\nytu\n' == mockStdout.getvalue() )

    #   test cutLines - 12. cut multiple lines combining single column and a range to end
    def test_cutLine_bytesMultipleLinesAndSingleColumnAndRangeToEnd( self ):

        with patch( 'sys.stdout', new=StringIO() ) as mockStdout:
            inputFile = StringIO( 'abcdef\nghijklm\nnopqrs\ntuvwxyz' )
            options = { 'bytes': [ [ 4, 0 ], [ 2, 3 ] ] }

            cut.cutLines( inputFile, options )

        self.assertTrue( 'efc\nklmi\nrsp\nxyzv\n' == mockStdout.getvalue() )

    #   test cutLines - 13. cut multiple lines combining single column and a range
    def test_cutLine_bytesMultipleLinesAndSingleColumnAndRange( self ):

        with patch( 'sys.stdout', new=StringIO() ) as mockStdout:
            inputFile = StringIO( 'abcdef\nghijklm\nnopqrs\ntuvwxyz' )
            options = { 'bytes': [ [ 1, 3 ], [ 5, 6 ] ] }

            cut.cutLines( inputFile, options )

        self.assertTrue( 'bcf\nhil\nops\nuvy\n' == mockStdout.getvalue() )

    #   test cutLines - 14. out of range in single column
    def test_cutLine_outOfRangeInSingleColumn( self ):

        with patch( 'sys.stdout', new=StringIO() ) as mockStdout:
            inputFile = StringIO( 'abcdef\nghijklm\nnopqrs\ntuvwxyz' )
            options = { 'bytes': [ [ 6, 7 ] ] }

            cut.cutLines( inputFile, options )

        self.assertTrue( '\nm\n\nz\n' == mockStdout.getvalue() )

    #   test cutLines - 15. out of range in column range from begin
    def test_cutLine_outOfRangeInColumnRangeFromBegin( self ):

        with patch( 'sys.stdout', new=StringIO() ) as mockStdout:
            inputFile = StringIO( 'abcdef\nghijklm\nnopqrs\ntuvwxyz' )
            options = { 'bytes': [ [ 0, 7 ] ] }

            cut.cutLines( inputFile, options )

        self.assertTrue( 'abcdef\nghijklm\nnopqrs\ntuvwxyz\n' == mockStdout.getvalue() )

    #   test cutLines - 16. out of range in column range to end
    def test_cutLine_outOfRangeInColumnRangeToEnd( self ):

        with patch( 'sys.stdout', new=StringIO() ) as mockStdout:
            inputFile = StringIO( 'abcdef\nghijklm\nnopqrs\ntuvwxyz' )
            options = { 'bytes': [ [ 6, 0 ] ] }

            cut.cutLines( inputFile, options )

        sys.stderr.write( '[debug] result: \'' + mockStdout.getvalue() + '\'\n' )
        self.assertTrue( '\nm\n\nz\n' == mockStdout.getvalue() )

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
                sys.argv = [ 'cut', '-n', '--bytes=4' ]
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
                sys.argv = [ 'cut', '--bytes=b' ]
                cut.main()

            self.assertEqual( exit.exception.code, 2 )
            self.assertTrue( -1 != mockStderr.getvalue().find( 'invalid byte/character position "b"' ) )

    #   test cut - 14. check for missing parameter for characters options
    def test_missingParameterForCharactersOptions( self ):

        with patch( 'sys.stderr', new=StringIO() ) as mockStderr:
            with self.assertRaises( SystemExit ) as exit:
                sys.argv = [ 'cut', '--characters=' ]
                cut.main()

            self.assertEqual( exit.exception.code, 2 )
            self.assertTrue( -1 != mockStderr.getvalue().find( 'argument -c/--characters=: expected one argument' ) )

    #   test cut - 15. check for invalid parameter for characters options
    def test_invalidParameterForCharactersOptions( self ):

        with patch( 'sys.stderr', new=StringIO() ) as mockStderr:
            with self.assertRaises( SystemExit ) as exit:
                sys.argv = [ 'cut', '--characters=c' ]
                cut.main()

            self.assertEqual( exit.exception.code, 2 )
            self.assertTrue( -1 != mockStderr.getvalue().find( 'invalid byte/character position "c"' ) )

    #   test cut - 16. check for missing parameter for fields options
    def test_missingParameterForFieldsOptions( self ):

        with patch( 'sys.stderr', new=StringIO() ) as mockStderr:
            with self.assertRaises( SystemExit ) as exit:
                sys.argv = [ 'cut', '--fields=' ]
                cut.main()

            self.assertEqual( exit.exception.code, 2 )
            self.assertTrue( -1 != mockStderr.getvalue().find( 'argument -f/--fields=: expected one argument' ) )

    #   test cut - 17. check for invalid parameter for fields options
    def test_invalidParameterForFieldsOptions( self ):

        with patch( 'sys.stderr', new=StringIO() ) as mockStderr:
            with self.assertRaises( SystemExit ) as exit:
                sys.argv = [ 'cut', '--fields=f' ]
                cut.main()

            self.assertEqual( exit.exception.code, 2 )
            self.assertTrue( -1 != mockStderr.getvalue().find( 'invalid byte/character position "f"' ) )

    #   test cut - 18. check for missing parameter for delimiter option
    def test_missingParameterForDelimiterOption( self ):

        with patch( 'sys.stderr', new=StringIO() ) as mockStderr:
            with self.assertRaises( SystemExit ) as exit:
                sys.argv = [ 'cut', '--delimiter=', '--field=2' ]
                cut.main()

            self.assertEqual( exit.exception.code, 2 )
            self.assertTrue( -1 != mockStderr.getvalue().find( 'argument -d/--delimiter=: expected one argument' ) )

    #   test cut - 19. check for invalid parameter for delimiter option
    def test_invalidParameterForDelimiterOption( self ):

        with patch( 'sys.stderr', new=StringIO() ) as mockStderr:
            with self.assertRaises( SystemExit ) as exit:
                sys.argv = [ 'cut', '--delimiter=tab', '--field=2' ]
                cut.main()

            sys.stdout.write( '[debug] result: \'' + mockStderr.getvalue() + '\'\n' )
            self.assertEqual( exit.exception.code, 2 )
            self.assertTrue( -1 != mockStderr.getvalue().find( 'the delimiter must be a single character' ) )

#	entry point

if __name__ == '__main__':
    unittest.main()

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

    #   test cutLines - 01. cut a single line and column
    def test_cutLine_bytes01( self ):

        with patch( 'sys.stdout', new=StringIO() ) as mockStdout:
            inputFile = StringIO( 'abcdefghijklm\nnopqrstuvwxyz\n' )
            options = { 'bytes': [ [ 3, 4 ] ] }

            cut.cutLines( inputFile, options )

        sys.stderr.write( '[debug] result: \'' + mockStdout.getvalue() + '\'\n' )
        self.assertTrue( 'd\nq\n' == mockStdout.getvalue() )

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

#	entry point

if __name__ == '__main__':
    unittest.main()

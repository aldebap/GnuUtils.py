#!	/usr/bin/python3

################################################################################
#	test_cut.py  -  Nov-15-2018 by aldebap
#
#	Unit tests for the Python version of GNU Linux cut utility
################################################################################

from io import StringIO
from unittest.mock import patch
import unittest
import os
import sys
import tempfile

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
    def test_cutLine_bytesOutOfRangeInSingleColumn( self ):

        with patch( 'sys.stdout', new=StringIO() ) as mockStdout:
            inputFile = StringIO( 'abcdef\nghijklm\nnopqrs\ntuvwxyz' )
            options = { 'bytes': [ [ 6, 7 ] ] }

            cut.cutLines( inputFile, options )

        self.assertTrue( '\nm\n\nz\n' == mockStdout.getvalue() )

    #   test cutLines - 15. out of range in column range from begin
    def test_cutLine_bytesOutOfRangeInColumnRangeFromBegin( self ):

        with patch( 'sys.stdout', new=StringIO() ) as mockStdout:
            inputFile = StringIO( 'abcdef\nghijklm\nnopqrs\ntuvwxyz' )
            options = { 'bytes': [ [ 0, 7 ] ] }

            cut.cutLines( inputFile, options )

        self.assertTrue( 'abcdef\nghijklm\nnopqrs\ntuvwxyz\n' == mockStdout.getvalue() )

    #   test cutLines - 16. out of range in column range to end
    def test_cutLine_bytesOutOfRangeInColumnRangeToEnd( self ):

        with patch( 'sys.stdout', new=StringIO() ) as mockStdout:
            inputFile = StringIO( 'abcdef\nghijklm\nnopqrs\ntuvwxyz' )
            options = { 'bytes': [ [ 6, 0 ] ] }

            cut.cutLines( inputFile, options )

        self.assertTrue( '\nm\n\nz\n' == mockStdout.getvalue() )

    #   test cutLines - 17. complement of cut multiple lines
    def test_cutLine_bytesComplementMultipleLines( self ):

        with patch( 'sys.stdout', new=StringIO() ) as mockStdout:
            inputFile = StringIO( 'abcdef\nghijklm\nnopqrs\ntuvwxyz' )
            options = { 'bytes': [ [ 1, 3 ], [ 5, 6 ] ], 'complement': True }

            cut.cutLines( inputFile, options )

        self.assertTrue( 'ade\ngjkm\nnqr\ntwxz\n' == mockStdout.getvalue() )

    #   test cutLines - 18. cut a single line and column
    def test_cutLine_charactersSingleLineAndColumn01( self ):

        with patch( 'sys.stdout', new=StringIO() ) as mockStdout:
            inputFile = StringIO( 'abcdefghijklm\n' )
            options = { 'characters': [ [ 3, 4 ] ] }

            cut.cutLines( inputFile, options )

        self.assertTrue( 'd\n' == mockStdout.getvalue() )

    #   test cutLines - 19. cut a single line (no LF) and column
    def test_cutLine_charactersSingleLineAndColumn02( self ):

        with patch( 'sys.stdout', new=StringIO() ) as mockStdout:
            inputFile = StringIO( 'abcdefghijklm' )
            options = { 'characters': [ [ 3, 4 ] ] }

            cut.cutLines( inputFile, options )

        self.assertTrue( 'd\n' == mockStdout.getvalue() )

    #   test cutLines - 20. cut multiple lines and a single column
    def test_cutLine_charactersMultipleLinesAndSingleColumn01( self ):

        with patch( 'sys.stdout', new=StringIO() ) as mockStdout:
            inputFile = StringIO( 'abcdef\nghijklm\nnopqrs\ntuvwxyz\n' )
            options = { 'characters': [ [ 3, 4 ] ] }

            cut.cutLines( inputFile, options )

        self.assertTrue( 'd\nj\nq\nw\n' == mockStdout.getvalue() )

    #   test cutLines - 21. cut multiple lines (no LF at the end) and a single column
    def test_cutLine_charactersMultipleLinesAndSingleColumn02( self ):

        with patch( 'sys.stdout', new=StringIO() ) as mockStdout:
            inputFile = StringIO( 'abcdef\nghijklm\nnopqrs\ntuvwxyz' )
            options = { 'characters': [ [ 3, 4 ] ] }

            cut.cutLines( inputFile, options )

        self.assertTrue( 'd\nj\nq\nw\n' == mockStdout.getvalue() )

    #   test cutLines - 22. cut a single line and a range of colums starting from begin
    def test_cutLine_charactersSingleLineAndRangeFromBegin( self ):

        with patch( 'sys.stdout', new=StringIO() ) as mockStdout:
            inputFile = StringIO( 'abcdefghijklm\n' )
            options = { 'characters': [ [ 0, 4 ] ] }

            cut.cutLines( inputFile, options )

        self.assertTrue( 'abcd\n' == mockStdout.getvalue() )

    #   test cutLines - 23. cut multiple lines and a range of colums starting from begin
    def test_cutLine_charactersMultipleLinesAndRangeFromBegin( self ):

        with patch( 'sys.stdout', new=StringIO() ) as mockStdout:
            inputFile = StringIO( 'abcdef\nghijklm\nnopqrs\ntuvwxyz\n' )
            options = { 'characters': [ [ 0, 4 ] ] }

            cut.cutLines( inputFile, options )

        self.assertTrue( 'abcd\nghij\nnopq\ntuvw\n' == mockStdout.getvalue() )

    #   test cutLines - 24. cut a single line and a range of colums to the end
    def test_cutLine_charactersSingleLineAndRangeToEnd( self ):

        with patch( 'sys.stdout', new=StringIO() ) as mockStdout:
            inputFile = StringIO( 'abcdefghijklm\n' )
            options = { 'characters': [ [ 4, 0 ] ] }

            cut.cutLines( inputFile, options )

        self.assertTrue( 'efghijklm\n' == mockStdout.getvalue() )

    #   test cutLines - 25. cut multiple lines and a range of colums to the end
    def test_cutLine_charactersMultipleLinesAndRangeToEnd( self ):

        with patch( 'sys.stdout', new=StringIO() ) as mockStdout:
            inputFile = StringIO( 'abcdef\nghijklm\nnopqrs\ntuvwxyz\n' )
            options = { 'characters': [ [ 4, 0 ] ] }

            cut.cutLines( inputFile, options )

        self.assertTrue( 'ef\nklm\nrs\nxyz\n' == mockStdout.getvalue() )

    #   test cutLines - 26. cut a single line and a range of colums
    def test_cutLine_charactersSingleLineAndRange( self ):

        with patch( 'sys.stdout', new=StringIO() ) as mockStdout:
            inputFile = StringIO( 'abcdefghijklm\n' )
            options = { 'characters': [ [ 4, 8 ] ] }

            cut.cutLines( inputFile, options )

        self.assertTrue( 'efgh\n' == mockStdout.getvalue() )

    #   test cutLines - 27. cut multiple lines and a range of colums
    def test_cutLine_charactersMultipleLinesAndRange( self ):

        with patch( 'sys.stdout', new=StringIO() ) as mockStdout:
            inputFile = StringIO( 'abcdef\nghijklm\nnopqrs\ntuvwxyz\n' )
            options = { 'characters': [ [ 2, 5 ] ] }

            cut.cutLines( inputFile, options )

        self.assertTrue( 'cde\nijk\npqr\nvwx\n' == mockStdout.getvalue() )

    #   test cutLines - 28. cut multiple lines combining single column and a range from begin
    def test_cutLine_charactersMultipleLinesAndSingleColumnAndRangeFromBegin( self ):

        with patch( 'sys.stdout', new=StringIO() ) as mockStdout:
            inputFile = StringIO( 'abcdef\nghijklm\nnopqrs\ntuvwxyz' )
            options = { 'characters': [ [ 5, 6 ], [ 0, 2 ] ] }

            cut.cutLines( inputFile, options )

        self.assertTrue( 'fab\nlgh\nsno\nytu\n' == mockStdout.getvalue() )

    #   test cutLines - 29. cut multiple lines combining single column and a range to end
    def test_cutLine_charactersMultipleLinesAndSingleColumnAndRangeToEnd( self ):

        with patch( 'sys.stdout', new=StringIO() ) as mockStdout:
            inputFile = StringIO( 'abcdef\nghijklm\nnopqrs\ntuvwxyz' )
            options = { 'characters': [ [ 4, 0 ], [ 2, 3 ] ] }

            cut.cutLines( inputFile, options )

        self.assertTrue( 'efc\nklmi\nrsp\nxyzv\n' == mockStdout.getvalue() )

    #   test cutLines - 30. cut multiple lines combining single column and a range
    def test_cutLine_charactersMultipleLinesAndSingleColumnAndRange( self ):

        with patch( 'sys.stdout', new=StringIO() ) as mockStdout:
            inputFile = StringIO( 'abcdef\nghijklm\nnopqrs\ntuvwxyz' )
            options = { 'characters': [ [ 1, 3 ], [ 5, 6 ] ] }

            cut.cutLines( inputFile, options )

        self.assertTrue( 'bcf\nhil\nops\nuvy\n' == mockStdout.getvalue() )

    #   test cutLines - 31. out of range in single column
    def test_cutLine_charactersOutOfRangeInSingleColumn( self ):

        with patch( 'sys.stdout', new=StringIO() ) as mockStdout:
            inputFile = StringIO( 'abcdef\nghijklm\nnopqrs\ntuvwxyz' )
            options = { 'characters': [ [ 6, 7 ] ] }

            cut.cutLines( inputFile, options )

        self.assertTrue( '\nm\n\nz\n' == mockStdout.getvalue() )

    #   test cutLines - 32. out of range in column range from begin
    def test_cutLine_charactersOutOfRangeInColumnRangeFromBegin( self ):

        with patch( 'sys.stdout', new=StringIO() ) as mockStdout:
            inputFile = StringIO( 'abcdef\nghijklm\nnopqrs\ntuvwxyz' )
            options = { 'characters': [ [ 0, 7 ] ] }

            cut.cutLines( inputFile, options )

        self.assertTrue( 'abcdef\nghijklm\nnopqrs\ntuvwxyz\n' == mockStdout.getvalue() )

    #   test cutLines - 33. out of range in column range to end
    def test_cutLine_charactersOutOfRangeInColumnRangeToEnd( self ):

        with patch( 'sys.stdout', new=StringIO() ) as mockStdout:
            inputFile = StringIO( 'abcdef\nghijklm\nnopqrs\ntuvwxyz' )
            options = { 'characters': [ [ 6, 0 ] ] }

            cut.cutLines( inputFile, options )

        self.assertTrue( '\nm\n\nz\n' == mockStdout.getvalue() )

    #   test cutLines - 34. complement of cut multiple lines
    def test_cutLine_charactersComplementMultipleLines( self ):

        with patch( 'sys.stdout', new=StringIO() ) as mockStdout:
            inputFile = StringIO( 'abcdef\nghijklm\nnopqrs\ntuvwxyz' )
            options = { 'characters': [ [ 1, 3 ], [ 5, 6 ] ], 'complement': True }

            cut.cutLines( inputFile, options )

        self.assertTrue( 'ade\ngjkm\nnqr\ntwxz\n' == mockStdout.getvalue() )

    #   test cutLines - 35. cut a single line and column
    def test_cutLine_fieldsSingleLineAndColumn01( self ):

        with patch( 'sys.stdout', new=StringIO() ) as mockStdout:
            inputFile = StringIO( 'ab;cd;ef;gh;ij;klm\n' )
            options = { 'fields': [ [ 3, 4 ] ], 'delimiter': ';' }

            cut.cutLines( inputFile, options )

        self.assertTrue( 'gh\n' == mockStdout.getvalue() )

    #   test cutLines - 36. cut a single line (no LF) and column
    def test_cutLine_fieldsSingleLineAndColumn02( self ):

        with patch( 'sys.stdout', new=StringIO() ) as mockStdout:
            inputFile = StringIO( 'ab;cd;ef;gh;ij;klm' )
            options = { 'fields': [ [ 3, 4 ] ], 'delimiter': ';' }

            cut.cutLines( inputFile, options )

        self.assertTrue( 'gh\n' == mockStdout.getvalue() )

    #   test cutLines - 37. cut multiple lines and a single column
    def test_cutLine_fieldsMultipleLinesAndSingleColumn01( self ):

        with patch( 'sys.stdout', new=StringIO() ) as mockStdout:
            inputFile = StringIO( 'ab;cd;ef;gh;ij\nkl;mn;op;qr;st\nuv;wx;yz;12;34\n' )
            options = { 'fields': [ [ 3, 4 ] ], 'delimiter': ';' }

            cut.cutLines( inputFile, options )

        self.assertTrue( 'gh\nqr\n12\n' == mockStdout.getvalue() )

    #   test cutLines - 38. cut multiple lines (no LF at the end) and a single column
    def test_cutLine_fieldsMultipleLinesAndSingleColumn02( self ):

        with patch( 'sys.stdout', new=StringIO() ) as mockStdout:
            inputFile = StringIO( 'ab;cd;ef;gh;ij\nkl;mn;op;qr;st\nuv;wx;yz;12;34' )
            options = { 'fields': [ [ 3, 4 ] ], 'delimiter': ';' }

            cut.cutLines( inputFile, options )

        self.assertTrue( 'gh\nqr\n12\n' == mockStdout.getvalue() )

    #   test cutLines - 39. cut a single line and a range of colums starting from begin
    def test_cutLine_fieldsSingleLineAndRangeFromBegin( self ):

        with patch( 'sys.stdout', new=StringIO() ) as mockStdout:
            inputFile = StringIO( 'ab;cd;ef;gh;ij;klm\n' )
            options = { 'fields': [ [ 0, 4 ] ], 'delimiter': ';' }

            cut.cutLines( inputFile, options )

        self.assertTrue( 'ab;cd;ef;gh\n' == mockStdout.getvalue() )

    #   test cutLines - 40. cut multiple lines and a range of colums starting from begin
    def test_cutLine_fieldsMultipleLinesAndRangeFromBegin( self ):

        with patch( 'sys.stdout', new=StringIO() ) as mockStdout:
            inputFile = StringIO( 'ab;cd;ef;gh;ij\nkl;mn;op;qr;st\nuv;wx;yz;12;34' )
            options = { 'fields': [ [ 0, 4 ] ], 'delimiter': ';' }

            cut.cutLines( inputFile, options )

        self.assertTrue( 'ab;cd;ef;gh\nkl;mn;op;qr\nuv;wx;yz;12\n' == mockStdout.getvalue() )

    #   test cutLines - 41. cut a single line and a range of colums to the end
    def test_cutLine_fieldsSingleLineAndRangeToEnd( self ):

        with patch( 'sys.stdout', new=StringIO() ) as mockStdout:
            inputFile = StringIO( 'ab;cd;ef;gh;ij;klm\n' )
            options = { 'fields': [ [ 4, 0 ] ], 'delimiter': ';' }

            cut.cutLines( inputFile, options )

        self.assertTrue( 'ij;klm\n' == mockStdout.getvalue() )

    #   test cutLines - 42. cut multiple lines and a range of colums to the end
    def test_cutLine_fieldsMultipleLinesAndRangeToEnd( self ):

        with patch( 'sys.stdout', new=StringIO() ) as mockStdout:
            inputFile = StringIO( 'ab;cd;ef;gh;ij\nkl;mn;op;qr;st\nuv;wx;yz;12;34' )
            options = { 'fields': [ [ 4, 0 ] ], 'delimiter': ';' }

            cut.cutLines( inputFile, options )

        self.assertTrue( 'ij\nst\n34\n' == mockStdout.getvalue() )

    #   test cutLines - 43. cut a single line and a range of colums
    def test_cutLine_fieldsSingleLineAndRange( self ):

        with patch( 'sys.stdout', new=StringIO() ) as mockStdout:
            inputFile = StringIO( 'ab;cd;ef;gh;ij;kl;mn;op;qr\n' )
            options = { 'fields': [ [ 4, 8 ] ], 'delimiter': ';' }

            cut.cutLines( inputFile, options )

        self.assertTrue( 'ij;kl;mn;op\n' == mockStdout.getvalue() )

    #   test cutLines - 44. cut multiple lines and a range of colums
    def test_cutLine_fieldsMultipleLinesAndRange( self ):

        with patch( 'sys.stdout', new=StringIO() ) as mockStdout:
            inputFile = StringIO( 'ab;cd;ef;gh;ij\nkl;mn;op;qr;st\nuv;wx;yz;12;34;56' )
            options = { 'fields': [ [ 2, 5 ] ], 'delimiter': ';' }

            cut.cutLines( inputFile, options )

        self.assertTrue( 'ef;gh;ij\nop;qr;st\nyz;12;34\n' == mockStdout.getvalue() )

    #   test cutLines - 45. cut multiple lines combining single column and a range from begin
    def test_cutLine_fieldsMultipleLinesAndSingleColumnAndRangeFromBegin( self ):

        with patch( 'sys.stdout', new=StringIO() ) as mockStdout:
            inputFile = StringIO( 'ab;cd;ef;gh;ij\nkl;mn;op;qr;st\nuv;wx;yz;12;34;56' )
            options = { 'fields': [ [ 3, 4 ], [ 0, 2 ] ], 'delimiter': ';' }

            cut.cutLines( inputFile, options )

        self.assertTrue( 'gh;ab;cd\nqr;kl;mn\n12;uv;wx\n' == mockStdout.getvalue() )

    #   test cutLines - 46. cut multiple lines combining single column and a range to end
    def test_cutLine_fieldsMultipleLinesAndSingleColumnAndRangeToEnd( self ):

        with patch( 'sys.stdout', new=StringIO() ) as mockStdout:
            inputFile = StringIO( 'ab;cd;ef;gh;ij\nkl;mn;op;qr;st\nuv;wx;yz;12;34;56' )
            options = { 'fields': [ [ 4, 0 ], [ 2, 3 ] ], 'delimiter': ';' }

            cut.cutLines( inputFile, options )

        self.assertTrue( 'ij;ef\nst;op\n34;56;yz\n' == mockStdout.getvalue() )

    #   test cutLines - 47. cut multiple lines combining single column and a range
    def test_cutLine_fieldsMultipleLinesAndSingleColumnAndRange( self ):

        with patch( 'sys.stdout', new=StringIO() ) as mockStdout:
            inputFile = StringIO( 'ab;cd;ef;gh;ij\nkl;mn;op;qr;st\nuv;wx;yz;12;34;56' )
            options = { 'fields': [ [ 1, 3 ], [ 4, 5 ] ], 'delimiter': ';' }

            cut.cutLines( inputFile, options )

        self.assertTrue( 'cd;ef;ij\nmn;op;st\nwx;yz;34\n' == mockStdout.getvalue() )

    #   test cutLines - 48. out of range in single column
    def test_cutLine_fieldsOutOfRangeInSingleColumn( self ):

        with patch( 'sys.stdout', new=StringIO() ) as mockStdout:
            inputFile = StringIO( 'ab;cd;ef;gh;ij\nkl;mn;op;qr;st\nuv;wx;yz;12;34;56' )
            options = { 'fields': [ [ 5, 6 ] ], 'delimiter': ';' }

            cut.cutLines( inputFile, options )

        self.assertTrue( '\n\n56\n' == mockStdout.getvalue() )

    #   test cutLines - 49. out of range in column range from begin
    def test_cutLine_fieldsOutOfRangeInColumnRangeFromBegin( self ):

        with patch( 'sys.stdout', new=StringIO() ) as mockStdout:
            inputFile = StringIO( 'ab;cd;ef;gh;ij\nkl;mn;op;qr;st\nuv;wx;yz;12;34;56' )
            options = { 'fields': [ [ 0, 7 ] ], 'delimiter': ';' }

            cut.cutLines( inputFile, options )

        self.assertTrue( 'ab;cd;ef;gh;ij\nkl;mn;op;qr;st\nuv;wx;yz;12;34;56\n' == mockStdout.getvalue() )

    #   test cutLines - 50. out of range in column range to end
    def test_cutLine_fieldsOutOfRangeInColumnRangeToEnd( self ):

        with patch( 'sys.stdout', new=StringIO() ) as mockStdout:
            inputFile = StringIO( 'ab;cd;ef;gh;ij\nkl;mn;op;qr;st\nuv;wx;yz;12;34;56' )
            options = { 'fields': [ [ 5, 0 ] ], 'delimiter': ';' }

            cut.cutLines( inputFile, options )

        self.assertTrue( '\n\n56\n' == mockStdout.getvalue() )

    #   test cutLines - 51. complement of cut multiple lines
    def test_cutLine_fieldsComplementMultipleLines( self ):

        with patch( 'sys.stdout', new=StringIO() ) as mockStdout:
            inputFile = StringIO( 'ab;cd;ef;gh;ij;kl;m\nno;pq;rs;tu;vw;xy;z' )
            options = { 'fields': [ [ 1, 3 ], [ 5, 6 ] ], 'delimiter': ';', 'complement': True }

            cut.cutLines( inputFile, options )

        self.assertTrue( 'ab;gh;ij;m\nno;tu;vw;z\n' == mockStdout.getvalue() )

    #   test cutLines - 52. cut multiple lines combining single column and a range, with a chosen output delimiter
    def test_cutLine_fieldsMultipleLinesChosenOutputDelimiter( self ):

        with patch( 'sys.stdout', new=StringIO() ) as mockStdout:
            inputFile = StringIO( 'ab;cd;ef;gh;ij;kl;m\nno;pq;rs;tu;vw;xy;z' )
            options = { 'fields': [ [ 1, 3 ], [ 5, 6 ] ], 'delimiter': ';', 'outputDelimiter': '_' }

            cut.cutLines( inputFile, options )

        self.assertTrue( 'cd_ef_kl\npq_rs_xy\n' == mockStdout.getvalue() )

    #   test cutLines - 53. cut multiple lines combining single column and a range, with a chosen output delimiter
    def test_cutLine_fieldsMultipleLinesOnlyDelimited( self ):

        with patch( 'sys.stdout', new=StringIO() ) as mockStdout:
            inputFile = StringIO( 'ab;cd;ef;gh\nijklmnop\nrs;tu;vw;xy;z' )
            options = { 'fields': [ [ 0, 1 ], [ 3, 4 ] ], 'delimiter': ';', 'outputDelimiter': ' ', 'onlyDelimited': True }

            cut.cutLines( inputFile, options )

        #   sys.stderr.write( '[debug] result: \'' + mockStdout.getvalue() + '\'\n' )
        self.assertTrue( 'ab gh\nrs xy\n' == mockStdout.getvalue() )

    #   cut.parseRanges() function tests
    #   TODO: write all test cases for this function

    #   cut.main() function tests

    #   test main - 01. check for no required options
    def test_main_withoutOptions( self ):

        with patch( 'sys.stderr', new=StringIO() ) as mockStderr:
            with self.assertRaises( SystemExit ) as exit:
                sys.argv = [ 'cut' ]
                cut.main()

        self.assertEqual( exit.exception.code, 2 )
        self.assertTrue( -1 != mockStderr.getvalue().find( 'you must specify a list of bytes, characters, or fields' ) )

    #   test main - 02. check for version options
    def test_main_versionOption( self ):

        with patch( 'sys.stdout', new=StringIO() ) as mockStdout:
            sys.argv = [ 'cut', '--version' ]
            cut.main()

        self.assertTrue( -1 != mockStdout.getvalue().find( 'Written by Aldebaran Perseke' ) )

    #   test main - 03. check for invalid option only
    def test_main_invalidOptionOnly( self ):

        with patch( 'sys.stderr', new=StringIO() ) as mockStderr:
            with self.assertRaises( SystemExit ) as exit:
                sys.argv = [ 'cut', '-a' ]
                cut.main()

        self.assertEqual( exit.exception.code, 2 )
        self.assertTrue( -1 != mockStderr.getvalue().find( 'unrecognized arguments: -a' ) )

    #   test main - 04. check for the ignored option only
    def test_main_ignoredOptionOnly( self ):

        with patch( 'sys.stderr', new=StringIO() ) as mockStderr:
            with self.assertRaises( SystemExit ) as exit:
                sys.argv = [ 'cut', '-n' ]
                cut.main()

        self.assertEqual( exit.exception.code, 2 )
        self.assertTrue( -1 != mockStderr.getvalue().find( 'you must specify a list of bytes, characters, or fields' ) )

    #   test main - 05. check for invalid option
    def test_main_invalidOption( self ):

        with patch( 'sys.stderr', new=StringIO() ) as mockStderr:
            with self.assertRaises( SystemExit ) as exit:
                sys.argv = [ 'cut', '-a', '--bytes=4' ]
                cut.main()

        self.assertEqual( exit.exception.code, 2 )
        self.assertTrue( -1 != mockStderr.getvalue().find( 'unrecognized arguments: -a' ) )

    #   test main - 06. check for the ignored option
    def test_main_ignoredOption( self ):

        with patch( 'sys.stdout', new=StringIO() ) as mockStdout:
            with patch( 'sys.stdin', new=StringIO( 'abcdefghijklm\n' ) ) as mockStdin:
                sys.argv = [ 'cut', '-n', '--bytes=4' ]
                cut.main()

        self.assertTrue( 'd\n' == mockStdout.getvalue() )

    #   test main - 07. check for bytes and characters options together
    def test_main_bytesAndCharactersOptions( self ):

        with patch( 'sys.stderr', new=StringIO() ) as mockStderr:
            with self.assertRaises( SystemExit ) as exit:
                sys.argv = [ 'cut', '--bytes=4', '--characters=5' ]
                cut.main()

        self.assertEqual( exit.exception.code, 2 )
        self.assertTrue( -1 != mockStderr.getvalue().find( 'only one type of list may be specified' ) )

    #   test main - 08. check for bytes and fields options together
    def test_main_bytesAndFieldsOptions( self ):

        with patch( 'sys.stderr', new=StringIO() ) as mockStderr:
            with self.assertRaises( SystemExit ) as exit:
                sys.argv = [ 'cut', '--bytes=4', '--fields=5' ]
                cut.main()

        self.assertEqual( exit.exception.code, 2 )
        self.assertTrue( -1 != mockStderr.getvalue().find( 'only one type of list may be specified' ) )

    #   test main - 09. check for characters and fields options together
    def test_main_charactersAndFieldsOptions( self ):

        with patch( 'sys.stderr', new=StringIO() ) as mockStderr:
            with self.assertRaises( SystemExit ) as exit:
                sys.argv = [ 'cut', '--characters=4', '--fields=5' ]
                cut.main()

        self.assertEqual( exit.exception.code, 2 )
        self.assertTrue( -1 != mockStderr.getvalue().find( 'only one type of list may be specified' ) )

    #   test main - 10. check for bytes and delimiter options together
    def test_main_bytesAndDelimiterOptions( self ):

        with patch( 'sys.stderr', new=StringIO() ) as mockStderr:
            with self.assertRaises( SystemExit ) as exit:
                sys.argv = [ 'cut', '--bytes=4', '--delimiter=;' ]
                cut.main()

        self.assertEqual( exit.exception.code, 2 )
        self.assertTrue( -1 != mockStderr.getvalue().find( 'an input delimiter may be specified only when operating on fields' ) )

    #   test main - 11. check for characters and delimiter options together
    def test_main_charactersAndDelimiterOptions( self ):

        with patch( 'sys.stderr', new=StringIO() ) as mockStderr:
            with self.assertRaises( SystemExit ) as exit:
                sys.argv = [ 'cut', '--characters=5', '--delimiter=;' ]
                cut.main()

        self.assertEqual( exit.exception.code, 2 )
        self.assertTrue( -1 != mockStderr.getvalue().find( 'an input delimiter may be specified only when operating on fields' ) )

    #   test main - 12. check for bytes and only delimiter options together
    def test_main_bytesAndOnlyDelimitedOptions( self ):

        with patch( 'sys.stderr', new=StringIO() ) as mockStderr:
            with self.assertRaises( SystemExit ) as exit:
                sys.argv = [ 'cut', '--bytes=4', '--only-delimited' ]
                cut.main()

        self.assertEqual( exit.exception.code, 2 )
        self.assertTrue( -1 != mockStderr.getvalue().find( 'suppressing non-delimited lines makes sense only when operating on fields' ) )

    #   test main - 13. check for characters and only delimiter options together
    def test_main_charactersAndOnlyDelimitedOptions( self ):

        with patch( 'sys.stderr', new=StringIO() ) as mockStderr:
            with self.assertRaises( SystemExit ) as exit:
                sys.argv = [ 'cut', '--characters=4', '--only-delimited' ]
                cut.main()

        self.assertEqual( exit.exception.code, 2 )
        self.assertTrue( -1 != mockStderr.getvalue().find( 'suppressing non-delimited lines makes sense only when operating on fields' ) )

    #   test main - 14. check for missing parameter for bytes options
    def test_main_missingParameterForBytesOptions( self ):

        with patch( 'sys.stderr', new=StringIO() ) as mockStderr:
            with self.assertRaises( SystemExit ) as exit:
                sys.argv = [ 'cut', '--bytes=' ]
                cut.main()

        self.assertEqual( exit.exception.code, 2 )
        self.assertTrue( -1 != mockStderr.getvalue().find( 'argument -b/--bytes=: expected one argument' ) )

    #   test main - 15. check for invalid parameter for bytes options
    def test_main_invalidParameterForBytesOptions( self ):

        with patch( 'sys.stderr', new=StringIO() ) as mockStderr:
            with self.assertRaises( SystemExit ) as exit:
                sys.argv = [ 'cut', '--bytes=b' ]
                cut.main()

        self.assertEqual( exit.exception.code, 2 )
        self.assertTrue( -1 != mockStderr.getvalue().find( 'invalid byte/character position "b"' ) )

    #   test main - 16. check for missing parameter for characters options
    def test_main_missingParameterForCharactersOptions( self ):

        with patch( 'sys.stderr', new=StringIO() ) as mockStderr:
            with self.assertRaises( SystemExit ) as exit:
                sys.argv = [ 'cut', '--characters=' ]
                cut.main()

        self.assertEqual( exit.exception.code, 2 )
        self.assertTrue( -1 != mockStderr.getvalue().find( 'argument -c/--characters=: expected one argument' ) )

    #   test main - 17. check for invalid parameter for characters options
    def test_main_invalidParameterForCharactersOptions( self ):

        with patch( 'sys.stderr', new=StringIO() ) as mockStderr:
            with self.assertRaises( SystemExit ) as exit:
                sys.argv = [ 'cut', '--characters=c' ]
                cut.main()

        self.assertEqual( exit.exception.code, 2 )
        self.assertTrue( -1 != mockStderr.getvalue().find( 'invalid byte/character position "c"' ) )

    #   test main - 18. check for missing parameter for fields options
    def test_main_missingParameterForFieldsOptions( self ):

        with patch( 'sys.stderr', new=StringIO() ) as mockStderr:
            with self.assertRaises( SystemExit ) as exit:
                sys.argv = [ 'cut', '--fields=' ]
                cut.main()

        self.assertEqual( exit.exception.code, 2 )
        self.assertTrue( -1 != mockStderr.getvalue().find( 'argument -f/--fields=: expected one argument' ) )

    #   test main - 19. check for invalid parameter for fields options
    def test_main_invalidParameterForFieldsOptions( self ):

        with patch( 'sys.stderr', new=StringIO() ) as mockStderr:
            with self.assertRaises( SystemExit ) as exit:
                sys.argv = [ 'cut', '--fields=f' ]
                cut.main()

        self.assertEqual( exit.exception.code, 2 )
        self.assertTrue( -1 != mockStderr.getvalue().find( 'invalid byte/character position "f"' ) )

    #   test main - 20. check for missing parameter for delimiter option
    def test_main_missingParameterForDelimiterOption( self ):

        with patch( 'sys.stderr', new=StringIO() ) as mockStderr:
            with self.assertRaises( SystemExit ) as exit:
                sys.argv = [ 'cut', '--delimiter=', '--field=2' ]
                cut.main()

        self.assertEqual( exit.exception.code, 2 )
        self.assertTrue( -1 != mockStderr.getvalue().find( 'argument -d/--delimiter=: expected one argument' ) )

    #   test main - 21. check for invalid parameter for delimiter option
    def test_main_invalidParameterForDelimiterOption( self ):

        with patch( 'sys.stderr', new=StringIO() ) as mockStderr:
            with self.assertRaises( SystemExit ) as exit:
                sys.argv = [ 'cut', '--delimiter=tab', '--field=2' ]
                cut.main()

        self.assertEqual( exit.exception.code, 2 )
        self.assertTrue( -1 != mockStderr.getvalue().find( 'the delimiter must be a single character' ) )

    #   test main - 22. check for no file names
    def test_main_noFileNames( self ):

        with patch( 'sys.stdout', new=StringIO() ) as mockStdout:
            with patch( 'sys.stdin', new=StringIO( 'abcdef\nghijklm\nnopqrs\ntuvwxyz' ) ) as mockStdin:
                sys.argv = [ 'cut', '--bytes=2-3,6' ]
                cut.main()

        self.assertTrue( 'bcf\nhil\nops\nuvy\n' == mockStdout.getvalue() )

    #   test main - 23. check for hifen as file name
    def test_main_hifenAsFileNames( self ):

        with patch( 'sys.stdout', new=StringIO() ) as mockStdout:
            with patch( 'sys.stdin', new=StringIO( 'abcdef\nghijklm\nnopqrs\ntuvwxyz' ) ) as mockStdin:
                sys.argv = [ 'cut', '--characters=2-3,6', '-' ]
                cut.main()

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
            cut.main()

        self.assertTrue( -1 != mockStderr.getvalue().find( 'No such file or directory' ) )

    #   test main - 25. check for single file name
    def test_main_singleFileName( self ):

        contentFile = tempfile.NamedTemporaryFile( delete=False )
        contentFile.write( b'abc;def;ghi;jkl\nmno;pqr;stu;vwx;yz\n' )
        contentFile.close()

        with patch( 'sys.stdout', new=StringIO() ) as mockStdout:
            sys.argv = [ 'cut', '--fields=1,3-4', '--delimiter=;', contentFile.name ]
            cut.main()

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
            cut.main()

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
                cut.main()

        #   sys.stderr.write( '[debug] result: \'' + mockStdout.getvalue() + '\'\n' )
        self.assertTrue( 'acef\ngikl\nmoqr\nsuwx\n' == mockStdout.getvalue() )
        os.remove( contentFile.name )

    #   TODO: write one test case for --zero-terminated option

#	entry point

if __name__ == '__main__':
    unittest.main()

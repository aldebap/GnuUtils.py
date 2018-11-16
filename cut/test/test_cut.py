#!	/usr/bin/python3

################################################################################
#	test_cut.py  -  Nov-15-2018 by aldebap
#
#	Unit tests for the Python version of GNU Linux cut utility
################################################################################

from io import StringIO
from unittest.mock import patch
import unittest

import cut

#   Unit tests class

class test_cut( unittest.TestCase ):
    def test_withoutOptions( self ):
        with patch( 'sys.stderr', new=StringIO() ) as mockStderr:
            with self.assertRaises( SystemExit ) as exit:
                cut.main()
            self.assertEqual( exit.exception.code, 2 )
            self.assertTrue( -1 != mockStderr.getvalue().find( 'you must specify a list of bytes, characters, or fields' ) )

#	entry point

if __name__ == '__main__':
    unittest.main()

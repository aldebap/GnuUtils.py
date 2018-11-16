#!	/usr/bin/python

################################################################################
#	test_cut.py  -  Nov-15-2018 by aldebap
#
#	Unit tests for the Python version of GNU Linux cut utility
################################################################################

import unittest
#import cut

#   Unit tests class

class test_cut( unittest.TestCase ):
    def test_withoutOptions( self ):
#        cut.main()
        self.assertTrue( True )

#	entry point

if __name__ == '__main__':
    unittest.main()

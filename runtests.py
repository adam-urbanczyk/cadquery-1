import sys
from tests import *
import cadquery
import unittest

#if you are on python 2.7, you can use -m uniitest discover.
#but this is required for python 2.6.6 on windows. FreeCAD0.12 will not load
#on py 2.7.x on win
suite = unittest.TestSuite()

suite.addTests(unittest.TestLoader().loadTestsFromTestCase(TestCadQuery.TestCadQuery))

if __name__ == '__main__':
    result = unittest.TextTestRunner().run(suite)
    sys.exit(not result.wasSuccessful())

import unittest

import testIn2post


suite = unittest.TestSuite(unittest.makeSuite(testIn2post.TestIn2post))


if __name__ == '__main__':
    result = unittest.TextTestRunner(verbosity=2).run(suite)
    sys.exit(not result.wasSuccessful())

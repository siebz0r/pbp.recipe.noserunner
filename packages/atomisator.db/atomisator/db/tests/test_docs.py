import unittest
import doctest
import os

# you can add variables here, that will be available 
# in the doctests

test_dir = os.path.dirname(__file__)
package_dir = os.path.split(test_dir)[0]

def doc_suite(test_dir):
    """Returns a test suite, based on doctests found in /doctest."""
    suite = []
    globs = globals()

    flags = (doctest.ELLIPSIS | doctest.NORMALIZE_WHITESPACE |
             doctest.REPORT_ONLY_FIRST_FAILURE)

    doctest_dir = os.path.join(package_dir, 'docs')

    # filtering files on extension
    docs = [os.path.join(doctest_dir, doc) for doc in
            os.listdir(doctest_dir) if doc.endswith('.txt')]

    for test in docs:
        suite.append(doctest.DocFileSuite(test, optionflags=flags, 
                                          globs=globs,
                                          module_relative=False))

    return unittest.TestSuite(suite)

def test_suite():
    """Returns the test suite."""
    return doc_suite(test_dir)

if __name__ == '__main__':
    unittest.main(defaultTest='test_suite')


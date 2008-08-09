import os
from nose.tools import *
from atomisator.filters import StopWords

def test_stop():
    
    stopfile = os.path.join(os.path.dirname(__file__), 
                            'words.txt')

    sw = StopWords()
    entry = {'title': 'the title', 
             'description': 'viagra info'}
    entries = []
    entry = sw(entry, entries, stopfile)
    assert_equals(entry, None)

    entry = {'title': 'the title', 
             'description': 'info'}
    res = sw(entry, entries, stopfile)
    assert_equals(entry, res)



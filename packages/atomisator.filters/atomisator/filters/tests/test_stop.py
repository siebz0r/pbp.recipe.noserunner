import os

from atomisator.filters import StopWords

def test_stop():
    
    stopfile = os.path.join(os.path.dirname(__file__), 
                            'words.txt')

    sw = StopWords()
    entry = sw(entry, dbtable, stopfile)

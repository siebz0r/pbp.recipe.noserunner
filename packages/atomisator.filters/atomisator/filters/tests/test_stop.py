import os
from nose.tools import *
from atomisator.filters import StopWords
from atomisator.filters import BuzzWords
from atomisator.filters import Doublons

def test_stop():

    stopfile = os.path.join(os.path.dirname(__file__), 
            'words.txt')

    sw = StopWords()
    entry = {'title': 'the title', 
            'summary': 'viagra info'}
    entries = []
    entry = sw(entry, entries, stopfile)
    assert_equals(entry, None)

    entry = {'title': 'the title', 
            'summary': 'info'}
    res = sw(entry, entries, stopfile)
    assert_equals(entry, res)

def test_buzz():

    buzzfile = os.path.join(os.path.dirname(__file__), 
            'words.txt')

    bw = BuzzWords()
    entry = {'title': 'the title', 
            'summary': 'viagra info'}
    entries = []
    entry = bw(entry, entries, buzzfile)
    assert_equals(entry['title'], '[viagra] the title')

    entry = {'title': 'the title', 
            'summary': 'info'}
    res = bw(entry, entries, buzzfile)
    assert_equals(res, None)

def test_doublons():
    db = Doublons()
    entry = {'title': 'the title', 
            'summary': 'info'}
    class E:
        title = ''
        summary = ''

    e = E()
    e.summary = 'info'
    entries = [e]
    entry = db(entry, entries)
    assert_equals(entry, None)

    entry = {'title': 'the title', 
            'summary': 'info'}
    res = db(entry, [])
    assert_equals(res, entry)


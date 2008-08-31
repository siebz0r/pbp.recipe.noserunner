# -*- encoding: utf-8 -*-
# (C) Copyright 2008 Tarek Ziadé <tarek@ziade.org>
#
import os
from nose.tools import *

from atomisator.filters import StopWords
from atomisator.filters import BuzzWords
from atomisator.filters import Doublons
from atomisator.filters import ReplaceWords

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

    # based on regepx
    entry['summary'] = 'start with start'
    res = sw(entry, entries, stopfile)
    assert_equals(res, None)


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
        link = summary = title = url = ''

    e = E()
    e.summary = 'info'
    entries = [e]
    entry = db(entry, entries)
    assert_equals(entry, None)

    entry = {'title': 'the title', 
            'summary': 'info'}
    res = db(entry, [])
    assert_equals(res, entry)

def test_replace():
    rw = ReplaceWords()
    entry = {'title': 'the title', 'summary': 'info'}
    replfile = os.path.join(os.path.dirname(__file__), 
                            'replace.txt')
    res = rw(entry, [], replfile)
    assert_equals(res['title'], 'the tixxxtle')
    assert_equals(res['summary'], 'info sp')

    entry = {'title': 'the title', 
             'summary': 'info not interesting'}
    res = rw(entry, [], replfile)
    assert_equals(res['title'], 'the tixxxtle')
    assert_equals(res['summary'], 'info sp ')



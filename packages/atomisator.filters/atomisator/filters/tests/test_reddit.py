# -*- encoding: utf-8 -*-
# (C) Copyright 2008 Tarek Ziadé <tarek@ziade.org>
#
import urllib2
from atomisator.filters.reddit import RedditFollower
from nose.tools import *

class Url:

    headers = {'content-type': 'text/html; charset=utf-8'}
    def __init__(self,  d):
        self._data = d

    def read(self):
        return self._data

def setupurl():
    urllib2.old = urllib2.urlopen
    def open(*args):
        return Url('<html><body>yeah</body></html>')
    urllib2.urlopen = open

def teardownurl():
    urllib2.urlopen = urllib2.old
    del urllib2.old

@with_setup(setupurl, teardownurl)
def test_reddit():
    red = RedditFollower()
    e = {'summary': 
         '<a href="http://link">[link]</a> <a href="xxx">[comments]</a>'}
    entry = red(e, [])

    assert 'yeah' in entry['summary']


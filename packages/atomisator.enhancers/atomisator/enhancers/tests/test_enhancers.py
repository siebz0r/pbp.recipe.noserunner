from atomisator.enhancers import DiggComments
from nose.tools import *

def test_digg():
    
    class E:
        url = 'http://mail.python.org/pipermail/python-dev/2006-December/070323.html'
        summary = 'xxx'
    entry =  E()
    d = DiggComments()
    entry = d(entry)
    assert '<li>' in entry.summary


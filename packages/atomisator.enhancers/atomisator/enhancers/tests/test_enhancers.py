from atomisator.enhancers import DiggComments
from atomisator.enhancers import RelatedEntries
from atomisator.enhancers.digg import Digg

from nose.tools import *

def setup():
    class Story:
        id = u'9878756'

    def one(*args, **kw):
        return [Story()]
    
    global old, old2
    old = Digg.getStories
    Digg.getStories = one

    class Comment:
        content = 'good comment'

    def one_comment(*args, **kw):
        return [Comment()]
    
    old2 = Digg.getStoriesComments
    Digg.getStoriesComments = one_comment

def teardown():
    Digg.getStories = old
    Digg.getStoriesComments = old2

@with_setup(setup, teardown)
def test_digg():

    class E:
        url = 'http://mail.python.org/pipermail/python-dev/2006-December/070323.html'
        summary = 'xxx'
    entry =  E()
    d = DiggComments()
    entry = d(entry, [])
    assert '<li>' in entry.summary

def test_related():
    
    r = RelatedEntries()



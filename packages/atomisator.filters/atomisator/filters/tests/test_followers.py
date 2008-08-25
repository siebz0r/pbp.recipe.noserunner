# -*- encoding: utf-8 -*-
# (C) Copyright 2008 Tarek Ziadé <tarek@ziade.org>
#
import urllib2
from atomisator.filters.followers import RedditFollower, DeliciousFollower
from nose.tools import *

DATA = """
<html>
 <body>
    The simplest way to use this module is to call the urlopen function,
    which accepts a string containing a URL or a Request object (described
    below).  It opens the URL and returns the results as file-like
    object; the returned object has some extra methods described below.
    
    The OpenerDirector manages a collection of Handler objects that do
    all the actual work.  Each Handler implements a particular protocol or
    option.  The OpenerDirector is a composite object that invokes the
    Handlers needed to open the requested URL.  For example, the
    HTTPHandler performs HTTP GET and POST requests and deals with
    non-error returns.  The HTTPRedirectHandler automatically deals with
    HTTP 301, 302, 303 and 307 redirect errors, and the HTTPDigestAuthHandler
    deals with digest authentication.
    
    urlopen(url, data=None) -- basic usage is that same as original
    urllib.  pass the url and optionally data to post to an HTTP URL, and
    get a file-like object back.  One difference is that you can also pass
    a Request instance instead of URL.  Raises a URLError (subclass of
    IOError); for HTTP errors, raises an HTTPError, which can also be
    treated as a valid response.
    
    build_opener -- function that creates a new OpenerDirector instance.
    will install the default handlers.  accepts one or more Handlers as
    arguments, either instances or Handler classes that it will
    instantiate.  if one of the argument is a subclass of the default
    handler, the argument will be installed instead of the default.
    
    install_opener -- installs a new opener as the default opener.

    HTTPRedirectHandler
 </body>
</html>
"""

class Url:

    headers = {'content-type': 'text/html; charset=utf-8'}
    def __init__(self,  d):
        self._data = d

    def read(self):
        return self._data

def setupurl():
    urllib2.old = urllib2.urlopen
    def open(*args):
        return Url(DATA)
    urllib2.urlopen = open

def teardownurl():
    urllib2.urlopen = urllib2.old
    del urllib2.old

@with_setup(setupurl, teardownurl)
def test_reddit():
    red = RedditFollower()
    e = {'summary': 
         '<a href="http://link">[link]</a> <a href="xxx">[comments]</a>',
         'title': ('HTTPRedirectHandler and HTTPDigestAuthHandler' 
                   ' (and more)')}
    entry = red(e, [])
    assert 'HTTPRedirectHandler' in entry['summary']

@with_setup(setupurl, teardownurl) 
def test_delicious():
    delicious = DeliciousFollower()
    
    e = {'comments': 
            'http://delicious.com/url/45bb751bb4dd1f4a291c91cf31c43511',
         'title': ('HTTPRedirectHandler and HTTPDigestAuthHandler' 
                   ' (and more)'),
         'link': 'http://link'}
    entry = delicious(e, [])
    assert 'HTTPRedirectHandler' in entry['summary']


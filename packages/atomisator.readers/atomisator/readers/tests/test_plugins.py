from nose.tools import *

import os
from atomisator.readers.html import HTML
from atomisator.readers.folder import Folder
from atomisator.readers.twitter import Twitter

test_dir = os.path.dirname(__file__)

def test_html():

    web_page = os.path.join(test_dir, 'page.html')
    parser = HTML()
    content = parser('file://'+web_page)

    assert_equals(len(content), 1)
    content = content[0]
    assert_equals(content['title'], 'the title')
    assert content['summary'].startswith('The content')

    extractor = (r'<div class="entry">.*?<h1>(.*?)</h1>'
                  '(.*?)</div>')

    content = parser('file://'+web_page,
                     extractor)

    assert_equals(len(content), 2)
    assert_equals(content[1]['title'], 'title 2')
    assert_equals(content[1]['summary'], 'this is entry two')

    extractor = (r'<div class="entry">.*?<h1>.*?</h1>'
                  '(.*?)</div>')

    content = parser('file://'+web_page,
                     extractor)

    assert_equals(len(content), 2)
    assert_equals(content[1]['title'], 'the title')
    assert_equals(content[1]['summary'], 'this is entry two')

def test_folder():

    content_folder = os.path.join(test_dir, 'data')
    parser = Folder()
    result = parser(content_folder)


    assert_equals(len(result), 2)
    assert_equals(result[1]['summary'], 'some things\n\n')

def test_twitter():

    twitt_file = os.path.join(os.path.dirname(__file__), 'twitter.xml')
    engine = Twitter()
    excl = 'chipnowacek, pydanny,SnowWrite'
    entries = engine(open(twitt_file), excl)
    assert_equals(len(entries), 8)

def test_yahoo():
    pass



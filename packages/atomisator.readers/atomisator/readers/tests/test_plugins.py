from nose.tools import *

import os
from atomisator.readers import HTML 

def test_html():

    web_page = os.path.join(os.path.dirname(__file__), 'page.html') 
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


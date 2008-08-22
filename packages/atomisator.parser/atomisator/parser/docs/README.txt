=================
atomisator.parser
=================

The parser knows how to return a feed content, with
the `parse` function, available as a top-level function::

    >>> from atomisator.parser import Parser

This function takes the feed url and returns an iterator
over its content. A second parameter can specify a maximum
number of entries to return. If not given, it is fixed to 10::

    >>> import os
    >>> res = Parser()(os.path.join(test_dir, 'sample.xml'))
    >>> res
    <itertools.imap ...>

Each item is a dictionary that contain the entry::

    >>> entry = res.next()
    >>> entry['title']
    u'CSSEdit 2.0 Released'

The keys available are:

    >>> keys = sorted(entry.keys())
    >>> list(keys)
    ['id', 'link', 'links', 'summary', 'summary_detail', 'tags', 
     'title', 'title_detail']

Dates are changed into datetime::

    >>> type(entry['date'])
    >>>

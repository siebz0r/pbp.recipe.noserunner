=================
atomisator.parser
=================

The parser knows how to return a feed content, with
the `parse` function, available as a top-level function::

    >>> from atomisator.parser import parse

This function takes the feed url and returns an iterator
on its content. A second parameter can specify how
much entries has to be returned before the iterator is 
exhausted. If not given, it is fixed to 10::

    >>> import os
    >>> res = parse(os.path.join(test_dir, 'sample.xml'))
    >>> res
    itertools.islice ...>

Each item is a dictionnary that contain the entry::

    >>> entry = res.next()
    >>> entry['title']
    'SSEdit 2.0 Released'

The keys available are:

    >>> keys = sorted(entry.keys())
    >>> list(keys)
    ['id', 'link', 'links', 'summary', 'summary_detail', 'tags', 
     'title', 'title_detail']

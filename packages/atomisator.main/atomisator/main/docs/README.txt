===============
atomisator.main
===============

The package has two main features:

1. it loads the feeds described into `atomisator.cfg`.
2. it generates a feed

    >>> from atomisator.main import load_feeds
    >>> load_feeds()
    Parsing feed sample1.xml
    Parsing feed sample2.xml
    0 entries read.

    >>> from atomisator.main import generate_feed
    >>> generate_feed()
    Writing feed in atomisator.xml
    Feed ready.



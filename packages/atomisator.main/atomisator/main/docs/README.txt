===============
atomisator.main
===============

The package has two main features:

1. it loads the feeds described into `atomisator.cfg`.
2. it generates a feed

    >>> from atomisator.main import load_feeds
    >>> load_feeds(test_conf)
    Parsing feed ...digg.xml
    10 entries read.
    Parsing feed ...tarek.xml
    10 entries read.
    Parsing feed ...pp.xml
    10 entries read.
    30 total.

    >>> from atomisator.main import generate_feed
    >>> generate_feed(test_conf)
    Writing feed in atomisator.xml
    Feed ready.



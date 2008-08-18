===============
atomisator.main
===============

The package has two main features:

1. it loads the feeds described into `atomisator.cfg`.
2. it generates a feed

    >>> from atomisator.main.run import load_feeds
    >>> load_feeds(test_conf)
    Reading source ...digg.xml
    1 entries read.
    Reading source ...tarek.xml
    4 entries read.
    Reading source ...pp.xml
    18 entries read.
    23 total.

    >>> from atomisator.main.run import generate_feed
    >>> generate_feed(test_conf)
    Writing feed in atomisator.xml
    Feed ready.



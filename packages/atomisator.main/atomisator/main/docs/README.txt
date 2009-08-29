===============
atomisator.main
===============

The package has two main features:

1. it loads the feeds described into `atomisator.cfg`.
2. it generates a feed

    >>> from atomisator.main.core import DataProcessor
    >>> processor = DataProcessor(test_conf)
    >>> processor.load_data()
    Loading...

    >>> processor.generate_data()
    Preparing enhancers.
    Enhancing: related, digg
    Writing outputs.Rendering: rss.
    Output ready.



=======================
atomisator.main package
=======================

This package is part of the `Python Expert Programming` book  written by 
Tarek Ziadé.


For more information, go to http://atomisator.ziade.org

Atomisator merge several feeds into on single feed,
storing entries in a database to avoid doublons.

To use it, create an atomisator.cfg file somewhere::

    [atomisator]

    sites = 
        http://tarekziade.wordpress.com/atom
        http://digg.com/rss2.xml

    database = sqlite:///Users/tarek/atomisator.db

    file = /Users/tarek/atomisator.xml
    title = meta
    description = Automatic feed created by Atomisator.
    link =  http://atomisator.ziade.org/example

You can then call the `atomisator` tool over it::

    $ atomisator /path/to/atomisator.cfg

It will generate the atomisator.xml file.

You can also call separately the process that fills the database::

    $ load_feeds /path/to/atomisator.cfg

Then generate the xml file in another process::

    $ generate_feed /path/to/atomisator.cfg


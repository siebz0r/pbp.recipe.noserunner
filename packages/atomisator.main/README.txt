=======================
atomisator.main package
=======================

This package is part of the `Expert Python Programming` book  written by 
Tarek Ziadé.


For more information, go to http://atomisator.ziade.org

Atomisator merge several feeds into on single feed,
storing entries in a database to avoid doublons.

To use it, create an atomisator.cfg file somewhere, using the
-c option::

    $ atomisator -c atomisator.cfg

A default configuration file will be generated, that looks like this::

    [atomisator]

    # put here the feeds you wish to parse
    sites = 
        http://tarekziade.wordpress.com/atom
        http://digg.com/rss2.xml

    # put here the database location
    database = sqlite:///atomisator.db

    # this is the file that will be generated
    file = atomisator.xml

    # infos that will appear in the generated feed. 
    title = meta
    description = Automatic feed created by Atomisator.
    link =  http://atomisator.ziade.org/example

You can then call the `atomisator` tool using this file with the -f option::

    $ atomisator -f /path/to/atomisator.cfg

You can specify the path as a free argument as well::

    $ atomisator /path/to/atomisator.cfg  

It will generate the atomisator.xml file, after reading the sources.

You can also call separately the process that fills the database::

    $ atomisator -r -f /path/to/atomisator.cfg

In this case the feed generation will not occur. 

The -g option can be used to generate the xml file on its own:

    $ atomisator -g -f /path/to/atomisator.cfg

This is useful to read sources and generate the feed within different process and different time basis.


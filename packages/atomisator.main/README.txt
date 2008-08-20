=======================
atomisator.main package
=======================

This package is part of the `Expert Python Programming` book  written by Tarek Ziadé.

For more information, go to http://atomisator.ziade.org

.. contents::

The big picture
===============

`Atomisator` is a feed framework. Its purpose it to provide an engine to build
a feed by merging several sources of data. 

.. figure:: http://ziade.org/atomisator/atomisator.png
    :alt: The big picture
    
    The big picture.    

Building a feed is done by two processes :

- 1, 2, 3 : Reading and filtering data
- 4, 5, 6 : Building the feed

Reading and filtering data is done in three steps :

1. read the data sources
2. filter the collected data
3. store them into a dedicated database

Building the feed is done in threesteps :

4. read the database
5. enhance the entries with dynamic data
6. render the feed

The nice thing about readers, filters and enhancers is that they
are plugins. This means you can write your own plugins and
use Atomisator to build your own custom feed generator.

Quick Start
===========

To use it, create a configuration file somewhere, using the
-c option::

    $ atomisator -c atomisator.cfg

A default configuration file will be generated, that looks like this::

    [atomisator]

    # put here the feeds you wish to parse
    sources = 
        rss     http://tarekziade.wordpress.com/atom
        rss     http://digg.com/rss2.xml

    # put here the filters you want to use
    filters =
        doublons

    # put here the enhancers you want to use
    enhancers =
     
    # put here the database location
    database = sqlite:///atomisator.db

    # this is the file that will be generated
    file = atomisator.xml

    # infos that will appear in the generated feed. 
    title = meta
    description = Automatic feed created by Atomisator.
    link =  http://atomisator.ziade.org/example

You can then build your feed by using this configuration file with the -f option::

    $ atomisator -f /path/to/atomisator.cfg
    Reading source http://tarekziade.wordpress.com/atom
    10 entries read.
    Reading source http://digg.com/rss/index.xml
    40 entries read.
    50 total.
    Writing feed in atomisator.xml
    Feed ready.

You can specify the path as a free argument as well::

    $ atomisator /path/to/atomisator.cfg  

`Atomisator` will then generate an `atomisator.xml` file, after reading the sources.

You can also call separately the process that fills the database::

    $ atomisator -r -f /path/to/atomisator.cfg

In this case the feed generation will not occur. 

The -g option can be used to generate the xml file on its own::

    $ atomisator -g -f /path/to/atomisator.cfg

This is useful to read sources and generate the feed within different process and different time basis.

For other useful options, run::

    $ atomisator --help

Available plugins
=================

XXX to be written

How to write a plugin
=====================

XXX to be written




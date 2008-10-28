==========
Atomisator
==========

The big picture
===============

`Atomisator` is a generic data processing framework that works
with plugins. Its purpose is to provide an engine to build a 
data processing task. 

1. You provide the plugins that does the work.
2. You describe how to combine them in a configuration file.
3. Atomisator does the work.

Atomisator works in two steps:

- Collecting: data is acquired and filtered, then stored.
- Rendering: stored data is enhanced and rendered.

.. figure:: http://ziade.org/atomisator/atomisator.png
    :alt: The big picture
    
    The big picture.    

Quick Start
===========

Let's build a Planet with Atomisator !

To do it, create a configuration file somewhere, 
using the -c option::

    $ atomisator -c atomisator.cfg

A default configuration file is generated, 
that looks like this (comments where removed)::

    [atomisator]

    sources = 
        rss http://tarekziade.wordpress.com/atom 
        rss http://digg.com/rss/index.xml

    filters =

    enhancers =

    outputs =
        rss atomisator.xml http://atomisator.ziade.org/example "Meta feed" "Automatic feed created by Atomisator." 

    database = sqlite:///atomisator.db

This file can be interpreted by Atomisator, with the -f option::

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

`Atomisator` will read the sources, then generate 
an `atomisator.xml` file.

Two phases process
::::::::::::::::::

You can also call separately the process that fills the database::

    $ atomisator -r -f /path/to/atomisator.cfg

In this case the feed generation will not occur. 

The -g option can be used to generate the xml file on its own::

    $ atomisator -g -f /path/to/atomisator.cfg

This is useful to read sources and generate the feed within different process and different time basis.

For other useful options, run::

    $ atomisator --help

More details
============
 
As said earlier, Atomisator works in two steps:

- Collecting: data is acquired and filtered, then stored.
- Rendering: stored data is enhanced and rendered.

Collecting data
:::::::::::::::

Collecting data is done by reading (1) and filtering (2) data.
These two steps are done by invoking plugins.

For example, if you want to get some data from an RSS feed,
you can use the `rss` plugin that is provided by default,
and use it in an Atomisator configuration file::

    ...
    sources = 
        rss     http://tarekziade.wordpress.com/atom
        rss     http://digg.com/rss2.xml
    ...

This tells Atomisator to look for the `rss` reader plugin,
and invoke it with the url as an argument. The plugin has to 
return entries.

The next step is to filter collected entries. Filtering means
either changing the data on the fly, either discarding it.

For example, if you want to remove all entries that contains
particular expressions, you can use the `stopwords` plugin
that is provided by default and use it in an Atomisator
configuration file::

    ...
    filters =
        stopwords   word_list.txt
    ...

This tells atomisator to look for the `stopwords` plugin and
to invoke it with collected entries. The plugin uses the word
list in the pointed file, and look of the data match the 
given regular expressions. If so, the data is discarded.

Rendering data
::::::::::::::

After the data has been collected, it is stored in a database.
You can now render it, using the enhancers (5) and the outputs
(6) filters. 

For example, if you want to see if an entry correspond to a 
web page that has been `digged`, you can use the `digg` plugin::

    ...
    enhancers =
        digg
    ...

This plugin will be invoked by Atomisator, and it will inject 
Digg comments in the data by querying Digg.com via RPC.

Last the output plugins are called for the final step. For
example the `rss` output plugin will render the data in an
RSS 2.0 XML file::

    ...
    outputs =
        rss atomisator.xml http://atomisator.ziade.org/example meta "Automatic feed created by Atomisator." 
    ...
    
All the arguments following the plugin name will be sent to it,
besides the entries.

Available plugins
=================

XXX to be written

How to write a plugin
=====================

XXX to be written




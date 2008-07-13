=======================
atomisator.main package
=======================

.. contents::

Atomisator merge several feeds into on single feed,
storing entries in a database to avoid doublons.

To use it, create an atomisator.cfg file in your home::

    [atomisator]

    sites = 
        http://tarekziade.wordpress.com/atom

    database = sqlite:///Users/tarek/atomisator.db

    file = /Users/tarek/atomisator.xml
    title = meta
    description =
    link =

You can then call the `atomisator` tool::

    $ atomisator

It will generate the proper atomisator.xml file.


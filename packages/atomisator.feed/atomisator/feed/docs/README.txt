==============
atmisator.feed
==============

Generates a feed using a template::

    >>> from atomisator.feed import Generator
    >>> class Entry(object):
    ...     pass
    >>> class Tag(object):
    ...     value = 'value'
    >>> from tempfile import mktemp
    >>> tmpfilename = mktemp()
    >>> generator = Generator()
    >>> entry1 = Entry()
    >>> entry1.summary = 'summary1'
    >>> entry1.title = 'title1'
    >>> entry1.link = 'http://link1'
    >>> entry1.updated = 'date1'
    >>> entry1.tags = [Tag()]
    >>> generator([entry1],
    ...           (tmpfilename, 'http://link', 'the feed'))
    >>> print open(tmpfilename).read()
    <?xml version="1.0" encoding="utf-8"?>
    <rss version="2.0" xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#">
    <channel>
    <title><![CDATA[the feed]]></title>
    <description><![CDATA[]]></description>
    <link>http://link</link>
    <language>en</language>
    <copyright>Copyright 2008, Atomisator</copyright>
    <pubDate>Sat, 15 Mar 2008 00:15:05 +0200</pubDate>
    <lastBuildDate>Sat, 15 Mar 2008 00:15:05 +0200</lastBuildDate>
      <item>
        <title><![CDATA[title1]]></title>
        <description><![CDATA[summary1]]></description>
        <link><![CDATA[http://link1]]></link>
        <pubDate>date1</pubDate>
        <category>value</category>
      </item>
    </channel>
    </rss>
    <BLANKLINE>
    <BLANKLINE>


The same with unicode:

    >>> entry1.title = u'hééé'
    >>> generator([entry1],
    ...           (tmpfilename, 'http://link', 'the feed'))

Delete the temp file

    >>> import os
    >>> os.remove(tempfile)

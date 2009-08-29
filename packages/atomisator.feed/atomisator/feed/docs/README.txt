==============
atmisator.feed
==============

Generates a feed using a template::

    >>> from atomisator.feed import Generator
    >>> class Entry(object):
    ...     pass
    >>> class Tag(object):
    ...     value = u'valuè'
    >>> from tempfile import mktemp
    >>> tmpfilename = mktemp()
    >>> generator = Generator()
    >>> entry1 = Entry()
    >>> entry1.summary = u'sûmmary1'
    >>> entry1.title = u'tîtlé1'
    >>> entry1.link = u'http://link1'
    >>> entry1.updated = u'date1'
    >>> entry1.tags = [Tag()]
    >>> generator([entry1],
    ...           (tmpfilename, u'http://link', u'thééé feed'))
    >>> print open(tmpfilename).read()
    <?xml version="1.0" encoding="utf-8"?>
    <rss version="2.0" xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#">
    <channel>
    <title><![CDATA[thÃ©Ã©Ã© feed]]></title>
    <description><![CDATA[]]></description>
    <link>http://link</link>
    <language>en</language>
    <copyright>Copyright 2008, Atomisator</copyright>
    <pubDate>Sat, 15 Mar 2008 00:15:05 +0200</pubDate>
    <lastBuildDate>Sat, 15 Mar 2008 00:15:05 +0200</lastBuildDate>
      <item>
        <title><![CDATA[tÃ®tlÃ©1]]></title>
        <description><![CDATA[sÃ»mmary1]]></description>
        <link><![CDATA[http://link1]]></link>
        <pubDate>date1</pubDate>
        <category>valuÃ¨</category>
      </item>
    </channel>
    </rss>
    <BLANKLINE>
    <BLANKLINE>


Delete the temp file

    >>> import os
    >>> os.remove(tmpfilename)

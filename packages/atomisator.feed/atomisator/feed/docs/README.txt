==============
atmisator.feed
==============

Generates a feed using a template::

    >>> from atomisator.feed import generate
    >>> print generate('feed', 'the feed', 'http://link')
    <?xml version="1.0" encoding="utf-8"?>
    <rss version="2.0" xmlns:rdf="...">
    <channel>
    <title>feed</title>
    <description>the feed</description>
    <link>http://link</link>
    <language>en</language>
    ...
      <item>
        <title><![CDATA[Python 2.6alpha1 and 3.0alpha3 released]]></title>
        <description><![CDATA[Summary goes here]]></description>
        <link><![CDATA[http://www.python.org/news]]></link>
        <pubDate></pubDate>
      </item>
    </channel>
    </rss>
    <BLANKLINE>
    <BLANKLINE>


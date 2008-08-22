from feedparser import parse as feedparse
from feedparser import _parse_date
from itertools import islice
from itertools import imap

class Parser(object):
    """
    Returns entries of an RSS or Atom feed.

    Usage:
    
        [atomisator]
        sources =     
            rss url

    """

    def _filter_entry(self, entry):
        for field in ('date', 'updated', 'published'):
            if field in entry:
                entry[field] = _parse_date(entry[field])

        entry['links'] = [link['href'] for link in entry['links']]
        if 'summary' not in entry:
            if 'content' in entry:
                entry['summary'] = entry['content'][0]['value']
        return entry

    def __call__(self, url, size=-1):
        result = feedparse(url)
        if size != -1:
            return islice(imap(self._filter_entry, 
                               result['entries']), size)
        else:
            return imap(self._filter_entry, result['entries'])


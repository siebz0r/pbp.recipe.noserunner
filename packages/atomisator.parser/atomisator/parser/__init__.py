from feedparser import parse as feedparse
from feedparser import _parse_date
from itertools import islice
from itertools import imap
from datetime import datetime

class Parser(object):
    """
    Returns entries of an RSS or Atom feed.

    Usage:
    
        [atomisator]
        sources =     
            rss url [size] name

    """

    def _filter_entry(self, entry):
        keys = entry.keys()
        for field in ('date_parsed', 'updated_parsed', 'published_parsed'):
            if field in keys:
                del entry[field]

        for field in ('date', 'updated', 'published'):
            if field in keys:
                parsed = _parse_date(entry[field])
                if parsed is None:
                    del entry[field]
                else:
                    entry[field] = datetime(*parsed[:6])

        if 'date' not in keys and 'published' in keys:
            entry['date'] = entry['published']

        entry['links'] = [l for l in [link.get('href') for link in entry['links']]
                          if l is not None]
        if 'summary' not in entry:
            if 'content' in entry:
                entry['summary'] = entry['content'][0]['value']
        if self.name is not None:
            entry['title'] = u'[%s] %s' % (self.name, entry['title'])
        return entry

    def __call__(self, url, *args):
        if len(args) == 0:
            self.name = None
            size = -1
        else:
            try:
                size = int(args[0])
                self.name = u' '.join(args[1:])
            except ValueError:
                self.name = u' '.join(args)
                size = -1
        result = feedparse(url)
        if size != -1:
            return islice(imap(self._filter_entry, 
                               result['entries']), size)
        else:
            return imap(self._filter_entry, result['entries'])


from feedparser import parse as feedparse
from itertools import islice
from itertools import imap

class Parser(object):

    def _filter_entry(self, entry):
        entry['links'] = [link['href'] for link in entry['links']]
        return entry

    def __call__(self, url, size=-1):
        """Returns entries of the feed."""
        result = feedparse(url)
        if size != -1:
            return islice(imap(self._filter_entry, 
                               result['entries']), size)
        else:
            return imap(self._filter_entry, result['entries'])


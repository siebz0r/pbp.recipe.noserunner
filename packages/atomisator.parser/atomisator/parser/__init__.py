from feedparser import parse as feedparse
from itertools import islice
from itertools import imap

class Parser(object):

    def _filter_entry(self, entry):
        entry['links'] = [link['href'] for link in entry['links']]
        return entry

    def __call__(self, url, size=10):
        """Returns entries of the feed."""
        result = feedparse(url)
        return islice(imap(self._filter_entry, 
                           result['entries']), size)
        


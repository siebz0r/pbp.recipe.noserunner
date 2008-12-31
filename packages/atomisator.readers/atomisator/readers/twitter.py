import os
import urllib2
from os.path import join

from atomisator.parser import Parser

class Twitter(Parser):
    """Query twitter search service

    This plugin takes two parameters:
     - the query (mandatory)
     - a list of twitter users to exclude

    """
    root_query = 'http://search.twitter.com/search.atom?q=%s'

    def _filter(self, entry, excluded_users):
        author = entry['author']
        nick = author.split()[0]
        if nick in excluded_users:
            return True
        title = entry['title']
        elements = title.split()
        if len(elements) == 0:
            return True
        if elements[0].startswith('@'):
            to_nick = elements[0][1:]
            if elements[0][1:] in excluded_users:
                return True
        return False

    def __call__(self, query, excluded_users=None):
        if isinstance(query, str) and not query.startswith('file'):
            query = self.root_query % query
        entries = Parser.__call__(self, query)
        if excluded_users is None:
            return entries
        
        excluded_users = [e.strip() for e in excluded_users.split(',')]
        return [e for e in entries if not self._filter(e, excluded_users)]


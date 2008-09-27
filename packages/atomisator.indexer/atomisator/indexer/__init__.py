# -*- encoding: utf-8 -*-
# (C) Copyright 2008 Tarek Ziadé <tarek@ziade.org>
#
from afpy.xap.indexer import index_document


class Indexer(object):  
    """Indexes the content in a Xapian database"""

    def __call__(self, entry, entries, db=None):
        # todo
        docid = entry['link']
        text = '%s %s' % (entry['title'], entry['summary'])
        index_document(docid, text)
        return entry


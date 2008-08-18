from Cheetah.Template import Template
import Cheetah.Filters

import os
from cStringIO import StringIO

from atomisator.db.core import get_entries
from atomisator.db.mappers import entry

tmpl = os.path.join(os.path.dirname(__file__), 'rss2.tmpl')

def generate(title, description, link, enhancers=None, size=50):
    """Generates items."""
    keys = set(entry.c.keys() + ['links', 'tags'])

    if enhancers is None:
        enhancers = [] 
    
    # crappy transformers, get ridd of it
    def _dict(new_entry):
        res = {}
        for key in keys:
            res[key] = getattr(new_entry, key)
        return res

    def _str(entry):
        entry = _dict(entry)
        for key, value in entry.items():
            if isinstance(value, unicode):
                entry[key] = value.encode('utf8')
        return entry
  
    # see if this is the best way to load entries
    entries = get_entries()
    
    def _enhance(entry):
        for e, args in enhancers:
            entry = e(entry, entries, *args)
        return entry

    #entries = [_str(_enhance(e)) for e in entries[:size]]
    entries = [_enhance(e) for e in entries[:size]] 

    class Encode(Cheetah.Filters.Filter):
        def filter(self, val, **kw):
            if kw.has_key('encoding'):
                encoding = kw['encoding']
            else:
                encoding = 'utf8'
            if isinstance(val, unicode):
                val = val.encode(encoding)
            else:
                val = str(val)
            return val

    
    data = {'entries': entries, 
            'channel': {'title': title, 'description': description,
                        'link': link}}
    template = Template(open(tmpl).read(), searchList=[data], filter=Encode)
    return str(template)


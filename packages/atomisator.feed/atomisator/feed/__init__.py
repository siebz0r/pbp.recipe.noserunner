from Cheetah.Template import Template
import Cheetah.Filters

import os
from cStringIO import StringIO

from atomisator.db.core import get_entries

tmpl = os.path.join(os.path.dirname(__file__), 'rss2.tmpl')

def generate(title, description, link, enhancers=None, size=50):
    """Generates items."""
    if enhancers is None:
        enhancers = [] 
    
    entries = get_entries().all()
    
    # preparing entries
    for e, args in enhancers:
        if hasattr(e, 'prepare'):
            e.prepare(entries)

    def _enhance(entry):
        for e, args in enhancers:
            entry = e(entry, *args)
        return entry

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


from Cheetah.Template import Template
import os
from atomisator.db import get_entries
from atomisator.db.mappers import entry
from itertools import islice

tmpl = os.path.join(os.path.dirname(__file__), 'rss2.tmpl')

def generate(title, description, link, size=20):
    """Generates items."""
    def _dict(new_entry):
        res = {}
        for key in entry.c.keys():
            res[key] = getattr(new_entry, key)
        return res

    entries = islice(get_entries(), size)
    data = {'entries': [_dict(e) for e in entries], 
            'channel': {'title': title, 'description': description,
                        'link': link}}
    
    template = Template(open(tmpl).read(), searchList=[data])
    return str(template)


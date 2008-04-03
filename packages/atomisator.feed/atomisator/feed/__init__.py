from Cheetah.Template import Template
import os
from atomisator.db import get_entries
from itertools import islice

tmpl = os.path.join(os.path.dirname(__file__), 'rss2.tmpl')

def generate(title, description, link, size=20):
    """Generates items."""
    def _dict(entry):
        res = {}
        for key in entry.c.keys():
            res[key] = getattr(entry, key)
        return res

    entries = islice(get_entries(), size)
    data = {'entries': [_dict(entry) for entry in entries], 
            'channel': {'title': title, 'description': description,
                        'link': link}}
    
    template = Template(open(tmpl).read(), searchList=[data])
    return str(template)


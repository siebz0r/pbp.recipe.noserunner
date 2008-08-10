from Cheetah.Template import Template
import os

from atomisator.db.core import get_entries
from atomisator.db.mappers import entry

tmpl = os.path.join(os.path.dirname(__file__), 'rss2.tmpl')

def generate(title, description, link, size=50):
    """Generates items."""
    def _dict(new_entry):
        res = {}
        for key in entry.c.keys():
            res[key] = getattr(new_entry, key)
        return res

    def _str(entry):
        entry = _dict(entry)
        for key, value in entry.items():
            if isinstance(value, unicode):
                entry[key] = value.encode('utf8')
        return entry
    
    entries = [_str(e) for e in get_entries(size=size)]
    data = {'entries': entries, 
            'channel': {'title': title, 'description': description,
                        'link': link}}
    
    template = Template(open(tmpl).read(), searchList=[data])
    return str(template)


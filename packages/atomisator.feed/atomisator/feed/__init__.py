import tempita

import os
from cStringIO import StringIO

tmpl = os.path.join(os.path.dirname(__file__), 'rss2.tmpl')

class Generator(object):

    def __call__(self, entries, args, size=50):
        """Generates items."""
        filename = args[0]
        link = args[1]
        title = args[2]
        description = ' '.join(args[3:])

        entries = entries[:size]

        data = {'entries': entries,
                'channel': {'title': title,
                            'description': description,
                            'link': link}}
        template = tempita.Template(unicode(open(tmpl).read()))

        content = template.substitute(**data)
        f = open(filename, 'w')
        try:
            f.write(content.encode('utf-8'))
        finally:
            f.close()


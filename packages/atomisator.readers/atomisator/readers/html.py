from urllib2 import urlopen
import re

options = re.M |re.S|re.I|re.U

# presets
TITLE = r'<header>.*?<title>(.*?)</title>.*?</header>'
BODY = r'<body>(.*?)</body>'
SINGLE = r'%s.*?%s' % (TITLE, BODY)

class HTML(object):
    """
    Returns entries that matches the expression.

    Usage:

        [atomisator]
        sources = 
            html url expression

    If expression is None, returns the whole page 
    as one entry.

    Otherwise returns an iterator over items that
    matches the regular expression.

    The expression must be in form:

        ...(1)...(2)...

    where (1) is a group for the entry title,
    and (2) for the entry content.

    if one single group is provided, it is the entry
    content, and the title of the page is used for the 
    entry title.

    """

    def __call__(self, url, *expression):
        expression = ' '.join(expression)
        if expression == '':
            expression = SINGLE
        content = urlopen(url).read()
        content = content.decode('utf8')
        page_title = re.findall(TITLE, content, options)
        page_title = len(page_title) > 0 and page_title[0] or ''
        def _entry(e):
            groups = e.groups()
            if len(groups) == 0:
                return None
            if len(groups) == 1:
                return {'summary': groups[0].strip(), 
                        'title': page_title,
                        'url': url}
            
            return {'summary': groups[1].strip(), 
                    'title': groups[0].strip(), 
                    'url': url}

        return [_entry(e) for e in 
                re.finditer(expression, content, options)]
        

from BeautifulSoup import BeautifulSoup, Comment
from sgmllib import SGMLParser

TAGS = ('p', 'i', 'strong', 'b', 'u', 'a', 'h1', 'h2', 'h3', 'br', 'img')
ATTRS = ('href', 'src', 'title')

class Html2Txt(SGMLParser):
    def reset(self):
        SGMLParser.reset(self)
        self.pieces = []

    def handle_data(self, text):
        self.pieces.append(text)

    def handle_entityref(self, ref):
        if ref == 'amp':
            self.pieces.append("&")

    def output(self):
        return ' '.join(self.pieces)

class RedditFollower(object):
    """
    Will detect a reddit-like post and fill the summary
    with an extract of the target page 
    by following the link.
    """
    pattern = r'<a href="(.*)">\[link\]</a> <a href=".*?">\[comments\]</a>'

    def __call__(self, entry, entries):
        summary = entry.get('summary', '')
        link = re.search(self.pattern, summary, options) 
        if link is None:
            return entry

        # reddit-like detected
        link = link.groups()[0]

        # let's get a sample of the link
        sample, encoding = self._get_sample(link)
        if sample is not None:
            extract = '<div>Extract from link :</div> <p>%s</p><br/>' % \
                    sample.decode(encoding)            
            entry['summary'] = extract + entry['summary']
        return entry
 
    def _clean(self, value, size):
        """clean an html page"""
        soup = BeautifulSoup(value)

        # removes unwanted tags (security+style)
        for comment in soup.findAll(
            text = lambda text: isinstance(text, Comment)):
            comment.extract()
        for tag in soup.findAll(True):
            if tag.name not in TAGS:
                tag.hidden = True
            tag.attrs = [(attr, val) for attr, val in tag.attrs
                        if attr in ATTRS]

        # loads and render 
        parser = Html2Txt()
        parser.reset()
        parser.feed(soup.body.renderContents())
        parser.close()
        out = parser.output().strip()

        return out[:size] + (len(out) > size and '...' or '')

    def _get_sample(self, link, size=300):
        """get the page, extract part of it if it is some text"""
        charset = 'utf-8'
        try:
            page = urllib2.urlopen(link)
            if 'content-type' in page.headers.keys():
                content_type = page.headers['content-type'].split(';')
                type_ = content_type[0].strip().lower()
                if type_ not in ('text/html', 'text/plain', 'test/rst'):
                    return None, None
                if len(content_type) > 1:
                    charset = content_type[1].split('=')[-1]
            content = page.read()

        except urllib2.HTTPError:
            return None, None

        body = self._clean(content, size)
        return body, charset


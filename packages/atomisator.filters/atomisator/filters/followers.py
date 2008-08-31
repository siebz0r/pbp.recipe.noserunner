# -*- encoding: utf-8 -*-
# (C) Copyright 2008 Tarek Ziadé <tarek@ziade.org>
#
from sgmllib import SGMLParser
import socket
#import probstat
import re
import urllib2
import string

from BeautifulSoup import BeautifulSoup, Comment

options = re.DOTALL | re.UNICODE | re.MULTILINE | re.IGNORECASE
TAGS = set(('p', 'i', 'strong', 'b', 'u', 'a', 'h1', 'h2', 'h3', 'br', 'img'))
ATTRS = set(('href', 'src', 'title'))
DELETE_TAGS = ('script',)
DIV_BLOGS = set(('article-body', 'knol-content', 'post-body',
                 'post', 'entry-content', 'post-chapo', 'content'))
 
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

class _Follower(object):

    _marker = '.'

    def _detect(self, entry):
        """returns a link if detected
        None otherwise
        """
        raise NotImplementedError

    def __call__(self, entry, entries):
        link = self._detect(entry)
        if link is None:
            return entry

        entry['link'] = link

        # let's get a sample of the link
        sample, encoding = self._get_sample(entry['title'], link)
        if sample is not None:
            extract = '<div>Extract from link :</div> <p>%s</p><br/>' % sample
            entry['summary'] = (extract.decode(encoding, 'ignore') + 
                                entry.get('summary', u'') +
                                self._marker)
        return entry
 
    def _soup(self, value):
        soup = BeautifulSoup(value)

        # removes unwanted tags (security+style)
        for comment in soup.findAll(
            text = lambda text: isinstance(text, Comment)):
            comment.extract()

        for tag in soup.findAll(True):
            # trying a few patterns
            if tag.name == 'div':
                for attr, val in tag.attrs:
                    if attr == 'class':
                        vals = val.split()
                        for wanted in DIV_BLOGS:
                            for val in vals:
                                if val == wanted:
                                    # caught a pattern
                                    c = tag.renderContents()
                                    return self._soup('<body>%s</body>' % c)
            
            if tag.name == 'p' and 'meta' in [v for n, v in tag.attrs]:
                tag.extract()
                continue
            if tag.name in DELETE_TAGS:
                tag.extract()
                continue

            if tag.name not in TAGS:
                tag.hidden = True

            tag.attrs = [(attr, val) for attr, val in tag.attrs
                        if attr in ATTRS]
        if soup.body is not None: 
            return soup.body.renderContents()
        else:
            return soup.renderContents()
    
    def _clean(self, value):
        """cleans an html page."""
        # loads and render
        parser = Html2Txt()
        parser.reset()
        parser.feed(self._soup(value))
        parser.close()
        return parser.output().strip()

    def _words(self, data):
        data = ''.join([w for w in data if w in string.ascii_letters+' '])
        return [(len(w.strip()), w.strip()) for w in data.split()]

    #def _combos(self, lists):
    #    if lists == []:
    #        return []
    #    return probstat.Cartesian(lists)
    #    if len(lists) == 1:
    #        return [[x] for x in lists[0]]
    #    
    #    res = [[i] + j for j in self._combos(lists[1:]) for i in lists[0]]
    #    print res
    #    return res

    #def _ampl_combo(self, lists):
    #    for seq in self._combos(lists):
    #        start, end = min(seq), max(seq)
    #        yield end-start, start, end     

    def _extract(self, title, content, size):
        """will try to find the best extract
        
        XXX should be better, experimenting
        """
        content_size = len(content)
        delta = size / 2

        for l, word in reversed(sorted(self._words(title))):
            positions = [m.start() for m in re.finditer(word, content)]
            if positions != []:
                pos = positions[0]
                # now findig the position of the last dot
                dots = [m.start() for m in re.finditer('\. ', content[:pos])]
                if dots == []:
                    start = pos
                else:
                    start = dots[-1] + 1
                if start + delta > content_size:
                    end = content_size
                else:
                    end = start + delta
         
                return '...' + content[start:end] + '...'
        return '...' + content[:size] + '...'

        # finding the positions for all the words
        #def _indexes(word, content):
        #    return [e.start() for e in re.finditer(word.strip(), 
        #            content, options)]
        
         
        #positions = [_indexes(w, lcontent) for w in self._words(title) 
        #             if _indexes(w, lcontent) != []]
                
        # creating all the combos, and calculating the
        # amplitude for each
        #combos = sorted(self._ampl_combo(positions))
        #if combos == []:
        #    return content[:size]
        #ampl, start, end = combos[0]
        #if ampl > size:
        #    end = start + size
            
        #return '...' + content[start:end] + '...'
 
    def _get_sample(self, title, link, size=1000):
        """get the page, extract part of it if it is some text.
        
        tries to find the words of the title, to extract 
        the most meaningful part of the page.
        """
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

        except (urllib2.HTTPError, urllib2.URLError, socket.timeout):
            return None, None

        body = self._clean(content)
        return self._extract(title.encode(charset), body, size), charset

class RedditFollower(_Follower):
    """
    Will detect a reddit-like post and fill the summary
    of the entry with an extract of the target page 
    by following the link.

    The filter tries to pick up the best extract out
    of the page.
    """
    pattern = r'submitted .*? <br /> <a href="(.*?)">\[link\]</a> <a href=".*?">\[.*?comments\]</a>$'

    def _detect(self, entry):
        summary = entry.get('summary', '')

        link = re.search(self.pattern, summary, options) 
        if link is None:
            return None

        # reddit-like detected
        return link.groups()[0]

class DeliciousFollower(_Follower):
    """
    Will detect a delicious-like post and fill the summary
    of the entry with an extract of the target page 
    by following the link.

    The filter tries to pick up the best extract out
    of the page.
    """
    def _detect(self, entry):
        title_detail = entry.get('title_detail')
        if title_detail is not None and 'delicious.com' in title_detail['base']:
            return entry['link']
        comments = entry.get('comments', '')
        if comments.startswith('http://delicious.com/url/'):
            return entry['link']
        return None


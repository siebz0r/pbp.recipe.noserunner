# -*- encoding: utf-8 -*-
# (C) Copyright 2008 Tarek Ziadé <tarek@ziade.org>
#
from sgmllib import SGMLParser
#import probstat
import re
import urllib2
import string

from BeautifulSoup import BeautifulSoup, Comment

options = re.DOTALL | re.UNICODE | re.MULTILINE | re.IGNORECASE
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

class _Follower(object):

    def _detect(self, entry):
        """returns a link if detected
        None otherwise
        """
        raise NotImplementedError

    def __call__(self, entry, entries):
        link = self._detect(entry)
        if link is None:
            return entry

        # let's get a sample of the link
        sample, encoding = self._get_sample(entry['title'], link)
        if sample is not None:
            extract = '<div>Extract from link :</div> <p>%s</p><br/>' % sample
            entry['summary'] = extract.decode(encoding, 'ignore') + entry.get('summary', u'')
        return entry
 
    def _clean(self, value):
        """cleans an html page."""
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
            positions = list(reversed([m.start() for m in re.finditer(word, content)]))
            if positions != []:
                pos = positions[0]
                if pos > delta:
                    start = pos - delta
                else:
                    start = 0
                if pos + delta < content_size:
                    end = pos + delta
                else:
                    end = content_size

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
 
    def _get_sample(self, title, link, size=300):
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

        except urllib2.HTTPError:
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
    pattern = r'<a href="(.*)">\[link\]</a> <a href=".*?">\[comments\]</a>'

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
        comments = entry.get('comments', '')
        if not comments.startswith('http://delicious.com/url/'):
            return None
        return entry['link']


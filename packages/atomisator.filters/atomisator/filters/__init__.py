import re
import urllib2

_files = {}

options = re.DOTALL | re.UNICODE | re.MULTILINE | re.IGNORECASE

class FileFilter(object):

    def _comp(self, line):
        line = line.strip()
        return line, re.compile(line, options)

    def _read_file(self, path):
        if path in _files:
            return _files[path]
        _files[path] = [self._comp(line) for line in
                        open(path).readlines()
                        if line.strip() != '']
        return _files[path]

    def _get_texts(self, entry):
        return entry['title'], entry.get('summary', '')

    def _match(self, entry, path):
        for w, exp in self._read_file(path):
            for t in self._get_texts(entry):
                if exp.search(t) is not None:
                    return w
        return None

class StopWords(FileFilter):
    """
    Filter off entries that matches regular expressions.
    Expressions are given in a file, one per line.
    The file path is provided as argument.
    """ 
    def __call__(self, entry, entries, path):
        if self._match(entry, path) is not None:
            return None
        return entry

class ReplaceWords(FileFilter):
    """
    Replace one expression to another one.
    Expressions are given in a file.
    Each line is the matching expression, 
    followed by the replacement string.
    Elements are separated by the ":::" expression.

    The file path is provided as argument.
    """
    def _replace(self, entry, path):
        for w, exp, repl in self._read_file(path):
            for key in ('summary', 'title'):
                entry[key] = exp.sub(repl, entry[key])
        return entry

    def _comp(self, line):
        line = line.strip()
        spl = line.split(':::')
        if len(spl) == 1:
            exp, repl = spl[0], ''
        else:
            exp, repl = spl
        return exp, re.compile(exp, options), repl

    def __call__(self, entry, entries, path):
        return self._replace(entry, path) 

class BuzzWords(FileFilter):
    """
    Keep only the entries that matches regular expressions.
    Expressions are given in a file, one per line.
    The file path is provided as argument.
    """ 

    def __call__(self, entry, entries, path):
        """Keeps entries based on keywords"""
        w = self._match(entry, path)
        if w is not None:
            entry['title'] = '[%s] %s' % (w, entry['title'])
            return entry
        return None

class Doublons(object):
    """
    Entries are unique by their url, but sometimes you can have doublons.
    
    This filter filters off entries that are already in the database.
    By looking at the summaries.

    XXX todo : use levensthein distance here

    """ 
    def _clean(self, st):
        return st.lower().strip()
    
    def __call__(self, entry, entries):
        summary = self._clean(entry.get('summary', ''))
        for e in entries:
            if summary == self._clean(e.summary):
                return None
        return entry

class Spam(object):
    """
    Tries to remove spamy entries.
    """
    def __call__(self, entry, entries):
        if 'summary' in entry and entry['summary'].strip() == '':
            return None
        return entry

class AutoTag(FileFilter):
    """
    Automatically tag entries when words or regular expression
    from a file are found into this entry.
    """ 
    def _match(self, entry, path):
        res = []
        for w, exp in self._read_file(path):
            for t in self._get_texts(entry):
                if exp.search(t) is not None:
                    res.append(w)
        return res

    def __call__(self, entry, entries, path):
        """Keeps entries based on keywords"""
        for w in self._match(entry, path):
            if 'tags' not in entry:
                entry['tags'] = [{'term': w}]
            else:
                if w not in [e['term'] for e in entry.tags]:
                    entry['tags'].append({'term': w})
        return entry

#re_body = re.compile(r'<body>(.*?)</body>', options)
from BeautifulSoup import BeautifulSoup, Comment

valid_tags = 'p i strong b u a h1 h2 h3 pre br img'.split()
valid_attrs = 'href src'.split()
from sgmllib import SGMLParser

class html2txt(SGMLParser):
  def reset(self):
    SGMLParser.reset(self)
    self.pieces = []

  def handle_data(self, text):
    self.pieces.append(text)

  def handle_entityref(self, ref):
    if ref=='amp':
      self.pieces.append("&")

  def output(self):
    return " ".join(self.pieces)

def _clean(value, size):
    soup = BeautifulSoup(value)
    for comment in soup.findAll(
        text = lambda text: isinstance(text, Comment)):
        comment.extract()
    for tag in soup.findAll(True):
        if tag.name not in valid_tags:
            tag.hidden = True
        tag.attrs = [(attr, val) for attr, val in tag.attrs
                    if attr in valid_attrs]
    parser = html2txt()
    parser.reset()
    parser.feed(soup.body.renderContents())
    parser.close()
    out = parser.output().strip()
    return out[:size] + (len(out) > size and '...' or '')

def _get_sample(link, size=300):
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

    body = _clean(content, size)
    return body, charset

class RedditFollower(object):
    """
    Will detect a reddit-like post and fill the summary
    by following the link.
    """
    pattern = r'<a href="(.*)">\[link\]</a> <a href=".*?">\[comments\]</a>'

    def __call__(self, entry, entries):
        summary = entry.get('summary', '')
        link = re.search(self.pattern, summary, options) 
        if link is None:
            return entry
        link = link.groups()[0]
        # this is a reddit post, they are empty,
        # let's add some content
        sample, encoding = _get_sample(link)
        if sample is not None:
            extract = '<div>Extract from link :</div> <p>%s</p><br/>' % \
                    sample.decode(encoding)            
            entry['summary'] = extract + entry['summary']
        return entry
 

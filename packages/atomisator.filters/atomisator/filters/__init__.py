import re

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
        return entry['title'], entry['summary']

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
    Filter off entries that are already in the database.
    """ 
    def _clean(self, st):
        return st.lower().strip()
    
    def __call__(self, entry, entries):
        summary = self._clean(entry['summary'])
        for e in entries:
            if summary == self._clean(e.summary):
                return None
        return entry

class Spam(object):
    """
    Tries to remove spamy entries.
    """
    def __call__(self, entry, entries):
        if entry['summary'].strip() == '':
            return None
        return entry

class AutoTag(FileFilter):
    """
    Automatically tag entries when words or regular expression
    from a file are found into this entry.
    """ 

    def __call__(self, entry, entries, path):
        """Keeps entries based on keywords"""
        w = self._match(entry, path)
        if w is not None:
            if 'tags' not in entry:
                entry['tags'] = [w]
            elif w not in entry:
                entry['tags'].append(w)
        return entry


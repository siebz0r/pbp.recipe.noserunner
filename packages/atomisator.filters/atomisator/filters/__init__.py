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
   
    def __call__(self, entry, entries, path):
        """Filter off an entry if one of its words is in the stop file"""
        if self._match(entry, path) is not None:
            return None
        return entry

class ReplaceWords(FileFilter):
   
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

    def __call__(self, entry, entries, path):
        """Keeps entries based on keywords"""
        w = self._match(entry, path)
        if w is not None:
            entry['title'] = '[%s] %s' % (w, entry['title'])
            return entry
        return None

class Doublons(object):

    def _clean(self, st):
        return st.lower().strip()
    
    def __call__(self, entry, entries):
        summary = self._clean(entry['summary'])
        for e in entries:
            if summary == self._clean(e.summary):
                return None
        return entry

class Spam(object):

    def __call__(self, entry, entries):
        if entry['summary'].strip() == '':
            return None
        return entry



_files = {}

class FileFilter(object):

    def _read_file(self, path):
        if path in _files:
            return _files[path]
        list_ = [w.strip().lower() 
                 for w in open(path).readlines()
                 if w.strip() != '']
        list_.sort()
        _files[path] = set(list_)
        return _files[path]

class StopWords(FileFilter):
   
    def __call__(self, entry, entries, file):
        """Filter off an entry if one of its words is in the stop file"""
        # we don't read the database entries here
        words = self._read_file(file)
        fields = ('title', 'summary', 'description')
        for f in fields:
            if f not in entry:
                continue
            for w in entry[f].split():
                w = w.strip().lower()
                if w in words:
                    return None
        return entry

class BuzzWords(FileFilter):

    def __call__(self, entry, entries, file):
        """Filter off an entry if one of its words is in the stop file"""
        # we don't read the database entries here
        words = self._read_file(file)
        fields = ('title', 'summary', 'description')
        for f in fields:
            if f not in entry:
                continue
            for w in entry[f].split():
                w = w.strip().lower()
                if w in words:
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


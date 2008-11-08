# -*- encoding: utf-8 -*-
# (C) Copyright 2008 Tarek Ziadé <tarek@ziade.org>
#
import re

_files = {}
options = re.DOTALL | re.UNICODE | re.MULTILINE | re.IGNORECASE

class FileFilter(object):

    def __init__(self):
        self._cached_expressions = {}

    def _comp(self, line):
        line = line.strip()
        return line, re.compile(line, options)

    def _get_texts(self, entry):
        return entry['title'], entry.get('summary', '')

    def _match(self, entry, path):
        if path not in self._cached_expressions:
            patterns = [l for l in open(path).read().split('\n')
                        if l.strip() != '']
            expr = re.compile('|'.join(patterns), options)
            self._cached_expressions[path] = expr
        text = '\n'.join(self._get_texts(entry))
        return self._cached_expressions[path].search(text) 

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
        if path not in self._cached_expressions:
            lines = [self._comp(l) 
                     for l in open(path).read().split('\n')
                     if l.strip() != '']
            self._cached_expressions[path] = lines
        for key in ('summary', 'title'):
            for comp, repl in self._cached_expressions[path]:
                entry[key] = comp.sub(repl, entry[key]) 
        return entry

    def _comp(self, line):
        line = line.strip()
        spl = line.split(':::')
        if len(spl) == 1:
            exp, repl = spl[0], ''
        else:
            exp, repl = spl
        return re.compile(exp, options), repl

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
        m = self._match(entry, path)
        if m is not None:
            entry['title'] = '[%s] %s' % (m.group(), entry['title'])
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
        if st is None:
            return None
        return st.lower().strip()
    
    def __call__(self, entry, entries):
        link = self._clean(entry.get('link', ''))
        summary = self._clean(entry.get('summary', ''))
        for e in entries:
            if link == self._clean(e.link):
                return None
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
    def __call__(self, entry, entries, path):
        """Keeps entries based on keywords"""
        match = self._match(entry, path)
        if match is not None:
            entry['tags'] = [{'term': tag} for tag in  match.group()]
        return entry


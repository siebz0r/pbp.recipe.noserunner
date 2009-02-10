# -*- encoding: utf-8 -*-
# (C) Copyright 2008 Tarek Ziadé <tarek@ziade.org>
#
import re
import BeautifulSoup
import difflib

from atomisator.filters.guess_language import guessLanguage
from atomisator.filters.levenshtein import StringMatcher

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

    def __call__(self, entry, entries, ratio=''):
        link = self._clean(entry.get('link', ''))
        summary = self._clean(entry.get('summary', ''))
        matcher = StringMatcher()
        matcher.set_seq1(summary)
        for e in entries:
            if link == self._clean(e.link):
                return None
            matcher.set_seq2(self._clean(e.summary))
            ratio = matcher.quick_ratio()
            if ratio > 0.75:
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

class GuessLang(object):
    """"Filter out entries that are not in the chosen
    languages"""
    def __call__(self, entry, entries, langs='en'):
        langs = langs.split(',')
        text = '%s %s' % (entry.get('summary', ''), entry.get('title', ''))
        lang = guessLanguage(text)
        if lang not in langs:
            return None
        return entry

class UrlDiff(object):
    """Will create a diff with the previous version if founded in the
    database"""
    def _html_to_text(self, html):
        soup = BeautifulSoup.BeautifulSoup(html)
        # getting all comments and scripts
        def _filter(node):
            if isinstance(node, (BeautifulSoup.Comment,
                                 BeautifulSoup.Declaration)):
                return True
            return False
        comments = soup.findAll(text=_filter)
        # deleting all comments
        [comment.extract() for comment in comments]

        for s in soup.findAll('script'):
            s.extract()

        # get only the text from the <body>
        body = soup.body(text=True)

        # in text is the text of the html-doc
        return ''.join(body).strip()

    def _get_diff(self, text1, text2):
        text1 = self._html_to_text(text1).splitlines(True)
        text2 = self._html_to_text(text2).splitlines(True)
        res = ''.join(difflib.unified_diff(text1, text2)).split('\n')[2:]
        def _filter(line):
            if line.startswith('@'):
                return ''
            return line
        return '\n'.join([_filter(line) for line in res if line.strip() != ''])

    def __call__(self, entry, entries):

        url = entry['url']
        for existing in entries:
            if existing['url'] == url:
                entry['diff'] = self._get_diff(entry['summary'],
                                              existing['summary'])
                break
        return entry


import os
from os.path import join

class Folder(object):
    """Scans a folder and retrieve the content.

    This plugin knows how to extract the indexable
    content from text files, pdf files, etc.

    """
    def _extract(self, filepath):
        try:
            content = open(filepath).read()
        except IOError:
            return None
        content = content.decode('utf8', 'ignore')
        return {'title': filepath,
                'link': filepath,
                'summary': content}

    def __call__(self, path, recursive=True):
        if not os.path.exists(path) or not os.path.isdir(path):
            return []  
        
        results = []    # no generator for multiprocessor
        for root, dirs, files in os.walk(path):
            for file_ in files:
                if os.path.splitext(file_)[-1] not in ('.txt',):
                    continue
                res = self._extract(join(root, file_))
                if res is not None:
                    results.append(res)
        return results


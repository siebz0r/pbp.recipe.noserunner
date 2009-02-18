import os
from os.path import join
from urllib import quote_plus
from urllib import FancyURLopener

import simplejson

DEFAULT_CONFIG = {"appid": "b.U92LXV34GLljD7X8G9OwPyiN1CZJC_f8EeBpmNLzkuFhxxmrk2Jya2WDy3ku_Z5cdZj686",
                  "email": "",
                  "org": "test",
                  "agent": "Atomisator",
                  "commercial": False,
                  "purpose": "To give Atomisator a way to search into Yahoo.",
                  "version": "v1",
                  "vertical": "web",
                  "lang": "en",
                  "region": "us",
                  "start": 0,
                  "count": 10,
                  "uri": "http://boss.yahooapis.com/ysearch"}

SEARCH_API_URL = '%(uri)s/%(vertical)s/%(version)s/%(command)s'
SEARCH_PARAMS = ('?start=%(start)d&count=%(count)d&lang=%(lang)s&region=%(region)'
                 's&appid=%(appid)s')
URL = SEARCH_API_URL + SEARCH_PARAMS

class YahooOpener(FancyURLopener):
    version = ''


class Yahoo(object):
    """Query Yahoo BOSS search service

    This plugin takes two parameters:
     - the query (mandatory)
     - the yahoo configuration

    """

    # XXXX todo : include those
    def params(self, params):
        """ Takes a dictionary of key, value pairs and generates a cgi parameter/argument string """
        p = ""
        for k, v in params.iteritems():
            p += "&%s=%s" % (quote_plus(k), quote_plus(v))
        return p

    def __call__(self, command, config=None):

        if config is not None:
            DEFAULT_CONFIG.update(config)

        DEFAULT_CONFIG['command'] = quote_plus(command)
        url = URL % DEFAULT_CONFIG

        res = YahooOpener().open(url)
        if res.headers['content-type'] != 'application/json':
            return

        res = simplejson.loads(res.read())
        entries = res['ysearchresponse']['resultset_web']

        def _f(e):
            e['link'] = e['url']
            e['summary'] = e['abstract']
            return e

        return [_f(e) for e in entries]


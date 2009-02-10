import os
import urllib2
from os.path import join
from urllib import quote_plus

import simplejson
#from yos.crawl import rest

DEFAULT_CONFIG = {"appid": "BossDemo",
                  "email": "boss-feedback@yahoo-inc.com",
                  "org": "Yahoo! Inc.",
                  "agent": "Atomisator",
                  "commercial": False,
                  "purpose": "To give Atomisator a way to search into Yahoo.",
                  "version": "1.0",
                  "vertical": "web",
                  "lang": "en",
                  "region": "us",
                  "uri": "http://boss.yahooapis.com/ysearch"}

#vertical, version, quote_plus(command), start, count, lang, region) + params(more)

SEARCH_API_URL = ('%(uri)s/%(vertical)s/v%(version)/%(command)s?start=%(start)d&count=%(count)d'
                  '&lang=%s&region=%(region)s&appid=%(appid)s')

class Yahoo(object):
    """Query Yahoo BOSS search service

    This plugin takes two parameters:
     - the query (mandatory)
     - the yahoo configuration

    """

    def params(d):
        """ Takes a dictionary of key, value pairs and generates a cgi parameter/argument string """
        p = ""
        for k, v in d.iteritems():
            p += "&%s=%s" % (quote_plus(k), quote_plus(v))
        return p

    def __call__(self, query, config):

        #url = SEARCH_API_URL %
        res = search(query, count=count)

        #return rest.load_json(url)



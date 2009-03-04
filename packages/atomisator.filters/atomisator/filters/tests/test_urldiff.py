# -*- encoding: utf-8 -*-
# (C) Copyright 2008 Tarek Ziad\xe9 <tarek@ziade.org>
#
import os
from nose.tools import *

from atomisator.filters import UrlDiff

here = os.path.dirname(__file__)

summary1 = open(os.path.join(here, 'old.html')).read()
summary2 = open(os.path.join(here, 'new.html')).read()

diff = u"\n [modifier] Liens externes\n (fr) Site officiel\n-(en) Site officiel du langage Python\n  Portail de l\u2019informatique\n\n- Derni\xe8re modification de cette page le 9 f\xe9vrier 2009 \xe0 22:38.\n+ Derni\xe8re modification de cette page le 22 octobre 2008 \xe0 20:04.\n Droit d'auteur : Tous les textes sont disponibles sous les termes de la licence de documentation libre GNU (GFDL).\n Wikipedia\xae est une marque d\xe9pos\xe9e de la Wikimedia Foundation, Inc., organisation de bienfaisance r\xe9gie par le paragraphe 501(c)(3) du code fiscal des \xc9tats-Unis.\n Politique de confidentialit\xe9"

s1 = open(os.path.join(here, 's1.html')).read()
s2 = open(os.path.join(here, 's2.html')).read()

class Entry:
    def __init__(self, link, summary):
        self.link = link
        self.summary = summary

def test_urldiff():

    # if the entry is found add a diff
    d = UrlDiff()

    old = Entry('xxx', summary1)

    new = {'link': 'xxx',
           'summary': summary2}

    res = d(new, [old])
    assert_equals(res['diff'], diff)

def test_urldiff2():

    # if the entry is found add a diff
    d = UrlDiff()
    old = Entry('xxx', s1)
    new = {'link': 'xxx', 'summary': s2}
    res = d(new, [old])
    assert_equals(len(res['diff']) > 100)


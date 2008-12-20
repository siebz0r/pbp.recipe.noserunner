# -*- encoding: utf-8 -*-
# (C) Copyright 2008 Tarek Ziadé <tarek@ziade.org>
#
from atomisator.filters import GuessLang

fr = """
"Une pulvérisation invisible d'Ubik et vous bannirez la 
crainte obsédante, irrésistible, de voir le monde entier se 
transformer en lait tourné".

Qu'est-ce qu'Ubik ? Une marque de bière ? Une sauce salade ? 
Une variété de café ? Un médicament ? Peut-être... Et quel 
est donc ce monde où les portes et les douches parlent et 
n'obéissent aux ordres qu'en retour de monnaie sonnante et 
trébuchante ? Un monde où les morts vivent en animation 
suspendue et communiquent avec les vivants dans les
"moratoriums". C'est dans cet univers que Glen Runciter a 
créé un organisme de protection contre les intrusions 
mentales : télépathie, précognition, para-kinésie. Joe Chip, 
un de ses employés, est chargé de monter un groupe de 
"neutraliseurs" de pouvoirs "psy", afin de lutter contre 
ce qui semble être une menace de grande envergure. 
"""

en = """
This is the #1 reference and source for anyone wanting to 
print T-shirts or decorate garments. How to Print T-Shirts 
for Fun and Profit covers the details of screen printing, 
heat transfers, and the inkjet-to-garment process in an 
easy-to-follow, step-by-step manner. First published in 
1978, and just updated with the latest information in 2008, 
this book has sold more than 140,000 copies. Long known as 
The T-Shirt Printer's Bible, this latest edition lays out 
the technical processes, how to start a shop, how to market 
and sell T-shirts, a complete source directory, and plans 
for simple printing equipment. Whether you are a hobbyist or 
want to start a profitable business, How to Print T-Shirts 
for Fun and Profit is the best, most updated book available. 
"""

de = """
Die Chroniken von Narnia - Prinz Kaspian schreibt die Geschichte 
des ersten Teils fort und entführt den Zuschauer erneut in 
die magische Parallelwelt. Grosses Kino mit epischen 
Qualitäten und visionärer Kraft; wenn auch die 
fragwürdige Haltung nicht verschwiegen werden soll.
"""

def test_lang():

    entry = {'summary': fr, 'title': ''}
    guesser = GuessLang()
    
    assert guesser(entry, []) is None
    assert guesser(entry, [], 'de') is None
    assert guesser(entry, [], 'fr') is not None
    assert guesser(entry, [], 'en,de') is None

    entry['summary'] = en
    assert guesser(entry, []) is not None
    assert guesser(entry, [], 'de') is None
    assert guesser(entry, [], 'fr') is None
    assert guesser(entry, [], 'en,de') is not None

    entry['summary'] = de
    assert guesser(entry, []) is None
    assert guesser(entry, [], 'de') is not None
    assert guesser(entry, [], 'fr') is None
    assert guesser(entry, [], 'en,de') is not None




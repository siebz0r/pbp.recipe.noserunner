# -*- encoding: utf-8 -*-
# (C) Copyright 2008 Tarek Ziadé <tarek@ziade.org>
""" 
Mail output plugin.
"""
from email.MIMEText import MIMEText

class Mail(object):
    """Will send an alert by mail"""

    def __call__(self, entries, enhancers, args):
        
        # a mail is built, using MimeText
        msg = MIMEText() 


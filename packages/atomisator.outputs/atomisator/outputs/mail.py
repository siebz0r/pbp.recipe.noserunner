# -*- encoding: utf-8 -*-
# (C) Copyright 2008 Tarek Ziadé <tarek@ziade.org>
""" 
Mail output plugin.
"""
from email.MIMEText import MIMEText
from smtplib import SMTP 
from datetime import datetime 

DEFAULT_BODY_TMPL = """\
Atomisator has triggered an alert. Check out for:

%(entries)s
"""

DEFAULT_ENTRY_TMPL = """\
  * %(title)s: %(url)s
"""

class Mail(object):
    """Will send an alert by mail
    
    Arguments:
        - emails to send the alert to, separated by commas
        - subject (optional)
        - from mail (optional)
        - path to a template file for the body (optional)
        - path to a template file for the entry (optional)
        - smtp server (optional)
        - smtp port (optional)
    """

    def __call__(self, entries, args):
        
        # do not send a mail on empty entries
        if len(entries) == 0:
            return
        values = {'tos': args[0].split(',')}

        optionals = (('subject', 'Atomisator alert'),
                     ('from', 'admin@atomisator'),
                     ('body_template', DEFAULT_BODY_TMPL),
                     ('entry_template', DEFAULT_ENTRY_TMPL),
                     ('smtp_server', 'localhost'),
                     ('smtp_port', '25')
                     )
        
        for pos, default in enumerate(optionals):
            pos += 1
            name, default = default
            values[name] = len(args) > pos and args[pos] or default
    
        # lines
        lines = [values['entry_template'] % entry for entry in entries]
        
        # mail content
        text = values['body_template'] % \
                {'entries': '\n'.join(lines)}

        # a mail is built, using MimeText
        msg = MIMEText(text)
        msg['Subject'] = values['subject']
        msg['To'] = ','.join(values['tos'])
        msg['From'] = values['from']
        msg['Date'] = datetime.now().isoformat()
        msg = msg.as_string() 

        # let's send it
        smtp = SMTP(values['smtp_server'], values['smtp_port'])
        smtp.sendmail(values['from'], values['tos'], msg)



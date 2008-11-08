import smtplib
from nose.tools import *
import os

class _SMTP(object):
    msgs = []
    def __init__(self, *args, **kw):
        pass
    def close(self):
        pass

    def sendmail(self, from_, tos, msg, **kw):
        self.msgs.append({'from': from_,
                          'tos': tos, 'msg': msg})

smtplib.SMTP = _SMTP

import datetime

class _datetime(object):
    @classmethod
    def now(cls):
        return cls
    @classmethod
    def isoformat(cls):
        return 'NOW'
datetime.datetime = _datetime

# required because nose dicovering loads mail...
# so the patch for SMTP was not applied
import atomisator.outputs.mail
reload(atomisator.outputs.mail)
from atomisator.outputs.mail import Mail 

waited = """\
Content-Type: text/plain; charset="us-ascii"
MIME-Version: 1.0
Content-Transfer-Encoding: 7bit
Subject: Atomisator alert
To: tarek@ziade.org
From: admin@atomisator
Date: NOW

Atomisator has triggered an alert. Check out for:

  * this: http://here

"""

mail_config = os.path.join(os.path.dirname(__file__), 'email.cfg')

def test_email():

    email = Mail()

    class Entry(object):
        pass

    entry = Entry()
    entry.link = 'http://here'
    entry.title = 'this'

    args = (mail_config,)
    entries = [entry]
    email(entries, args)

    assert len(_SMTP.msgs) == 1
    msg = _SMTP.msgs[0]

    assert msg['from'] == 'admin@atomisator'
    assert_equals(msg['tos'], ['tarek@ziade.org'])

    assert_equals(msg['msg'], waited)


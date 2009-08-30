# coding: utf-8
from atomisator.filters import Doublons


SUMMARY1 = """
Python has a good reputation for tasks like systems programming, network programming, and scripting, but Python for the web is becoming red hot. Part of this has to do with the very popular web framework Django, that was developed at a newspaper to help quickly create Content Management Sites. . Another reason is that Google App Engine–Google’s Cloud Computing offering for developers–only exposes a Python API.

If you are new to Python Web Development, then I’d recommend Django, as it is ideal for building CMS-type applications, social networking websites, and blogs. On the other hand, If you want a hacker’s framework, you might want to give Pylons a look.

Please note: By hacker, I am referring to the kind of hacker Eric Raymond refers to when he writes, “Becoming a hacker will take intelligence, practice, dedication, and hard work. Therefore, you have to learn to distrust attitude and respect competence of every kind. Hackers won’t let posers waste their time, but they worship competence — especially competence at hacking, but competence at anything is valued.”
"""

SUMMARY2 = """
Python has a good reputation for tasks like systems programming, network programming, and scripting, but Python for the web is becoming red hot. Part of this has to do with the very popular web framework Django, that was developed at a newspaper to help quickly create Content Management Sites. . Another reason is that Google App Engine–Google’s Cloud Computing offering for developers–only exposes a Python API.

If you are new to Python Web Development, then I’d recommend Django, as it is ideal for building CMS-type applications, social networking websites, and blogs. On the other hand, If you want a hacker’s framework, you might like to give Pylons a look.

Please notice that : By hacker, I am referring to the kind of hacker Eric Raymond refers to when he writes, “Becoming a hacker will take intelligence, practice, dedication, and hard work. Therefore, you have to learn to distrust attitude and respect competence of every kind. Hackers won’t let posers waste their time, but they worship competence — especially competence at hacking, but competence at anything is valued.”
"""

SUMMARY3 = """
Revision control (also known as version control (system)
(VCS), source control or (source) code management (SCM))
is the management of multiple revisions of the same unit of
information. It is most commonly used in engineering and
software development to manage ongoing development of
digital documents like application source code, art
resources such as blueprints or electronic models, and other
projects that may be worked on by a team of people. Changes
to these documents are usually identified by incrementing an
associated number or letter code, termed the "revision
number", "revision level", or simply "revision" and
associated historically with the person making the change.
A simple form of revision control, for example, has the
initial issue of a drawing assigned the revision number "1".
When the first change is made, the revision number is
incremented to
"2" and so on.
"""


class Entry(object):
    link = 'xxx'
    summary = ''

    def get(self, name, default):
        if not hasattr(self, name):
            return default
        return getattr(self, name)

entry1 = Entry()
entry1.summary = SUMMARY1

entry2 = Entry()
entry2.summary = SUMMARY2
entry2.link = 'XoX'

entry3 = Entry()
entry3.summary = SUMMARY3
entry3.link = 'XuC'

def test_doublons():

    d = Doublons()
    res = d(entry1, [entry2])
    assert res is None

    res = d(entry1, [entry3])
    assert res is not None



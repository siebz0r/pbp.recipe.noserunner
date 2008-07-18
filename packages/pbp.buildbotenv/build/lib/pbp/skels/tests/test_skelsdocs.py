# -*- coding: utf-8 -*-
# Copyright (c) 2008 Tarek Ziadé

# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program; see the file COPYING. If not, write to the
# Free Software Foundation, Inc., 675 Mass Ave, Cambridge, MA 02139, USA.
"""
Generic Test case for pbp.skels doctest
"""
__docformat__ = 'restructuredtext'
import shutil
import popen2
import unittest
import doctest
import sys
import os
from paste.script.command import run

from zope.testing import doctest

current_dir = os.path.abspath(os.path.dirname(__file__))

from os import chdir

def paster(args):
    try:
        run(args.split(' '))
    except SystemExit:
        pass

def rmdir(*args):
    dirname = os.path.join(*args)
    if os.path.isdir(dirname):
        shutil.rmtree(dirname)

def read_sh(cmd):
    _cmd = cmd
    old = sys.stdout 
    child_stdout_and_stderr, child_stdin = popen2.popen4(_cmd)
    child_stdin.close()
    return child_stdout_and_stderr.read()

def sh(cmd):
    _cmd = cmd
    print cmd
    # launch command 2 times to see what append and be able 
    # to test in doc tests
    os.system(_cmd)
    child_stdout_and_stderr, child_stdin = popen2.popen4(_cmd)
    child_stdin.close()
    print child_stdout_and_stderr.read()

def ls(*args):
    dirname = os.path.join(*args)
    if os.path.isdir(dirname):
        filenames = os.listdir(dirname)
        for filename in sorted(filenames):
            print filename
    else:
        print 'No directory named %s' % dirname

def cd(*args):
    dirname = os.path.join(*args)
    os.chdir(dirname)

def config(filename):
    return os.path.join(current_dir, filename)

def cat(*args):
    filename = os.path.join(*args)
    if os.path.isfile(filename):
        print open(filename).read()
    else:
        print 'No file named %s' % filename

def touch(*args, **kwargs):
    filename = os.path.join(*args)
    open(filename, 'w').write(kwargs.get('data',''))

execdir = os.path.abspath(os.path.dirname(sys.executable))
tempdir = os.getenv('TEMP','/tmp')

def doc_suite(test_dir, setUp=None, tearDown=None, globs=None):
    """Returns a test suite, based on doctests found in /doctest."""
    suite = []
    if globs is None:
        globs = globals()

    flags = (doctest.ELLIPSIS | doctest.NORMALIZE_WHITESPACE |
             doctest.REPORT_ONLY_FIRST_FAILURE)

    package_dir = os.path.split(test_dir)[0]
    if package_dir not in sys.path:
        sys.path.append(package_dir)

    doctest_dir = os.path.join(package_dir, 'doctests')

    # filtering files on extension
    docs = [os.path.join(doctest_dir, doc) for doc in
            os.listdir(doctest_dir) if doc.endswith('.txt')]

    for test in docs:
        suite.append(doctest.DocFileSuite(test, optionflags=flags, 
                                          globs=globs, setUp=setUp, 
                                          tearDown=tearDown,
                                          module_relative=False))

    return unittest.TestSuite(suite)

def test_suite():
    """returns the test suite"""
    return doc_suite(current_dir)

if __name__ == '__main__':
    unittest.main(defaultTest='test_suite')


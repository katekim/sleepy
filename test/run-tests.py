#! /usr/bin/python

import getopt, glob, fnmatch, functools, imp, itertools, unittest, sys

class RunTests:

    def __selectTests (self, patterns):
        conds = []
        for pat in patterns:
            if pat[0] == '-':
                conds.append ((lambda pat : lambda n : not fnmatch.fnmatch (n, pat)) (pat[1:]))
            else:
                conds.append ((lambda pat : lambda n : fnmatch.fnmatch (n, pat)) (pat))
                pass
            pass

        tests = []
        for f in itertools.chain (glob.glob ('*Test.py'), glob.glob ('**/*Test.py')):
            modname = f[:-3]
            fin = open (f)
            mod = imp.load_module (modname, fin, f, ('', '', imp.PY_SOURCE))
            fin.close ()
            for testCase in filter (lambda t: t[-4:] == 'Test', dir (mod)):
                for t in filter (lambda t: t[:4] == 'test', dir (getattr (mod, testCase))):
                    name = '%s.%s' % (modname, t)
                    for cond in conds:
                        if cond (name):
                            tests.append ({'name' : name,
                                           'module' : mod,
                                           'modname' : testCase,
                                           'method' : t})
                            break
                        pass
                    pass
                pass
            pass
        return tests

    def __list (self, patterns):
        for t in self.__selectTests (patterns):
            print t['name']
            pass
        pass

    def __run (self, tests):
        suite = unittest.TestSuite ()
        for t in tests:
            testCase = getattr (t['module'], t['modname']) (t['method'])
            suite.addTest (testCase)
            pass
        result = unittest.TextTestRunner (verbosity = 2).run (suite)
        pass

    def __help (self):
        print """\
Name
====

run-tests.py -- manipulator of unit tests


Usage
=====

 run-tests.py [options] [patterns...]


Options
=======

-h              prints usage.
-l              lists names of test cases.


Patterns
========

A pattern of test is a combination of a test case name and a test
method name concatenated with `.'.  You can also specify patterns by
glob name matching, which is used for Unix pathname expansion.

For a simple example, an exact test method name with an exact test
case name is a valid pattern.

 TestCase1.testMethod1


You can specify all the test methods in TestCase1 by:

 TestCase1.*


The pattern below matches all the test methods in each test case which
begin with `testNormal', though it's rarely useful...

 *.testNormal*


As you can guess, only single wildcard matches everything and, in
fact, it's the default pattern when you specify nothing.

 *


A pattern beginning with `-' indicates a negative selection, which
means run-tests.py runs all the tests except ones that match the
pattern.  Note that in order to avoid having a pattern treated as a
command line parameter, it's a good practice to specify `--' before
patterns of negative selection.

All the tests except ones of TestCase2 will be executed by the pattern
below.

 -TestCase2.*


"""
        pass

    def main (self, argv):
        cmd = 'run'
        optlist, args = getopt.getopt (argv, 'hl')
        for opt in optlist:
            if opt[0] == '-h':
                cmd = 'help'
            elif opt[0] == '-l':
                cmd = 'list'
                pass
            pass

        if cmd == 'run':
            patterns = args if len (args) > 0 else ['*']
            tests = self.__selectTests (patterns)
            self.__run (tests)
        elif cmd == 'list':
            patterns = args if len (args) > 0 else ['*']
            self.__list (patterns)
        elif cmd == 'help':
            self.__help ()    
        else:
            raise Exception ('%s: unsupported command' % cmd)

        return 0

    pass

sys.exit (RunTests ().main (sys.argv[1:]))

#! /usr/bin/python
"""
privilege.py

Copyright (c) 2009-2010, Travis H.

License terms: Same as those of Python itself.

This module is designed to implement the privilege-dropping API
described here:
http://www.cs.berkeley.edu/~daw/papers/setuid-usenix02.pdf
http://www.cs.berkeley.edu/~daw/papers/setuid-login08b.pdf

This topic is complex so you should read at least the second paper
before trying to understand why I'm doing this.

NOTE: This code does not (yet) attempt to work on Solaris and AIX.
That is, you must have getres[ug]id and setres[ug]id to use it.

TODO:
I have added setres[ug]id to python; unsure of when it will
appear; make a future version of this will check for its presence.

Make interface more OO, less imperative.

Implement drop_priv_temp, restore_priv.

Implement on systems without setres[ug]id

Contributors:
Kevin Gilette
"""

from ctypes import *
from ctypes.util import find_library
import os
import pwd
import grp

# Get the name of the Operating System
os_kernel = os.uname()[0]

class PrivilegeFail(Exception):
    pass

clib = CDLL(find_library("c"))

# Tested on x86-64 -- all tests pass when run as root
__uid_t = c_uint
__gid_t = c_uint

_getresuid = clib.getresuid

def getresuid():
    """Get the real, effective, and saved user IDs"""
    # Create some memory locations for getresuid to write to.
    r = __uid_t()
    e = __uid_t()
    s = __uid_t()
    # Call getresuid syscall, passing by reference.
    res = _getresuid(byref(r), byref(e), byref(s))
    if res < 0: raise pythonapi.PyErr_SetFromErrno(py_object(OSError))
    # Convert to python integers.
    return r.value, e.value, s.value

_getresgid = clib.getresgid

def getresgid():
    """Get the real, effective, and saved group IDs"""
    r = __gid_t()
    e = __gid_t()
    s = __gid_t()
    # Call getresgid syscall, passing by reference.
    res = _getresgid(byref(r), byref(e), byref(s))
    if res < 0: raise pythonapi.PyErr_SetFromErrno(py_object(OSError))
    # Convert to python integers.
    return r.value, e.value, s.value

# Import the setresuid system call using ctypes
_setresuid = clib.setresuid
_setresuid.argttypes = [__uid_t, __uid_t, __uid_t]
_setresuid.resttype = c_int

# Import the setresgid system call using ctypes
_setresgid = clib.setresgid
_setresgid.argttypes = [__gid_t, __gid_t, __gid_t]
_setresgid.resttype = c_int

def setresuid(ruid, euid, suid):
    """Set the real, effective, and saved user IDs"""
    res = _setresuid(__uid_t(ruid), __uid_t(euid), __uid_t(suid))
    if res < 0: raise pythonapi.PyErr_SetFromErrno(py_object(OSError))

def setresgid(rgid, egid, sgid):
    """Set the real, effecive, and saved group IDs"""
    res = _setresgid(__gid_t(rgid), __gid_t(egid), __gid_t(sgid))
    if res < 0: raise pythonapi.PyErr_SetFromErrno(py_object(OSError))

def sort_uniq(args):
    """Sort a sequence, discarding duplicates."""
    return sorted(set(args))

class user_credentials:
    """
    This represents the credentials associated with a user.
    User ID
    Group ID
    Supplementary Groups
    This is used as an argument to drop_permanently
    """
    def __init__(self, uid, gid, sups):
        # -1 has special meaning for several set*id calls (ignore)
        if uid == -1: raise PrivilegeFail
        if gid == -1: raise PrivilegeFail
        nm = os.sysconf('SC_NGROUPS_MAX')
        if nm < 0 or nm < len(sups): raise PrivilegeFail
        self.uid = uid
        self.gid = gid
        self.sups = sort_uniq(sups)

def eql_sups(current, target):
    """
    Compare two supplementary group lists, and ignore if effective GID is in current but not target.
    Prerequisite: The supplementary group lists are sorted and filtered for duplicates.
    """
    egid = os.getegid()
    my_current = sort_uniq(current)
    # Instead of tediously ignoring this value, if it's in the current list, then go ahead
    # and add it to the target list 
    if egid in current:
        my_target = target + [ egid ]
    else:
        my_target = target
    my_target = sort_uniq(my_target)
    return my_current == my_target

def get_sups():
    """This is here to give us a layer of abstraction relative to system calls"""
    return os.getgroups()

def set_sups(target_sups):
    """
    This is designed to give us a layer of abstraction from the system calls.
    It also accomodates FreeBSD's idiosyncracy (which is POSIX-compliant) of
    keeping the egid in the supplementary groups list.
    It also makes an effort to not call the setgroups routine if the target
    group list is identical to the current one in force.
    """
    global os_kernel
    if os_kernel == 'FreeBSD':
        target_sups = [ os.getegid() ] + target_sups
    if os.geteuid() == 0:
        # This will raise an OSError exception if it fails
        os.setgroups(target_sups)
    else:
        cur_sups = get_sups()
        # This will probably fail
        if not eql_sups(cur_sups, target_sups):
            # This will raise an OSError exception if it fails
            os.setgroups(target_sups)
    return True

def set_gids(r, e, s):
    """This is here to give us a layer of abstraction relative to system calls"""
    setresgid(r, e, s)

def set_uids(r, e, s):
    """This is here to give us a layer of abstraction relative to system calls"""
    setresuid(r, e, s)

class res_ids:
    """
    This represents the three IDs (group or user) associated with a process.
    """
    def __init__(self, real, effective, saved):
        self.r = real
        self.e = effective
        self.s = saved

class proc_credentials:
    """
    This obtains and represents the credentials associated with a process.
    """
    def __init__(self):
        self.uids = apply(res_ids, getresuid())
        self.gids = apply(res_ids, getresgid())
        self.sups = sort_uniq(os.getgroups())

def get_fs_ids():
    """Get filesystem IDs - applies only to Linux"""
    uid = None
    gid = None
    file = open('/proc/self/status', 'r')
    for line in file:
        fields = line.split()
        if fields[0] == 'Uid:':
            uid = int(fields[4])
        elif fields[0] == 'Gid:':
            gid = int(fields[4])
    return uid, gid

def coerce_user(user):
    if hasattr(user, '__int__'):
        return int(user)
    return pwd.getpwnam(user).pw_uid

def coerce_group(group):
    if hasattr(group, '__int__'):
        return int(group)
    return grp.getgrnam(group).gr_gid

def drop_privileges_permanently(uid, gid, sups):
    """
    This routine is designed to permanently drop all privileges to the
    user, group, and supplementary groups specified.
    """

    uid = coerce_user(uid)
    gid = coerce_group(gid)
    sups = map(coerce_group, sups)

    # This does some syntax checking
    ucred = user_credentials(uid, gid, sups)

    # This is for our convenience
    u = uid
    g = gid

    # Order is important in these three calls
    set_sups(ucred.sups)
    set_gids(g, g, g) # real, effective, saved
    set_uids(u, u, u) # real, effective, saved

    # Check that we actually did what we expected or throw exception.
    pc = proc_credentials()
    # Portably compare the supplementary group list
    if not eql_sups(pc.sups, ucred.sups): raise PrivilegeFail
    # Check all the gids
    if not (g == pc.gids.r and g == pc.gids.e and g == pc.gids.s):
        raise PrivilegeFail
    # Check all the uids
    if not (u == pc.uids.r and u == pc.gids.e and u == pc.uids.s):
        raise PrivilegeFail
    global os_kernel
    if os_kernel == 'Linux':
        if get_fs_ids() != (u, g): raise PrivilegeFail

# This is all test code
# It is run if this script is invoked directly
if __name__ == '__main__':

    import unittest

    class test_getresXid(unittest.TestCase):
        """Test the calls to getresXid"""
        def test__getresuid(self):
            # TODO: is there any way to avoid redefining this here?  I tried a global but it didn't
            # work.
            # Note: the double-leading underscore may be getting special-cased by python.
            __uid_t = c_int
            r = __uid_t()
            e = __uid_t()
            s = __uid_t()
            ret = _getresuid(byref(r), byref(e), byref(s))
            self.assertEqual(ret, 0)
            self.assertEqual(r.value, os.getuid())
            self.assertEqual(e.value, os.geteuid())
            # NOTE: no other portable way to get saved UID
        def test_getresuid(self):
            (r, e, s) = getresuid()
            self.assertEqual(r, os.getuid())
            self.assertEqual(e, os.geteuid())
            # NOTE: no other portable way to get saved UID
        def test__getresgid(self):
            __gid_t = c_int
            r = __gid_t()
            e = __gid_t()
            s = __gid_t()
            ret = _getresgid(byref(r), byref(e), byref(s))
            self.assertEqual(ret, 0)
            self.assertEqual(r.value, os.getgid())
            self.assertEqual(e.value, os.getegid())
            # NOTE: no other portable way to get saved GID
        def test_getresgid(self):
            (r, e, s) = getresgid()
            self.assertEqual(r, os.getgid())
            self.assertEqual(e, os.getegid())
            # NOTE: no other portable way to get saved GID

    class test_setresuid(unittest.TestCase):
        """Test the call to setresuid"""
        def setUp(self):
            self.uid = os.geteuid()
        def test__setresuid(self):
            __uid_t = c_int
            r1 = __uid_t(1)
            e1 = __uid_t(1)
            # Must save root UID so that we can reset UIDs for other tests
            s1 = __uid_t(0)
            if self.uid == 0:
                rv = _setresuid(r1, e1, s1)
                self.assertEqual(rv, 0)
                (r2, e2, s2) = getresuid()
                self.assertEqual(r1.value, r2)
                self.assertEqual(e1.value, e2)
                self.assertEqual(s1.value, s2)
            else:
                rv = _setresuid(r1, e1, s1)
                self.assertEqual(rv, -1)
        def test_setresuid(self):
            if self.uid == 0:
                setresuid(1,1,0)
                (r, e, s) = getresuid()
                self.assertEqual(r, 1)
                self.assertEqual(e, 1)
                self.assertEqual(s, 0)
            else:
                self.assertRaises(OSError, setresuid, 1, 1, 1)
        def tearDown(self):
            if self.uid == 0:
                # Restore UIDs for next test
                _setresuid(0, 0, 0)

    class test_setresgid(unittest.TestCase):
        """Test the call to setresgid"""
        def setUp(self):
            self.uid = os.geteuid()
        def test__setresgid(self):
            __gid_t = c_int
            r1 = __gid_t(1)
            e1 = __gid_t(1)
            s1 = __gid_t(1)
            if self.uid == 0:
                rv = _setresgid(r1, e1, s1)
                self.assertEqual(rv, 0)
                (r2, e2, s2) = getresgid()
                self.assertEqual(r1.value, r2)
                self.assertEqual(e1.value, e2)
                self.assertEqual(s1.value, s2)
            else:
                rv = _setresgid(r1, e1, s1)
                self.assertEqual(rv, -1)
        def test_setresgid(self):
            if self.uid == 0:
                setresgid(1,1,1)
                (r, e, s) = getresgid()
                self.assertEqual(r, 1)
                self.assertEqual(e, 1)
                self.assertEqual(s, 1)
            else:
                self.assertRaises(OSError, setresgid, 1, 1, 1)

    class test_sort_uniq(unittest.TestCase):
        def test_sort_uniq(self):
            l = [ 'c', 'a', 'b', 'a' ]
            self.assertEqual(sort_uniq(l), [ 'a', 'b', 'c'])

    class test_user_credentials(unittest.TestCase):
        def test_negatives(self):
            self.assertRaises(PrivilegeFail, user_credentials, -1, 0, [])
            self.assertRaises(PrivilegeFail, user_credentials, 0, -1, [])
            uc = user_credentials(0, 0, [0, 1])

    class test_eql_sups(unittest.TestCase):
        def test_equal(self):
            self.assert_(eql_sups([0, 1, 2], [0, 1, 2]))
        def test_contains_egid(self):
            self.assert_(eql_sups(sort_uniq([0, 1, 2, os.getegid()]), [0, 1, 2]))
            self.assert_(eql_sups(sort_uniq([0, 1, os.getegid(), 9999]), [0, 1, 9999]))

    class test_get_sups(unittest.TestCase):
        def test(self):
            self.assertEqual(os.getgroups(), get_sups())

    class test_set_sups(unittest.TestCase):
        def test_equal(self):
            sups = os.getgroups()
            set_sups(sups)
            self.assertEqual(sups, os.getgroups())
        def test_unequal(self):
            old_sups = os.getgroups()
            sups = [ 1, 2, 3 ]
            if os.geteuid() == 0:
                set_sups(sups)
                self.assert_(eql_sups(os.getgroups(), sups))
                # Clean up by resetting supplementary groups
                set_sups(old_sups)
            else:
                self.assertRaises(OSError, set_sups, sups)

    class test_res_ids(unittest.TestCase):
        def test_res_ids(self):
            ids = res_ids(1, 2, 3)
            self.assertEqual(ids.r, 1)
            self.assertEqual(ids.e, 2)
            self.assertEqual(ids.s, 3)

    class test_proc_credentials(unittest.TestCase):
        def test_pc(self):
            pc = proc_credentials()
            self.assertEqual(pc.uids.r, os.getuid())
            self.assertEqual(pc.uids.e, os.geteuid())
            self.assertEqual(pc.uids.s, (getresuid())[2])
            self.assertEqual(pc.gids.r, os.getgid())
            self.assertEqual(pc.gids.e, os.getegid())
            self.assertEqual(pc.gids.s, (getresgid())[2])
            self.assertEqual(pc.sups, sort_uniq(os.getgroups()))

    class test_get_fs_ids(unittest.TestCase):
        def test_get_fs_ids(self):
            uid, gid = get_fs_ids()
            self.assertEqual(uid, os.getuid())
            self.assertEqual(gid, os.getgid())

    class test_drop_privs(unittest.TestCase):
        def test_drop_privs(self):
            """This test must be run last"""
            if os.geteuid() == 0:
                drop_privileges_permanently(1, 1, [1])

    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(test_getresXid))
    suite.addTest(unittest.makeSuite(test_setresuid))
    suite.addTest(unittest.makeSuite(test_setresgid))
    suite.addTest(unittest.makeSuite(test_sort_uniq))
    suite.addTest(unittest.makeSuite(test_user_credentials))
    suite.addTest(unittest.makeSuite(test_eql_sups))
    suite.addTest(unittest.makeSuite(test_set_sups))
    suite.addTest(unittest.makeSuite(test_res_ids))
    suite.addTest(unittest.makeSuite(test_proc_credentials))
    suite.addTest(unittest.makeSuite(test_get_fs_ids))
    suite.addTest(unittest.makeSuite(test_drop_privs))
    unittest.TextTestRunner().run(suite)

import unittest

from pyramid import testing
from zope.interface.verify import verifyClass
from zope.interface.verify import verifyObject

from voteit.groups.interfaces import IGroup
from voteit.groups.interfaces import IGroups


class GroupTests(unittest.TestCase):
    def setUp(self):
        self.config = testing.setUp()

    def tearDown(self):
        testing.tearDown()

    @property
    def _cut(self):
        from voteit.groups.models import Group
        return Group

    def test_verify_class(self):
        self.assertTrue(verifyClass(IGroup, self._cut))

    def test_verify_object(self):
        self.assertTrue(verifyObject(IGroup, self._cut()))

    def test_set_members(self):
        userids = ['a', 'b', 'c']
        obj = self._cut()
        obj.set_field_value('members', userids)
        self.assertEqual(obj.get_field_value('members'), frozenset(userids))


class GroupsTests(unittest.TestCase):
    def setUp(self):
        self.config = testing.setUp()

    def tearDown(self):
        testing.tearDown()

    @property
    def _cut(self):
        from voteit.groups.models import Groups
        return Groups

    def test_verify_class(self):
        self.assertTrue(verifyClass(IGroups, self._cut))

    def test_verify_object(self):
        self.assertTrue(verifyObject(IGroups, self._cut()))
